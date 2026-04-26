"""
Visual 5: Net Funding Requirement — Quarterly Profile, Q3 2024 – Q4 2025
Prysmian Group Dissertation
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
OUT_DIR = HERE / "pngs"
OUT_DIR.mkdir(exist_ok=True)

# ── Shared style constants (consistent with all visuals) ──────────────────────
FONT        = "Times New Roman"
TITLE_SIZE  = 14.5
LABEL_SIZE  = 11.5
TICK_SIZE   = 10
NOTE_SIZE   = 8.5
DPI         = 300
FIG_W, FIG_H = 13, 9.5

C = {
    "navy"     : "#1a1a1a",
    "blue_hi"  : "#185FA5",
    "blue_lo"  : "#A8CCEE",
    "blue_fill": "#C8DCF0",
    "red"      : "#A0281E",
    "teal"     : "#1D9E75",
    "teal_lt"  : "#E0F4EE",
    "grid"     : "#E8E8E8",
    "axis_text": "#666666",
    "note_text": "#999999",
    "mid"      : "#777777",
    "bg_even"  : "#EBF4FB",   # lighter blue — Q3, Q1, Q3…
    "bg_odd"   : "#D2E8F5",   # darker  blue — Q4, Q2, Q4…
    "sep"      : "#DDDDDD",
}

quarters = ["Q3 '24", "Q4 '24", "Q1 '25", "Q2 '25", "Q3 '25", "Q4 '25"]
qlabels  = ["Q3\n'24", "Q4\n'24", "Q1\n'25", "Q2\n'25", "Q3\n'25", "Q4\n'25"]

nfr       = [2126, 1309, 1804, 1691, 2148,  938]
nfd       = [5042, 4296, 4884, 4694, 4318, 3097]
ebitda_tm = [1751, 1927, 2042, 2190, 2294, 2398]
fcf_tm    = [ 979, 1011,  998,  979,  859, 1171]
mat       = 5160

r_debt = [nfr[i] / nfd[i]       * 100 for i in range(6)]
r_ebi  = [nfr[i] / ebitda_tm[i] * 100 for i in range(6)]
r_fcf  = [nfr[i] / fcf_tm[i]    * 100 for i in range(6)]
r_mat  = [nfr[i] / mat          * 100 for i in range(6)]

x = np.arange(6)

plt.rcParams.update({
    "font.family"        : FONT,
    "axes.spines.top"    : False,
    "axes.spines.right"  : False,
    "axes.spines.left"   : False,
    "axes.spines.bottom" : False,
    "xtick.bottom"       : False,
    "ytick.left"         : False,
})

fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor="white")

gs = fig.add_gridspec(
    2, 1,
    height_ratios=[2.8, 1.6],
    hspace=0.28,
    left=0.08, right=0.97,
    top=0.88, bottom=0.22,
)
ax_hero = fig.add_subplot(gs[0])
gs_bot  = gs[1].subgridspec(1, 4, wspace=0.0)
ax_r    = [fig.add_subplot(gs_bot[0, c]) for c in range(4)]

# ══════════════════════════════════════════════════════════════
# HERO PANEL
# ══════════════════════════════════════════════════════════════
ax = ax_hero

# Colour boundary falls exactly at each quarter tick (0,1,2,3,4,5)
_edges = [0, 1, 2, 3, 4, 5]
for _j in range(len(_edges) - 1):
    _bg = C["bg_even"] if _j % 2 == 0 else C["bg_odd"]
    ax.axvspan(_edges[_j], _edges[_j + 1], color=_bg, zorder=0, linewidth=0)

# Grid — custom ticks: dense 0–1000, then 500-step
hero_yticks = [0, 500, 1000, 1500, 2000, 2500]
for gv in hero_yticks:
    ax.axhline(gv, color=C["grid"], linewidth=0.7, zorder=0)

# Area + line
ax.fill_between(x, nfr, 0, color=C["blue_fill"], alpha=0.55, linewidth=0, zorder=1)
ax.plot(x, nfr, color=C["blue_hi"], linewidth=2.4, zorder=4,
        marker="o", markersize=7,
        markerfacecolor=C["blue_hi"],
        markeredgecolor="white", markeredgewidth=1.8)

# Q4 year-end markers (teal)
for i in [1, 5]:
    ax.scatter(i, nfr[i], s=100, color=C["teal"],
               zorder=5, edgecolors="white", linewidths=1.8)

# Data labels
offsets = [120, -175, 120, 120, 120, -175]
for i, v in enumerate(nfr):
    col = C["teal"] if i in [1, 5] else C["navy"]
    ax.text(x[i], v + offsets[i], f"€{v:,}m",
            ha="center", va="center",
            fontsize=9.5, color=col, fontweight="bold", zorder=6)

# Year-end dip callout
ax.annotate(
    "Year-end NFR systematically\nlower than intra-year peaks",
    xy=(1, nfr[1]), xytext=(1.8, 650),
    fontsize=8.5, color=C["teal"], ha="left",
    arrowprops=dict(arrowstyle="-", color=C["teal"],
                    lw=0.9, connectionstyle="arc3,rad=0.25"),
    bbox=dict(boxstyle="round,pad=0.35", facecolor=C["teal_lt"],
              edgecolor=C["teal"], linewidth=0.7, alpha=0.95),
    zorder=7,
)

# Axes
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(0, 2800)
ax.set_xticks(x)
ax.set_xticklabels([])          # strips below show quarter labels
ax.tick_params(axis="both", which="both", length=0)
ax.set_yticks(hero_yticks)
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda v, _: f"€{v/1000:.1f}bn" if v >= 1000 else (f"€{int(v)}m" if v > 0 else "0")))
ax.tick_params(axis="y", labelsize=TICK_SIZE - 1, labelcolor=C["axis_text"])
ax.set_ylabel("Net funding requirement (€m)",
              fontsize=LABEL_SIZE - 2, color=C["axis_text"], labelpad=8)

# ══════════════════════════════════════════════════════════════
# RATIO STRIPS — shared exponential-style scale across all 4 panels
# Dense ticks 0–50 (like NFR_Comp 0–40), sparse above
# ══════════════════════════════════════════════════════════════
STRIP_YTICKS = [0, 25, 50, 100, 150, 200, 250]   # dense low, sparse high
STRIP_YMAX   = 270                                 # shared ceiling

strip_configs = [
    ("NFR / net\nfinancial debt",   r_debt, None,  C["blue_hi"]),
    ("NFR /\nadj. EBITDA (TTM)",    r_ebi,  None,  C["blue_hi"]),
    ("NFR / free\ncash flow (TTM)", r_fcf,  100.0, C["blue_hi"]),
    ("NFR / 2027–31\nmaturities",   r_mat,  None,  C["blue_hi"]),
]

for col, (title, vals, threshold, lcolor) in enumerate(strip_configs):
    ra = ax_r[col]
    ymax = STRIP_YMAX

    # Colour boundary exactly at each quarter tick
    for _j in range(len(_edges) - 1):
        _bg = C["bg_even"] if _j % 2 == 0 else C["bg_odd"]
        ra.axvspan(_edges[_j], _edges[_j + 1], color=_bg, zorder=0, linewidth=0)

    # Grid at shared tick positions
    for gv in STRIP_YTICKS:
        ra.axhline(gv, color=C["grid"], linewidth=0.7, zorder=0)

    # 100% line (FCF panel)
    if threshold:
        ra.axhline(threshold, color=C["red"], linewidth=1.1,
                   linestyle=(0, (4, 3)), zorder=6)

    # Area + line
    ra.fill_between(x, vals, 0, color=C["blue_fill"], alpha=0.45, linewidth=0, zorder=1)
    ra.plot(x, vals, color=lcolor, linewidth=1.9, zorder=4,
            marker="o", markersize=4.5,
            markerfacecolor=lcolor,
            markeredgecolor="white", markeredgewidth=1.3)

    # Q4 teal dots
    for i in [1, 5]:
        ra.scatter(i, vals[i], s=45, color=C["teal"],
                   zorder=5, edgecolors="white", linewidths=1.3)

    # Labels on Q4s and peak only
    peak_i = vals.index(max(vals))
    labeled = sorted(set([1, peak_i, 5]))
    for i in labeled:
        col_l = C["teal"] if i in [1, 5] else C["navy"]
        ra.text(x[i], vals[i] + ymax * 0.04,
                f"{vals[i]:.0f}%",
                ha="center", va="bottom",
                fontsize=7.5, color=col_l, fontweight="bold", zorder=6)

    # Axes
    ra.set_xlim(-0.5, 5.5)
    ra.set_ylim(0, ymax)
    ra.set_xticks(x)
    ra.set_xticklabels(qlabels, fontsize=7, color=C["axis_text"], linespacing=1.2)
    ra.tick_params(axis="both", which="both", length=0)
    ra.set_yticks(STRIP_YTICKS)

    if col == 0:
        ra.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
        ra.tick_params(axis="y", labelsize=7.5, labelcolor=C["axis_text"])
    else:
        ra.set_yticklabels([])

    # Panel title above bars
    ra.text(0.5, 1.04, title,
            ha="center", va="bottom", fontsize=8.5,
            color=C["navy"], fontweight="bold",
            transform=ra.transAxes, linespacing=1.35)

    # Separator between panels
    if col < 3:
        lx = ra.get_position().x1 + 0.003
        fig.add_artist(plt.Line2D(
            [lx, lx], [gs[1].get_position(fig).y0, gs[1].get_position(fig).y1],
            transform=fig.transFigure,
            color=C["sep"], linewidth=0.7,
        ))

# Divider between hero and ratio strips
div_y = gs_bot[0, 0].get_position(fig).y1 + 0.005
fig.add_artist(plt.Line2D(
    [0.08, 0.97], [div_y, div_y],
    transform=fig.transFigure,
    color=C["sep"], linewidth=0.9,
))

# ── Title & subtitle ──────────────────────────────────────────────────────────
fig.text(0.08, 0.975,
         "Net funding requirement — quarterly profile, Q3 2024–Q4 2025",
         fontsize=TITLE_SIZE, fontweight="bold", color=C["navy"],
         ha="left", va="bottom")
fig.text(0.08, 0.945,
         "Prysmian Group  ·  NFR = trade receivables + contract assets + inventories − trade payables − contract liabilities",
         fontsize=LABEL_SIZE - 2.5, color=C["axis_text"],
         ha="left", va="bottom")

# ── Legend ────────────────────────────────────────────────────────────────────
legend_items = [
    plt.Line2D([0], [0], color=C["blue_hi"], linewidth=2,
               marker="o", markerfacecolor=C["blue_hi"],
               markeredgecolor="white", markersize=6,
               label="NFR / ratio"),
    plt.Line2D([0], [0], color="w", marker="o",
               markerfacecolor=C["teal"], markersize=7,
               markeredgecolor="white",
               label="Q4 year-end"),
    plt.Line2D([0], [0], color=C["red"], linewidth=1.2,
               linestyle=(0, (4, 3)), label="NFR = FCF (100%)"),
]
fig.legend(handles=legend_items,
           loc="upper right",
           bbox_to_anchor=(0.97, 0.978),
           fontsize=LABEL_SIZE - 3, frameon=False,
           labelcolor="#444444",
           handlelength=1.4, handleheight=0.9,
           ncol=3, columnspacing=1.2)

# ── Source note ───────────────────────────────────────────────────────────────
fig.text(0.08, 0.02,
         "Sources: Prysmian quarterly interim reports and results presentations, Q3 2024–Q4 2025. "
         "Contract liabilities at Q4'24 and Q4'25 from annual report IFRS 15 notes.\n"
         "Adj. EBITDA and FCF on trailing-twelve-month basis. FCF excludes acquisitions and disposals.",
         fontsize=NOTE_SIZE, color=C["note_text"], ha="left", va="bottom")

plt.savefig(str(OUT_DIR / "visual_nfr_quarterly.png"),
            dpi=DPI, bbox_inches="tight", facecolor="white")
print("Saved.")
