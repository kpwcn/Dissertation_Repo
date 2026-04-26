"""
Visual 4: Net Funding Requirement in Context
Prysmian Group, 2024 vs 2025
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
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
FIG_W, FIG_H = 13, 7.5

MARGINS = dict(left=0.07, right=0.97, top=0.90, bottom=0.28)

COLORS = {
    "bar24"    : "#185FA5",   # dark blue  — 2024
    "bar25"    : "#A8CCEE",   # light blue — 2025
    "red"      : "#A0281E",
    "teal"     : "#1D9E75",
    "grid"     : "#E8E8E8",
    "navy"     : "#1a1a1a",
    "axis_text": "#666666",
    "note_text": "#999999",
    "mid"      : "#777777",
}

# ── Data ──────────────────────────────────────────────────────────────────────
metrics = [
    "NFR / net\nfinancial debt",
    "NFR /\nadj. EBITDA",
    "NFR / free\ncash flow",
    "NFR / 2027–2031\nmaturity wall",
]
vals_24 = [30.5, 67.9, 129.5, 25.4]
vals_25 = [30.3, 39.1,  80.1, 18.2]

nfr_24, nfr_25 = 1309, 938
nfd_24, nfd_25 = 4296, 3097
ebi_24, ebi_25 = 1927, 2398
fcf_24, fcf_25 = 1011, 1171
mat            = 5160

denom_labels = [
    f"NFD: €{nfd_24:,}m → €{nfd_25:,}m",
    f"EBITDA: €{ebi_24:,}m → €{ebi_25:,}m",
    f"FCF: €{fcf_24:,}m → €{fcf_25:,}m",
    f"Maturities: €{mat:,}m (2027–31)",
]

Y_MAX   = 150   # shared scale across all panels
YTICKS  = [0, 10, 20, 30, 40, 80, 120]   # dense below 40, sparse above

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

n = len(metrics)
axes = []
for col in range(n):
    ax = fig.add_subplot(1, n, col + 1)
    axes.append(ax)

fig.subplots_adjust(
    left=MARGINS["left"], right=MARGINS["right"],
    top=MARGINS["top"],   bottom=MARGINS["bottom"],
    wspace=0.10,
)

bar_w = 0.34
x24   = 0.5 - bar_w / 2 - 0.04
x25   = 0.5 + bar_w / 2 + 0.04

for col, ax in enumerate(axes):
    v24 = vals_24[col]
    v25 = vals_25[col]

    ax.set_facecolor("white")

    # Grid at each custom tick
    for gv in YTICKS:
        ax.axhline(gv, color=COLORS["grid"], linewidth=0.7, zorder=0)

    # 100% danger line on FCF panel
    if col == 2:
        ax.axhline(100, color=COLORS["red"], linewidth=1.1,
                   linestyle=(0, (4, 3)), zorder=6)

    # Bars
    ax.bar(x24, v24, bar_w, color=COLORS["bar24"], linewidth=0, zorder=3)
    ax.bar(x25, v25, bar_w, color=COLORS["bar25"], linewidth=0, zorder=3)

    # Value labels above bars
    for bx, val, dark in [(x24, v24, True), (x25, v25, False)]:
        ax.text(bx, val + Y_MAX * 0.015,
                f"{val:.1f}%",
                ha="center", va="bottom",
                fontsize=10, color=COLORS["navy"] if dark else COLORS["mid"],
                fontweight="bold" if dark else "normal", zorder=5)

    # Shared axis limits and custom ticks
    ax.set_xlim(0, 1)
    ax.set_ylim(0, Y_MAX)
    ax.set_xticks([])
    ax.set_yticks(YTICKS)
    ax.tick_params(axis="both", which="both", length=0)

    # Y-axis labels only on leftmost panel
    if col == 0:
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
        ax.tick_params(axis="y", labelsize=TICK_SIZE - 1.5, labelcolor=COLORS["axis_text"])
        ax.set_ylabel("Net funding requirement as % of denominator",
                      fontsize=LABEL_SIZE - 2, color=COLORS["axis_text"], labelpad=8)
    else:
        ax.set_yticklabels([])

    # Panel title
    ax.text(0.5, -0.07, metrics[col],
            ha="center", va="top", fontsize=10,
            color=COLORS["navy"], fontweight="bold",
            transform=ax.transAxes, linespacing=1.45)

    # Denominator sub-label
    ax.text(0.5, -0.20, denom_labels[col],
            ha="center", va="top", fontsize=NOTE_SIZE - 0.5,
            color=COLORS["note_text"],
            transform=ax.transAxes, linespacing=1.3)

    # Thin vertical separator between panels
    if col < n - 1:
        lx = ax.get_position().x1 + 0.005
        fig.add_artist(plt.Line2D(
            [lx, lx], [MARGINS["bottom"], MARGINS["top"]],
            transform=fig.transFigure,
            color="#DDDDDD", linewidth=0.7,
        ))

# ── Title & subtitle ──────────────────────────────────────────────────────────
fig.text(MARGINS["left"], 0.975,
         "Net funding requirement in context, 2024–2025",
         fontsize=TITLE_SIZE, fontweight="bold", color=COLORS["navy"],
         ha="left", va="bottom")
fig.text(MARGINS["left"], 0.945,
         f"Prysmian Group  ·  NFR: €{nfr_24:,}m (2024) → €{nfr_25:,}m (2025)  ·  NFR = trade receivables + contract assets + inventories − trade payables − contract liabilities",
         fontsize=LABEL_SIZE - 2.5, color=COLORS["axis_text"],
         ha="left", va="bottom")

# ── Legend ────────────────────────────────────────────────────────────────────
legend_handles = [
    mpatches.Patch(color=COLORS["bar24"], label="2024"),
    mpatches.Patch(color=COLORS["bar25"], label="2025"),
    plt.Line2D([0], [0], color=COLORS["red"], linewidth=1.1,
               linestyle=(0, (4, 3)), label="NFR = FCF (100%)"),
]
fig.legend(
    handles=legend_handles,
    loc="upper right",
    bbox_to_anchor=(MARGINS["right"], 0.978),
    fontsize=LABEL_SIZE - 2,
    frameon=False,
    labelcolor="#444444",
    handlelength=1.2, handleheight=0.9,
    ncol=2, columnspacing=1.0,
)

# ── Source note ───────────────────────────────────────────────────────────────
fig.text(MARGINS["left"], 0.02,
         "Sources: Prysmian Annual Reports 2024–2025. FCF excludes acquisitions and disposals.\n"
         "Maturity wall = 2027–2031 scheduled debt maturities (€5,160m). Net financial debt per Prysmian disclosures.",
         fontsize=NOTE_SIZE, color=COLORS["note_text"], ha="left", va="bottom")

plt.savefig(str(OUT_DIR / "visual_nfr_context.png"),
            dpi=DPI, bbox_inches="tight", facecolor="white")
print("Saved.")
