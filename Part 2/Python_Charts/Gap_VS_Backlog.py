"""
Visual 3 (revised): Gross Project Cash Tie-Up vs Transmission Backlog, 2018–2025
Prysmian Group Dissertation — Working Capital Analysis

Gross tie-up = trade receivables + contract assets + inventories (no offsets).
Rationale: the backlog story is about cash committed before receipts arrive;
gross tie-up is the more direct measure of that pre-receipt burden.

Base year: 2020 = 100 (post-Covid anchor).

FONT SETUP (local use):
    Times New Roman is standard on Windows/macOS.
    On Linux: sudo apt install ttf-mscorefonts-installer && fc-cache -f
    Ensure FONT = "Times New Roman" below.
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

MARGINS = dict(left=0.08, right=0.97, top=0.90, bottom=0.18)

COLORS = {
    "backlog"    : "#185FA5",
    "gross"      : "#1D9E75",
    "fill_b"     : "#185FA5",
    "fill_g"     : "#1D9E75",
    "ref_line"   : "#AAAAAA",
    "break_band" : "#F5F5F0",
    "grid"       : "#E8E8E8",
    "axis_text"  : "#666666",
    "note_text"  : "#999999",
    "annot_bg"   : "#FFFFFF",
    "crossover"  : "#E8A020",
}

# ── Data ──────────────────────────────────────────────────────────────────────
years           = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
trade_rec       = [1635, 1475, 1374, 1622, 1942, 1987, 2433, 2428]
contract_assets = [ 362,  450,  162,  247,  503,  485,  554,  567]
inventories     = [1515, 1523, 1531, 2054, 2241, 2264, 2858, 3066]

# Backlog: 2018–2022 Projects perimeter; 2023+ Transmission segment
backlog_raw = [1.90, 2.04, 3.50, 4.40, 6.60, 10.70, 18.00, 17.00]  # €bn

gross_raw = [
    trade_rec[i] + contract_assets[i] + inventories[i]
    for i in range(len(years))
]  # €m: 3512, 3448, 3067, 3923, 4686, 4736, 5845, 6061

BASE = 2  # 2020
base_g = gross_raw[BASE]
base_b = backlog_raw[BASE]

gross_idx   = [v / base_g * 100 for v in gross_raw]
backlog_idx = [v / base_b * 100 for v in backlog_raw]

# ─────────────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family"       : FONT,
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "axes.spines.left"  : False,
    "axes.spines.bottom": False,
    "xtick.bottom"      : False,
    "ytick.left"        : False,
})

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
fig.subplots_adjust(**MARGINS)

x = np.arange(len(years))

# ── Perimeter-break band (2022→2023 boundary) ─────────────────────────────────
ax.axvspan(4.5, 5.5, color=COLORS["break_band"], linewidth=0, zorder=0, alpha=0.85)
ax.axvline(5, color="#CCCCCC", linewidth=0.8, linestyle=":", zorder=1)
ax.text(
    5.0, 492, "Perimeter\nbreak",
    fontsize=NOTE_SIZE - 0.5, color="#AAAAAA",
    ha="center", va="top", linespacing=1.4, style="italic",
)

# ── Reference line at 100 ─────────────────────────────────────────────────────
ax.axhline(100, color=COLORS["ref_line"], linewidth=0.9, linestyle="--", zorder=2)
ax.text(-0.42, 102, "2020 = 100",
        fontsize=NOTE_SIZE, color=COLORS["ref_line"], ha="left", va="bottom")

# ── Crossover annotation (~2021–2022) ─────────────────────────────────────────
# Series nearly converge at 2021 (125.7 vs 127.9) then diverge sharply
ax.annotate(
    "Series converge\n2021",
    xy=(3, 126.8), xytext=(2.35, 168),
    fontsize=NOTE_SIZE, color=COLORS["crossover"], ha="center",
    arrowprops=dict(arrowstyle="-|>", color=COLORS["crossover"],
                    lw=0.9, mutation_scale=8),
    bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS["annot_bg"],
              edgecolor=COLORS["crossover"], linewidth=0.7, alpha=0.95),
    zorder=6,
)

# ── Fill between the two lines to show the divergence region ─────────────────
# Shade where backlog > gross (backlog running ahead)
ax.fill_between(
    x, backlog_idx, gross_idx,
    where=[backlog_idx[i] >= gross_idx[i] for i in range(len(x))],
    alpha=0.06, color=COLORS["fill_b"], linewidth=0, zorder=1,
    interpolate=True,
)
# Shade where gross > backlog (pre-2020: cash burden ahead of pipeline)
ax.fill_between(
    x, gross_idx, backlog_idx,
    where=[gross_idx[i] > backlog_idx[i] for i in range(len(x))],
    alpha=0.08, color=COLORS["fill_g"], linewidth=0, zorder=1,
    interpolate=True,
)

# ── Lines ─────────────────────────────────────────────────────────────────────
line_b, = ax.plot(
    x, backlog_idx,
    color=COLORS["backlog"], linewidth=2.4, zorder=4,
    marker="s", markersize=5.5, linestyle="--",
    markerfacecolor=COLORS["backlog"],
    markeredgecolor="white", markeredgewidth=1.5,
    label="Transmission backlog  (2020 = 100)",
)
line_g, = ax.plot(
    x, gross_idx,
    color=COLORS["gross"], linewidth=2.4, zorder=4,
    marker="o", markersize=6,
    markerfacecolor=COLORS["gross"],
    markeredgecolor="white", markeredgewidth=1.5,
    label="Gross cash tie-up: receivables + contract assets + inventories  (2020 = 100)",
)

# ── Divergence bracket (2024) ─────────────────────────────────────────────────
xi = 6  # 2024
b_val = backlog_idx[xi]
g_val = gross_idx[xi]
mid   = (b_val + g_val) / 2

ax.annotate(
    "", xy=(xi + 0.18, b_val), xytext=(xi + 0.18, g_val),
    arrowprops=dict(arrowstyle="<->", color="#888888", lw=1.0,
                    shrinkA=3, shrinkB=3),
    zorder=5,
)
ax.text(
    xi + 0.32, mid,
    f"+{b_val - g_val:.0f}pt\ngap",
    fontsize=NOTE_SIZE, color="#888888",
    ha="left", va="center", linespacing=1.4,
)

# ── End-point labels (2025) ───────────────────────────────────────────────────
for yi, color, dy, lbl in [
    (backlog_idx[7], COLORS["backlog"],  12, f"{backlog_idx[7]:.0f}  (€17bn)"),
    (gross_idx[7],   COLORS["gross"],   -12, f"{gross_idx[7]:.0f}"),
]:
    ax.annotate(
        lbl,
        xy=(7, yi), xytext=(7.12, yi + dy),
        fontsize=TICK_SIZE - 1, color=color, ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=COLORS["annot_bg"],
                  edgecolor=color, linewidth=0.7, alpha=0.95),
        zorder=6,
    )


# ── Grid ──────────────────────────────────────────────────────────────────────
ax.yaxis.grid(True, color=COLORS["grid"], linewidth=0.7, zorder=0)
ax.set_axisbelow(True)

# ── Axes ──────────────────────────────────────────────────────────────────────
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=TICK_SIZE, color=COLORS["axis_text"])
ax.tick_params(axis="both", which="both", length=0)
ax.set_xlim(-0.5, len(years) - 0.3)
ax.set_ylim(0, 540)

ax.set_ylabel("Index  (2020 = 100)", fontsize=LABEL_SIZE,
              color=COLORS["axis_text"], labelpad=10)
ax.tick_params(axis="y", labelsize=TICK_SIZE, labelcolor=COLORS["axis_text"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}"))

# ── Title & subtitle ──────────────────────────────────────────────────────────
fig.text(
    MARGINS["left"], 0.975,
    "Gross project cash tie-up vs transmission backlog, 2018–2025",
    fontsize=TITLE_SIZE, fontweight="bold", color="#1a1a1a", ha="left", va="bottom",
)
fig.text(
    MARGINS["left"], 0.945,
    "Indexed, 2020 = 100  ·  Prysmian Group  ·  gross tie-up = receivables + contract assets + inventories",
    fontsize=LABEL_SIZE - 1, color=COLORS["axis_text"], ha="left", va="bottom",
)

# ── Legend ────────────────────────────────────────────────────────────────────
ax.legend(
    handles=[line_b, line_g],
    loc="upper left", bbox_to_anchor=(0.01, 0.97),
    fontsize=LABEL_SIZE - 1, frameon=True, framealpha=0.92,
    edgecolor="#DDDDDD", fancybox=False,
    labelcolor="#444444", handlelength=1.8,
)

# ── Source note ───────────────────────────────────────────────────────────────
fig.text(
    MARGINS["left"], 0.13,
    "Sources: Prysmian Annual Reports 2018–2025; FY results presentations. "
    "2018–2022 backlog under former Projects perimeter; 2023 onward under Transmission segment.\n"
    "Gross tie-up excludes trade payables and contract liabilities.",
    fontsize=NOTE_SIZE, color=COLORS["note_text"], ha="left", va="top",
)

plt.savefig(
    str(OUT_DIR / "visual_3_indexed_trend.png"),
    dpi=DPI, bbox_inches="tight", facecolor="white",
)
print("Saved.")