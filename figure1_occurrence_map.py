import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.lines import Line2D

df = pd.read_csv("gabi_clean.csv")

plot_bins = [11.0, 9.0, 7.0, 5.0, 3.0, 1.0]
titles    = ["11 Ma", "9 Ma", "7 Ma", "5 Ma", "3 Ma (Isthmus forms)", "1 Ma"]

fig, axes = plt.subplots(
    2, 3, figsize=(14, 9),
    subplot_kw={"projection": ccrs.PlateCarree()}
)
fig.suptitle(
    "Fossil occurrence distribution across time — North vs South America\nMammalia (PBDB)",
    fontsize=13, y=1.01
)

for ax, tbin, title in zip(axes.flat, plot_bins, titles):
    ax.set_extent([-170, -30, -60, 75], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND,      facecolor="#F0EDE8", zorder=0)
    ax.add_feature(cfeature.OCEAN,     facecolor="#D6E8F0", zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.4, edgecolor="#888888", zorder=1)
    ax.add_feature(cfeature.BORDERS,   linewidth=0.3, edgecolor="#AAAAAA",
                   linestyle=":", zorder=1)
    ax.add_feature(cfeature.LAKES,     facecolor="#D6E8F0", zorder=1)

    subset = df[df["time_bin"] == tbin]
    na = subset[subset["continent"] == "North America"]
    sa = subset[subset["continent"] == "South America"]

    if len(na) > 0:
        ax.scatter(na["lng"], na["lat"], s=8, color="steelblue",
                   alpha=0.55, transform=ccrs.PlateCarree(), zorder=3)
    if len(sa) > 0:
        ax.scatter(sa["lng"], sa["lat"], s=8, color="seagreen",
                   alpha=0.55, transform=ccrs.PlateCarree(), zorder=3)

    ax.plot([-170, -30], [10, 10], color="tomato", linewidth=0.9,
            linestyle="--", transform=ccrs.PlateCarree(), zorder=4)

    ax.set_title(f"{title}  |  NA={len(na)}  SA={len(sa)}", fontsize=9, pad=4)

legend_elements = [
    Line2D([0],[0], marker="o", color="w", markerfacecolor="steelblue",
           markersize=8, label="North America"),
    Line2D([0],[0], marker="o", color="w", markerfacecolor="seagreen",
           markersize=8, label="South America"),
    Line2D([0],[0], color="tomato", linewidth=1.2, linestyle="--",
           label="10°N continental split"),
]
fig.legend(handles=legend_elements, loc="lower center", ncol=3,
           fontsize=10, framealpha=0.9, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
plt.savefig("figure1_occurrence_map.png", dpi=200, bbox_inches="tight", facecolor="white")
print("Saved figure1_occurrence_map.png")
plt.show()
