"""
Visual 2 (revised): Net Funding-Gap Proxy and Funding-Gap Days, 2018–2025
Prysmian Group Dissertation — Working Capital Analysis

Formula (revised):
    FGD days = 365 × ( TR/Rev + CA/Rev + Inv/COGS − TP/COGS − CL/Rev )

    TR, CA, CL denominated by revenue (revenue-cycle items).
    Inventories and trade payables denominated by COGS (cost-cycle items).

All income statement figures in EUR from Prysmian platform (EUR), converted
from €000s to €m. Balance-sheet series unchanged (previously verified EUR).

FONT SETUP (local use):
    Times New Roman is standard on Windows/macOS.
    On Linux: sudo apt install ttf-mscorefonts-installer && fc-cache -f
    Set FONT = "Times New Roman" below.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
OUT_DIR = HERE / "pngs"
OUT_DIR.mkdir(exist_ok=True)

# ── Shared style constants (identical across all visuals) ─────────────────────
FONT        = "Times New Roman"
TITLE_SIZE  = 14.5
LABEL_SIZE  = 11.5
TICK_SIZE   = 10
NOTE_SIZE   = 8.5
DPI         = 300
FIG_W, FIG_H = 11, 7.5

MARGINS = dict(left=0.08, right=0.92, top=0.90, bottom=0.18)

COLORS = {
    "net_gap"   : "#1D9E75",
    "fgd_days"  : "#185FA5",
    "fill_gap"  : "#1D9E75",
    "fill_days" : "#185FA5",
    "grid"      : "#E8E8E8",
    "axis_text" : "#666666",
    "note_text" : "#999999",
    "annot_bg"  : "#FFFFFF",
}

# ── Data ──────────────────────────────────────────────────────────────────────
years           = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

# Balance-sheet series (€m) — Prysmian Annual Reports 2018–2025
trade_rec       = [1635, 1475, 1374, 1622, 1942, 1987, 2433, 2428]
contract_assets = [ 362,  450,  162,  247,  503,  485,  554,  567]
inventories     = [1515, 1523, 1531, 2054, 2241, 2264, 2858, 3066]
trade_pay       = [2132, 2062, 1958, 2592, 2718, 2199, 2462, 2798]
contract_lib    = [ 223,  298,  368,  454,  825, 1627, 2074, 2325]

# Income statement (€m, EUR) — platform figures in €000s converted to €m
revenue_eur = [10104, 11519, 10016, 12736, 16067, 15354, 17026, 19650]
cogs_eur    = [6626,   7234,  6395,  8677, 10618,  9653, 10740, 12145]

# ── Derived series ────────────────────────────────────────────────────────────
net_gap = [
    trade_rec[i] + contract_assets[i] + inventories[i]
    - trade_pay[i] - contract_lib[i]
    for i in range(len(years))
]
# €m: 1157, 1088, 741, 877, 1143, 910, 1309, 938

fgd_days = [
    365 * (
          trade_rec[i]       / revenue_eur[i]
        + contract_assets[i] / revenue_eur[i]
        + inventories[i]     / cogs_eur[i]
        - trade_pay[i]       / cogs_eur[i]
        - contract_lib[i]    / revenue_eur[i]
    )
    for i in range(len(years))
]
# days: 30.1, 24.4, 18.2, 17.9, 20.4, 22.5, 33.0, 20.5

# ─────────────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family"       : FONT,
    "axes.spines.top"   : False,
    "axes.spines.left"  : False,
    "xtick.bottom"      : False,
    "ytick.left"        : False,
    "ytick.right"       : False,
})

fig, ax1 = plt.subplots(figsize=(FIG_W, FIG_H))
fig.subplots_adjust(**MARGINS)
ax2 = ax1.twinx()

x = np.arange(len(years))

# ── Fill under lines ──────────────────────────────────────────────────────────
ax1.fill_between(x, net_gap,  alpha=0.10, color=COLORS["fill_gap"],  linewidth=0, zorder=1)
ax2.fill_between(x, fgd_days, alpha=0.09, color=COLORS["fill_days"], linewidth=0, zorder=1)

# ── Lines ─────────────────────────────────────────────────────────────────────
line1, = ax1.plot(
    x, net_gap, color=COLORS["net_gap"], linewidth=2.4, zorder=4,
    marker="o", markersize=6,
    markerfacecolor=COLORS["net_gap"], markeredgecolor="white", markeredgewidth=1.5,
    label="Net funding requirement (€m)",
)
line2, = ax2.plot(
    x, fgd_days, color=COLORS["fgd_days"], linewidth=2.4, zorder=4,
    marker="s", markersize=5.5, linestyle="--",
    markerfacecolor=COLORS["fgd_days"], markeredgecolor="white", markeredgewidth=1.5,
    label="Funding-gap days",
)

# ── Annotations: 2021 trough and 2024 peak ────────────────────────────────────
def annot(ax, xi, yi, label, color, xytext):
    ax.annotate(
        label, xy=(xi, yi), xytext=xytext,
        fontsize=TICK_SIZE - 1, color=color, ha="center",
        arrowprops=dict(arrowstyle="-", color=color, lw=0.8),
        bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS["annot_bg"],
                  edgecolor=color, linewidth=0.7, alpha=0.95),
        zorder=6,
    )

# €m trough (2020) and peak (2024)
annot(ax1, 2, net_gap[2],  f"€{net_gap[2]:,}m\n(trough)", COLORS["net_gap"],  (2,  net_gap[2] - 175))
annot(ax1, 6, net_gap[6],  f"€{net_gap[6]:,}m\n(peak)",   COLORS["net_gap"],  (6,  net_gap[6] + 115))

# days trough (2021) and peak (2024)
annot(ax2, 3, fgd_days[3], f"{fgd_days[3]:.1f}d\n(trough)", COLORS["fgd_days"], (3,    fgd_days[3] - 3.5))
annot(ax2, 6, fgd_days[6], f"{fgd_days[6]:.1f}d\n(peak)",   COLORS["fgd_days"], (6.75, fgd_days[6] + 1.8))

# ── Grid and spines ───────────────────────────────────────────────────────────
ax1.yaxis.grid(True, color=COLORS["grid"], linewidth=0.7, zorder=0)
ax1.set_axisbelow(True)
ax1.spines["right"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["right"].set_color("#DDDDDD")
ax2.spines["right"].set_linewidth(0.6)

# ── X-axis ────────────────────────────────────────────────────────────────────
ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=TICK_SIZE, color=COLORS["axis_text"])
ax1.tick_params(axis="both", which="both", length=0)
ax2.tick_params(axis="both", which="both", length=0)
ax1.set_xlim(-0.45, len(years) - 0.55)

# ── Y-axis left (€m) ──────────────────────────────────────────────────────────
ax1.set_ylabel("Net funding requirement  (€m)", fontsize=LABEL_SIZE,
               color=COLORS["net_gap"], labelpad=10)
ax1.tick_params(axis="y", labelsize=TICK_SIZE, labelcolor=COLORS["net_gap"])
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"€{int(v):,}m"))
ax1.set_ylim(400, 1600)

# ── Y-axis right (days) ───────────────────────────────────────────────────────
ax2.set_ylabel("Funding-gap days", fontsize=LABEL_SIZE,
               color=COLORS["fgd_days"], labelpad=10, rotation=270, va="bottom")
ax2.tick_params(axis="y", labelsize=TICK_SIZE, labelcolor=COLORS["fgd_days"])
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}d"))
ax2.set_ylim(8, 45)

# ── Title & subtitle ─────────────────────────────────────────────────────────
fig.text(
    MARGINS["left"], 0.975,
    "Net funding requirement and funding-gap days, 2018–2025",
    fontsize=TITLE_SIZE, fontweight="bold", color="#1a1a1a", ha="left", va="bottom",
)
fig.text(
    MARGINS["left"], 0.945,
    "Prysmian Group  ·  left axis: €m  ·  right axis: days",
    fontsize=LABEL_SIZE - 1, color=COLORS["axis_text"], ha="left", va="bottom",
)

# ── Legend ────────────────────────────────────────────────────────────────────
ax1.legend(
    handles=[line1, line2],
    loc="upper left", bbox_to_anchor=(0.01, 0.97),
    fontsize=LABEL_SIZE - 1, frameon=True, framealpha=0.92,
    edgecolor="#DDDDDD", fancybox=False,
    labelcolor="#444444", handlelength=1.8,
)

# ── Source note ───────────────────────────────────────────────────────────────
fig.text(
    MARGINS["left"], 0.13,
    "Sources: Prysmian Annual Reports 2018–2025 (balance-sheet); income statement in EUR from LSEG & Pitchbook.\n"
    "FGD formula: 365 × (TR/Rev + CA/Rev + Inv/COGS − TP/COGS − CL/Rev). TR, CA, CL use revenue; Inv and TP use COGS.",
    fontsize=NOTE_SIZE, color=COLORS["note_text"], ha="left", va="top",
)

plt.savefig(
    str(OUT_DIR / "visual_2_funding_gap_trend.png"),
    dpi=DPI, bbox_inches="tight", facecolor="white",
)
print("Saved.")