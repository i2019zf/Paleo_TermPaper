import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import BallTree
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("gabi_clean.csv")
print(f"Records loaded: {len(df)}")

EARTH_RADIUS_KM = 6371
epsilon_km_values = [600, 800, 1000]
MIN_SAMPLES = 5
SKIP_BINS = [10.0]

time_bins = sorted(df["time_bin"].dropna().unique())
results = []

def run_dbscan(points, eps_rad):
    coords = np.radians(points[["lat", "lng"]].values)
    labels = DBSCAN(
        eps=eps_rad, min_samples=MIN_SAMPLES,
        algorithm="ball_tree", metric="haversine"
    ).fit_predict(coords)
    return labels

for eps_km in epsilon_km_values:
    eps_rad = eps_km / EARTH_RADIUS_KM
    print(f"\nepsilon = {eps_km} km")

    for tbin in time_bins:
        if tbin in SKIP_BINS:
            print(f"  {tbin} Ma — skipped, too few records")
            results.append({
                "time_bin": tbin, "epsilon_km": eps_km,
                "nnd_km": np.nan, "na_clusters": np.nan,
                "sa_clusters": np.nan, "status": "skipped"
            })
            continue

        subset = df[df["time_bin"] == tbin].copy()
        na = subset[subset["continent"] == "North America"].copy()
        sa = subset[subset["continent"] == "South America"].copy()

        if len(na) < MIN_SAMPLES or len(sa) < MIN_SAMPLES:
            print(f"  {tbin} Ma — skipped, too sparse (NA={len(na)}, SA={len(sa)})")
            results.append({
                "time_bin": tbin, "epsilon_km": eps_km,
                "nnd_km": np.nan, "na_clusters": 0,
                "sa_clusters": 0, "status": "sparse"
            })
            continue

        na["cluster"] = run_dbscan(na, eps_rad)
        sa["cluster"] = run_dbscan(sa, eps_rad)

        na_clusters = len(set(na["cluster"]) - {-1})
        sa_clusters = len(set(sa["cluster"]) - {-1})

        na_core = na[na["cluster"] != -1][["lat", "lng"]]
        sa_core = sa[sa["cluster"] != -1][["lat", "lng"]]

        if len(na_core) == 0 or len(sa_core) == 0:
            nnd_km = np.nan
            status = "no_core_points"
        else:
            tree = BallTree(np.radians(sa_core.values), metric="haversine")
            dists, _ = tree.query(np.radians(na_core.values), k=1)
            nnd_km = float(np.min(dists) * EARTH_RADIUS_KM)
            status = "ok"

        print(f"  {tbin} Ma — NA clusters: {na_clusters}, SA clusters: {sa_clusters}, NND: {nnd_km:.0f} km")

        results.append({
            "time_bin"   : tbin,
            "epsilon_km" : eps_km,
            "nnd_km"     : round(nnd_km, 1) if not np.isnan(nnd_km) else np.nan,
            "na_clusters": na_clusters,
            "sa_clusters": sa_clusters,
            "status"     : status
        })

results_df = pd.DataFrame(results)
results_df.to_csv("nnd_results.csv", index=False)
print("\nSaved nnd_results.csv")

print("\nCore result (epsilon = 800 km):")
core = results_df[results_df["epsilon_km"] == 800].dropna(subset=["nnd_km"])
core = core.sort_values("time_bin", ascending=False)
print(core[["time_bin", "nnd_km", "na_clusters", "sa_clusters"]].to_string(index=False))

threshold = 1500
merge_candidates = core[core["nnd_km"] < threshold].sort_values("time_bin", ascending=False)
if len(merge_candidates) > 0:
    merge_start = merge_candidates["time_bin"].max()
    merge_end   = merge_candidates["time_bin"].min()
    midpoint = (merge_start + merge_end) / 2
    diff = 3.0 - midpoint
    print(f"\nDetected merge window: {merge_end} Ma – {merge_start} Ma")
    print(f"Known Isthmus date: ~3 Ma")
    print(f"Offset from 3 Ma: {abs(diff):.1f} Ma {'earlier' if diff < 0 else 'later'}")
else:
    print(f"\nNo merge detected below {threshold} km threshold.")
