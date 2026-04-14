import requests
import pandas as pd

url = "https://paleobiodb.org/data1.2/occs/list.csv"

params = {
    "base_name"  : "Mammalia",
    "lngmin"     : -170,
    "lngmax"     : -30,
    "latmin"     : -60,
    "latmax"     : 75,
    "max_ma"     : 12,
    "min_ma"     : 0.5,
    "taxon_reso" : "genus",
    "show"       : "coords,classext,ident,stratext",
    "limit"      : "99999",
}

print("Downloading from PBDB, this might take a minute...")
response = requests.get(url, params=params, timeout=120)

if response.status_code == 200:
    with open("gabi_raw.csv", "wb") as f:
        f.write(response.content)
    print("Done. Saved as gabi_raw.csv")
else:
    print(f"Something went wrong: {response.status_code}")
    print(response.text[:500])

df = pd.read_csv("gabi_raw.csv")
print(f"\nTotal records: {len(df)}")
print(f"Age range: {df['min_ma'].min()} – {df['max_ma'].max()} Ma")
print(f"Lat range: {df['lat'].min():.2f} to {df['lat'].max():.2f}")
print(f"\nFirst few rows:")
print(df.head())
