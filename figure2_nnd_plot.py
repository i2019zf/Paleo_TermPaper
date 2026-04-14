import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("nnd_results.csv")

eps_styles = {
    600:  {"color": "#B5D4F4", "lw": 1.2, "ls": "--",  "label": "ε = 600 km"},
    800:  {"color": "#185FA5", "lw": 2.2, "ls": "-",   "label": "ε = 800 km (main)"},
    1000: {"color": "#9FE1CB", "lw": 1.2, "ls": ":",   "label": "ε = 1000 km"},
}

fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("#FAFAFA")

for eps, style in eps_styles.items():
    sub = df[(df["epsilon_km"] == eps) & (df["status"] == "ok")].copy()
    sub = sub.sort_values("time_bin", ascending=False)
    ax.plot(
        sub["time_bin"], sub["nnd_km"],
        color=style["color"], linewidth=style["lw"],
        linestyle=style["ls"], marker="o",
        markersize=5 if eps == 800 else 3,
        markerfacecolor=style["color"],
        zorder=3 if eps == 800 else 2,
        label=style["label"]
    )

core = df[(df["epsilon_km"] == 800) & (df["status"] == "ok")].sort_values("time_bin")
for _, row in core.iterrows():
    if row["time_bin"] in [1.0, 2.0, 3.0, 7.0, 11.0]:
        offset = (12, -18) if row["time_bin"] in [3.0, 7.0] else (12, 8)
        ax.annotate(
            f"{row['nnd_km']:.0f} km",
            xy=(row["time_bin"], row["nnd_km"]),
            xytext=offset, textcoords="offset points",
            fontsize=8, color="#185FA5",
            arrowprops=dict(arrowstyle="-", color="#B5D4F4", lw=0.8)
        )

ax.axvline(x=3.0, color="#D85A30", linewidth=1.8, linestyle="--",
           zorder=4, label="Isthmus of Panama (~3 Ma)")
ax.axhline(y=1500, color="#888780", linewidth=1.0, linestyle=":", zorder=1)
ax.text(11.3, 1570, "merge threshold (1500 km)", fontsize=8, color="#888780", ha="right")
ax.axvspan(2.0, 3.0, alpha=0.08, color="#D85A30", zorder=0, label="detected merge window")

ax.annotate(
    "6 Ma anomaly\n(SA sampling spike)",
    xy=(6.0, 1094), xytext=(7.2, 1400),
    fontsize=8, color="#5F5E5A",
    arrowprops=dict(arrowstyle="->", color="#B4B2A9", lw=0.8)
)

ax.set_xlim(12.2, 0.3)
ax.set_ylim(-200, 7000)
ax.set_xlabel("Time (Ma) — older to recent", fontsize=11, labelpad=8)
ax.set_ylabel("Nearest Neighbor Distance (km)", fontsize=11, labelpad=8)
ax.set_title(
    "Inter-continental fossil cluster distance across the GABI window\n"
    "North America vs South America, Mammalia, 11–1 Ma",
    fontsize=12, fontweight="normal", pad=12
)
ax.set_xticks(range(1, 12))
ax.set_xticklabels([f"{x} Ma" for x in range(1, 12)], fontsize=9)
ax.tick_params(axis="both", which="both", length=3, color="#B4B2A9")
for spine in ax.spines.values():
    spine.set_edgecolor("#D3D1C7")
    spine.set_linewidth(0.8)
ax.grid(axis="y", color="#E8E6E0", linewidth=0.6, zorder=0)
ax.legend(loc="upper right", fontsize=9, framealpha=0.9,
          edgecolor="#D3D1C7", fancybox=False)

plt.tight_layout()
plt.savefig("figure2_nnd_plot.png", dpi=300, bbox_inches="tight", facecolor="white")
print("Saved figure2_nnd_plot.png")
plt.show()
