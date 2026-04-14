import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("gabi_clean.csv")

bias = df.groupby(["time_bin", "continent"])["occurrence_no"].count().unstack(fill_value=0)
bias = bias.sort_values("time_bin", ascending=False)

na_counts = bias["North America"].values
sa_counts = bias["South America"].values
bins      = bias.index.values
x         = np.arange(len(bins))
width     = 0.38

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(11, 8),
    gridspec_kw={"height_ratios": [3, 1]},
    sharex=True
)
fig.patch.set_facecolor("white")

ax1.set_facecolor("#FAFAFA")
bars_na = ax1.bar(x - width/2, na_counts, width, color="#378ADD",
                  alpha=0.85, label="North America", zorder=3)
bars_sa = ax1.bar(x + width/2, sa_counts, width, color="#1D9E75",
                  alpha=0.85, label="South America", zorder=3)

for bar in bars_na:
    h = bar.get_height()
    if h > 0:
        ax1.text(bar.get_x() + bar.get_width()/2, h + 30, str(int(h)),
                 ha="center", va="bottom", fontsize=7.5, color="#0C447C")

for bar in bars_sa:
    h = bar.get_height()
    if h > 0:
        ax1.text(bar.get_x() + bar.get_width()/2, h + 30, str(int(h)),
                 ha="center", va="bottom", fontsize=7.5, color="#085041")

isthmus_idx = np.where(bins == 3.0)[0]
if len(isthmus_idx):
    ax1.axvline(x=isthmus_idx[0], color="#D85A30",
                linewidth=1.8, linestyle="--", zorder=4, alpha=0.8)
    ax1.text(isthmus_idx[0] + 0.15, 3500, "~3 Ma\nIsthmus",
             fontsize=8.5, color="#993C1D")

ax1.set_ylabel("Number of PBDB occurrences", fontsize=11, labelpad=8)
ax1.set_title(
    "Sampling bias: North America vs South America fossil record density\n"
    "Mammalia, 12–1 Ma (1 Ma bins)",
    fontsize=12, fontweight="normal", pad=12
)
ax1.legend(fontsize=10, framealpha=0.9, edgecolor="#D3D1C7", fancybox=False)
ax1.grid(axis="y", color="#E8E6E0", linewidth=0.6, zorder=0)
for spine in ax1.spines.values():
    spine.set_edgecolor("#D3D1C7")
    spine.set_linewidth(0.8)

ax1.annotate(
    f"NA:SA ratio overall ~{na_counts.sum()/sa_counts.sum():.1f}:1\nSubsampling applied before NND analysis",
    xy=(0.02, 0.92), xycoords="axes fraction",
    fontsize=8.5, color="#444441",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#F1EFE8",
              edgecolor="#B4B2A9", linewidth=0.8)
)

ax2.set_facecolor("#FAFAFA")
ratio = np.where(sa_counts > 0, na_counts / sa_counts, np.nan)
ax2.bar(x, ratio, width * 2.1, color="#7F77DD", alpha=0.75, zorder=3)
ax2.axhline(y=1.0, color="#888780", linewidth=1.2, linestyle="--", zorder=4)
ax2.text(len(bins) - 0.5, 1.08, "equal sampling", fontsize=8,
         color="#5F5E5A", ha="right")

if len(isthmus_idx):
    ax2.axvline(x=isthmus_idx[0], color="#D85A30",
                linewidth=1.8, linestyle="--", zorder=4, alpha=0.8)

ax2.set_ylabel("NA : SA ratio", fontsize=10, labelpad=8)
ax2.set_ylim(0, max(ratio[~np.isnan(ratio)]) * 1.2)
ax2.grid(axis="y", color="#E8E6E0", linewidth=0.6, zorder=0)
for spine in ax2.spines.values():
    spine.set_edgecolor("#D3D1C7")
    spine.set_linewidth(0.8)

ax2.set_xticks(x)
ax2.set_xticklabels([f"{int(b)} Ma" for b in bins], fontsize=9)
ax2.set_xlabel("Time bin (Ma) — older to recent", fontsize=11, labelpad=8)

plt.tight_layout(h_pad=0.6)
plt.savefig("figure3_bias_chart.png", dpi=300, bbox_inches="tight", facecolor="white")
print("Saved figure3_bias_chart.png")
plt.show()
