import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# =============================================================================
# CONFIGURE
# =============================================================================
OUT_DIR = Path(".")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# DATA
# =============================================================================
years = [2020, 2021, 2022, 2023, 2024]
backlog = [3.5, 4.4, 6.4, 18.0, 17.0]  # in € Billions

# =============================================================================
# FIGURE SETUP
# =============================================================================
fig, ax = plt.subplots(figsize=(9, 5.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# =============================================================================
# COLOR SCHEME
# =============================================================================
bar_color = '#2171b5'
highlight_color = '#0d4a70'

# Highlight 2023 peak
colors = [bar_color if y != 2023 else highlight_color for y in years]

# =============================================================================
# PLOT BARS
# =============================================================================
bars = ax.bar(years, backlog, color=colors, width=0.6, edgecolor='none')

# =============================================================================
# VALUE LABELS
# =============================================================================
for year, val in zip(years, backlog):
    ax.text(year, val + 0.4, f'€{val:.1f}B', ha='center', va='bottom', 
            fontsize=10.5, fontweight='bold', color='#222222')

# =============================================================================
# MINIMAL ANNOTATIONS - only 2 key callouts
# =============================================================================
# 2020 baseline
ax.annotate('Pre-acceleration\nbaseline',
            xy=(2020, 3.5), xytext=(2020, 8.5),
            fontsize=8, color='#666666', ha='center',
            arrowprops=dict(arrowstyle='-', color='#aaaaaa', lw=0.7))

# 2023 record - positioned cleanly
ax.annotate('Record: Amprion\n& EGL2 awards',
            xy=(2023, 18.0), xytext=(2023, 21.5),
            fontsize=8, color='#666666', ha='center',
            arrowprops=dict(arrowstyle='-', color='#aaaaaa', lw=0.7))

# =============================================================================
# CAGR BOX
# =============================================================================
cagr = ((backlog[-1] / backlog[0]) ** (1/4) - 1) * 100
ax.text(0.97, 0.92, f'CAGR: {cagr:.0f}%', transform=ax.transAxes,
        ha='right', va='top', fontsize=9.5, color='#2171b5', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#f0f7fc', 
                  edgecolor='#2171b5', linewidth=1))

# =============================================================================
# FORMATTING
# =============================================================================
# Title (centered, consistent size)
ax.text(0.5, 1.12, 'Prysmian Projects Backlog', transform=ax.transAxes,
        fontsize=14, fontweight='bold', color='#1a1a1a', ha='center')
ax.text(0.5, 1.04, 'Year-end order book value, € Billions', transform=ax.transAxes,
        fontsize=9.5, color='#666666', ha='center')

# Y-axis
ax.set_ylim(0, 24)
ax.set_yticks([0, 5, 10, 15, 20])
ax.set_yticklabels(['0', '5', '10', '15', '20'], fontsize=9, color='#555555')
ax.set_ylabel('')

# X-axis
ax.set_xticks(years)
ax.set_xticklabels(years, fontsize=10, fontweight='medium', color='#333333')
ax.set_xlim(2019.3, 2024.7)

# Grid - subtle horizontal only
ax.yaxis.grid(True, linestyle='-', alpha=0.25, color='#cccccc', zorder=0)
ax.set_axisbelow(True)

# Spines - minimal
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#888888')
ax.spines['left'].set_linewidth(0.6)
ax.spines['bottom'].set_color('#888888')
ax.spines['bottom'].set_linewidth(0.6)

ax.tick_params(axis='x', length=0, pad=6)
ax.tick_params(axis='y', length=0, pad=4)

# =============================================================================
# LEGEND - compact
# =============================================================================
legend_elements = [
    mpatches.Patch(facecolor=bar_color, label='Backlog'),
    mpatches.Patch(facecolor=highlight_color, label='Peak'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=8, frameon=False,
          ncol=2, columnspacing=1, handlelength=1.2, handleheight=0.8)

# =============================================================================
# SOURCE
# =============================================================================
fig.text(0.5, 0.01, 'Source: Prysmian Group Annual Reports & Investor Presentations',
         ha='center', fontsize=7.5, style='italic', color='#999999',
         transform=fig.transFigure)

# =============================================================================
# SAVE
# =============================================================================
plt.tight_layout()
plt.subplots_adjust(top=0.85, bottom=0.1)

output_path = OUT_DIR / 'prysmian_backlog_chart_final.png'
plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()

print(f"Chart saved to: {output_path}")

# =============================================================================
# CSV DATA
# =============================================================================
import csv

notes = [
    'Baseline level prior to offshore wind and grid interconnection acceleration',
    'All-time record at the time; €4.8B in new project awards during year',
    'Significant jump driven by surge in global energy transition projects',
    'Record high due to Amprion and EGL2 mega-project awards',
    'Remained robust following high execution of existing 2023 orders'
]

with open(OUT_DIR / 'prysmian_backlog_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Year', 'Backlog_EUR_Billions', 'YoY_Growth_Pct', 'Notes'])
    for i, (y, b, n) in enumerate(zip(years, backlog, notes)):
        yoy = ((b / backlog[i-1]) - 1) * 100 if i > 0 else None
        writer.writerow([y, b, f'{yoy:.1f}' if yoy else 'N/A', n])

print("CSV saved to:", OUT_DIR / 'prysmian_backlog_data.csv')