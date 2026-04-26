"""
S&P-Style Adjusted FFO to Debt Ratio — Prysmian Group, 2018–2025
Version 2 — Editorial / FT-grade design
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.lines as mlines
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
OUT_DIR = HERE / "pngs"
OUT_DIR.mkdir(exist_ok=True)

FONT        = "Times New Roman"
DPI         = 300
FIG_W, FIG_H = 13, 7.8

MARGINS = dict(left=0.07, right=0.97, top=0.91, bottom=0.14)

C = {
    "navy"     : "#0A2342",
    "blue_hi"  : "#185FA5",
    "blue_lo"  : "#C8DCF0",
    "amber"    : "#C47A1E",      # 2025: barely above — warning colour
    "amber_lt" : "#FDF3E3",      # danger-zone band fill
    "red"      : "#A0281E",
    "red_lt"   : "#F5E8E7",
    "teal"     : "#1D9E75",
    "grid"     : "#EBEBEB",
    "mid"      : "#888888",
    "light"    : "#BBBBBB",
    "note"     : "#999999",
    "bg_alt"   : "#F8F8F7",
}

years   = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
ebitda  = [ 767, 1007,  840,  976, 1488, 1628, 1927, 2398]
ffo     = [ 573,  802,  612,  777, 1196, 1228, 1524, 1896]
debt    = [3309, 3297, 3231, 3797, 3200, 3200, 5503, 5308]
ratio   = [17.3, 24.3, 18.9, 20.5, 37.4, 38.4, 27.7, 35.7]
SP35    = 35.0

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

# ── Two zones: chart (70%) + data strip (30%) ─────────────────────────────────
gs = fig.add_gridspec(
    2, 1, height_ratios=[3.6, 1],
    hspace=0,
    left=MARGINS["left"], right=MARGINS["right"],
    top=MARGINS["top"],   bottom=MARGINS["bottom"],
)
ax  = fig.add_subplot(gs[0])
axd = fig.add_subplot(gs[1])

x = np.arange(len(years))

# ── Alt-column background (chart) ────────────────────────────────────────────
for i in range(len(years)):
    if i % 2 == 0:
        ax.axvspan(i-0.5, i+0.5, color=C["bg_alt"], zorder=0, linewidth=0)
        axd.axvspan(i-0.5, i+0.5, color=C["bg_alt"], zorder=0, linewidth=0)

# ── Threshold band (red fill below 35% = danger zone) ────────────────────────
ax.axhspan(0, SP35, color=C["red_lt"], alpha=0.5, zorder=0, linewidth=0)
# ── Amber warning band (35%–37%: technically compliant but dangerously thin) ──
ax.axhspan(SP35, 37, color=C["amber_lt"], alpha=0.7, zorder=0, linewidth=0)

# ── Horizontal grid ───────────────────────────────────────────────────────────
for yv in [10, 20, 30, 40]:
    ax.axhline(yv, color=C["grid"], linewidth=0.8, zorder=1)

# ── Lollipop colour helper ────────────────────────────────────────────────────
def lollipop_col(i, r):
    if i == 7:
        return C["amber"]    # 2025: just scrapes over — warning
    if r >= SP35:
        return C["blue_hi"]  # comfortably above
    return C["blue_lo"]      # below threshold

# ── Lollipop stems ────────────────────────────────────────────────────────────
for i, r in enumerate(ratio):
    ax.plot([i, i], [0, r], color=lollipop_col(i, r),
            linewidth=2.2, zorder=2, solid_capstyle="round")

# ── Lollipop heads ────────────────────────────────────────────────────────────
for i, r in enumerate(ratio):
    col = lollipop_col(i, r)
    ec  = C["amber"] if i == 7 else "white"
    ax.scatter(i, r, s=130, color=col, zorder=4, linewidths=2.0, edgecolors=ec)

# ── Ratio labels ──────────────────────────────────────────────────────────────
for i, r in enumerate(ratio):
    col    = lollipop_col(i, r) if i == 7 else (C["navy"] if r >= SP35 else C["mid"])
    weight = "bold"
    ax.text(i, r + 1.1, f"{r:.1f}%",
            ha="center", va="bottom", fontsize=10.5,
            color=col, fontweight=weight, zorder=5)

# ── S&P threshold line ────────────────────────────────────────────────────────
ax.axhline(SP35, color=C["red"], linewidth=1.3, linestyle=(0,(5,3)), zorder=3)
ax.text(-0.5, SP35 + 0.6, "S&P 35% threshold",
        fontsize=8.5, color=C["red"], ha="left", va="bottom",
        style="italic", fontweight="normal")


# ── Axes ─────────────────────────────────────────────────────────────────────
ax.set_xlim(-0.55, len(years) - 0.35)
ax.set_ylim(0, 47)
ax.set_xticks(x)
ax.set_xticklabels([])
ax.tick_params(axis="both", which="both", length=0)
ax.set_ylabel("Adjusted FFO / debt  (%)", fontsize=10,
              color=C["mid"], labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{v:.0f}%"))
ax.tick_params(axis="y", labelsize=9.5, labelcolor=C["mid"])

# ── Title block ───────────────────────────────────────────────────────────────
fig.text(MARGINS["left"], 0.945,
         "S&P-style adjusted FFO to debt ratio",
         fontsize=14, fontweight="bold", color=C["navy"], ha="left")
fig.text(MARGINS["left"], 0.920,
         "Prysmian Group, 2018–2025  ·  FFO = adjusted EBITDA − paid income taxes − financial charges",
         fontsize=9, color=C["mid"], ha="left")

# ── Thin rule between chart and data strip ────────────────────────────────────
_sep_y = MARGINS["bottom"] + (MARGINS["top"] - MARGINS["bottom"]) / (3.6 + 1)
fig.add_artist(plt.Line2D(
    [MARGINS["left"], MARGINS["right"]],
    [_sep_y, _sep_y],
    transform=fig.transFigure,
    color="#CCCCCC", linewidth=0.8,
))

# ── Data strip ────────────────────────────────────────────────────────────────
LBL_X = -1.55   # row labels sit in a reserved left margin
axd.set_xlim(LBL_X, len(years) - 0.45)
axd.set_ylim(0, 1)
axd.axis("off")

# Years that clear 35% threshold (navy/blue) or just scrape over (amber for 2025)
def data_col(i):
    if i == 7:
        return C["amber"]    # 2025: barely above — amber throughout
    if ratio[i] >= SP35:
        return C["blue_hi"]  # 2022, 2023: comfortably above
    return C["mid"]          # below threshold

def data_fw(i):
    return "bold" if ratio[i] >= SP35 else "normal"

row_defs = [
    (0.80, "Year",             [str(y) for y in years],         C["navy"], 10, "bold"),
    (0.52, "Adj. EBITDA (€m)", [f"{v:,}" for v in ebitda],      C["mid"],   9, "normal"),
    (0.26, "FFO (€m)",         [f"{v:,}" for v in ffo],          C["mid"],   9, "normal"),
    (0.02, "Debt (€m)",        [f"{v:,}" for v in debt],         C["mid"],   9, "normal"),
]

for (ypos, label, vals, default_col, fs, default_fw) in row_defs:
    # Row label — always in its default style
    axd.text(LBL_X + 0.05, ypos, label,
             fontsize=fs - 0.5, color=default_col, fontweight=default_fw,
             va="center", ha="left")
    for i, val in enumerate(vals):
        # Year row: keep navy/bold regardless; all data rows: follow threshold colour
        if label == "Year":
            vc, fw2 = C["navy"], "bold"
        else:
            vc  = data_col(i)
            fw2 = data_fw(i)
        axd.text(i, ypos, val,
                 ha="center", va="center",
                 fontsize=fs, color=vc, fontweight=fw2)

# ── Legend ────────────────────────────────────────────────────────────────────
leg_items = [
    mlines.Line2D([0],[0], marker='o', color='w', markerfacecolor=C["blue_hi"],
                  markersize=8, label="FFO/debt ≥ 35%  (meets S&P threshold)"),
    mlines.Line2D([0],[0], marker='o', color='w', markerfacecolor=C["blue_lo"],
                  markersize=8, label="FFO/debt < 35%"),
]
ax.legend(handles=leg_items, loc="upper left", bbox_to_anchor=(0.0, 1.0),
          fontsize=8.5, frameon=False, labelcolor="#555555",
          handletextpad=0.5, borderpad=0)

# ── Source ────────────────────────────────────────────────────────────────────
fig.text(MARGINS["left"], 0.09,
         "Sources: Prysmian Annual Reports and results presentations, 2018–2025. "
         "Debt = current + non-current financial liabilities.\n"
         "S&P: 'We could lower the rating if adjusted FFO to debt failed to approach 35% by end-2025 and 45% by end-2026.'",
         fontsize=7.8, color=C["note"], ha="left", va="top")

plt.savefig(str(OUT_DIR / "visual_ffo_debt_ratio.png"),
            dpi=DPI, bbox_inches="tight", facecolor="white")
print("Saved.")