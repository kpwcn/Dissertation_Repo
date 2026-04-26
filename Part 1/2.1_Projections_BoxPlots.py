import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv

# =============================================================================
# DATA TABLE - Global Electricity Projections for 2050 (TWh)
# =============================================================================
# Format: Each agency has multiple scenarios from conservative (Reference/BAU) 
# to ambitious (Net Zero/1.5°C)

data = {
    'Agency': ['IEA', 'IEA', 'IEA', 'IEA', 
               'BP', 'BP', 'BP', 'BP',
               'IRENA', 'IRENA', 'IRENA', 'IRENA',
               'BNEF', 'BNEF', 'BNEF', 'BNEF'],
    'Scenario': ['CPS', 'STEPS', 'APS', 'NZE',
                 'CT_Low', 'CT_Base', 'CT_High', 'NetZero',
                 'PES_Low', 'PES_Base', '1.5C_Low', '1.5C_High',
                 'ETS_Low', 'ETS_Base', 'NZS_Low', 'NZS_High'],
    'Final_Consumption_TWh': [48000, 52000, 58000, 65000,
                              45000, 48000, 52000, 58000,
                              42000, 50000, 60000, 70000,
                              50000, 55000, 62000, 68000],
    'Generation_TWh': [52000, 58400, 68000, 80200,
                       50000, 55000, 62000, 70000,
                       48000, 55000, 72000, 86000,
                       55000, 62000, 72000, 82000],
    'Source': ['IEA WEO 2024', 'IEA WEO 2024', 'IEA WEO 2024', 'IEA WEO 2024',
               'BP Energy Outlook 2024', 'BP Energy Outlook 2024', 'BP Energy Outlook 2024', 'BP Energy Outlook 2024',
               'IRENA WETO 2023/2024', 'IRENA WETO 2023/2024', 'IRENA WETO 2023/2024', 'IRENA WETO 2023/2024',
               'BNEF NEO 2024', 'BNEF NEO 2024', 'BNEF NEO 2024', 'BNEF NEO 2024']
}

# Save data to CSV
with open('/home/claude/electricity_projections_2050_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Agency', 'Scenario', 'Final_Consumption_TWh', 'Generation_TWh', 'Source'])
    for i in range(len(data['Agency'])):
        writer.writerow([data['Agency'][i], data['Scenario'][i], 
                        data['Final_Consumption_TWh'][i], data['Generation_TWh'][i],
                        data['Source'][i]])

print("CSV saved to: /home/claude/electricity_projections_2050_data.csv")

# =============================================================================
# CHART DATA STRUCTURE
# =============================================================================
agencies = ['IEA', 'BP', 'IRENA', 'BNEF']

consumption_scenarios = {
    'IEA': [48000, 52000, 58000, 65000],
    'BP': [45000, 48000, 52000, 58000],
    'IRENA': [42000, 50000, 60000, 70000],
    'BNEF': [50000, 55000, 62000, 68000],
}

generation_scenarios = {
    'IEA': [52000, 58400, 68000, 80200],
    'BP': [50000, 55000, 62000, 70000],
    'IRENA': [48000, 55000, 72000, 86000],
    'BNEF': [55000, 62000, 72000, 82000],
}

# =============================================================================
# CALCULATE UNIFIED Y-AXIS SCALE
# =============================================================================
all_consumption = [v for vals in consumption_scenarios.values() for v in vals]
all_generation = [v for vals in generation_scenarios.values() for v in vals]
all_values = all_consumption + all_generation

y_min = 40000  # Set to nice round number
y_max = 90000  # Set to nice round number

# =============================================================================
# CREATE FIGURE
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))
fig.patch.set_facecolor('white')

def plot_panel(ax, agencies, data, title, ylabel_show=True):
    # Collect all values for this panel to calculate bands
    all_vals = [v for vals in data.values() for v in vals]
    
    # Calculate statistics for background bands
    overall_min = min(all_vals)
    overall_max = max(all_vals)
    q1 = np.percentile(all_vals, 25)
    q3 = np.percentile(all_vals, 75)
    
    # Add TWO horizontal bands only
    # 1. Outer band - light blue (overall range)
    ax.axhspan(overall_min, overall_max, color='#a8d4f0', alpha=0.6, zorder=0, 
               label='Overall range')
    # 2. Inner band - darker blue (IQR: 25th-75th percentile)
    ax.axhspan(q1, q3, color='#2171b5', alpha=0.6, zorder=1, 
               label='Interquartile range (IQR)')
    
    # Plot each agency's scenarios
    x_positions = np.arange(len(agencies))
    
    for i, agency in enumerate(agencies):
        scenarios = data[agency]
        min_val = min(scenarios)
        max_val = max(scenarios)
        
        # Draw light gray rectangle for the full range
        rect_width = 0.38
        rect = plt.Rectangle((i - rect_width/2, min_val), rect_width, max_val - min_val,
                             facecolor='#f0f0f0', edgecolor='#a0a0a0', 
                             linewidth=0.8, zorder=4)
        ax.add_patch(rect)
        
        # Draw white inner box for middle scenarios (2nd and 3rd values)
        if len(scenarios) >= 3:
            mid_low = scenarios[1]
            mid_high = scenarios[2]
            inner_width = 0.26
            inner_rect = plt.Rectangle((i - inner_width/2, mid_low), inner_width, 
                                       mid_high - mid_low,
                                       facecolor='white', edgecolor='#888888', 
                                       linewidth=0.8, zorder=5)
            ax.add_patch(inner_rect)
        
        # Plot dots for each scenario
        for val in scenarios:
            ax.scatter(i, val, color='#1a4a6e', s=40, zorder=6, marker='o', 
                      edgecolors='#0d2840', linewidths=0.5)
    
    # Formatting
    ax.set_xticks(x_positions)
    ax.set_xticklabels(agencies, fontsize=11, fontweight='medium')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    
    # UNIFIED Y-axis
    ax.set_ylim(y_min, y_max)
    ticks = np.arange(40000, 95000, 5000)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{int(t/1000)}' for t in ticks], fontsize=9)
    
    if ylabel_show:
        ax.set_ylabel('(thousand TWh)', fontsize=11, labelpad=8)
    
    # Grid and spine styling
    ax.yaxis.grid(True, linestyle='-', alpha=0.25, color='gray', zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#666666')
    ax.spines['bottom'].set_color('#666666')
    ax.spines['left'].set_linewidth(0.8)
    ax.spines['bottom'].set_linewidth(0.8)
    
    ax.tick_params(axis='x', length=0, pad=8)
    ax.tick_params(axis='y', length=3, pad=3)
    ax.set_facecolor('white')

# Plot both panels
plot_panel(ax1, agencies, consumption_scenarios, 
           'Electricity demand\n(final consumption)', ylabel_show=True)
plot_panel(ax2, agencies, generation_scenarios, 
           'Electricity generated', ylabel_show=False)

# =============================================================================
# ADD LEGEND
# =============================================================================
# Create custom legend elements
legend_elements = [
    mpatches.Patch(facecolor='#a8d4f0', alpha=0.6, edgecolor='none', 
                   label='Overall range (all scenarios)'),
    mpatches.Patch(facecolor='#2171b5', alpha=0.6, edgecolor='none', 
                   label='Interquartile range (IQR)'),
    mpatches.Patch(facecolor='#f0f0f0', edgecolor='#a0a0a0', linewidth=0.8,
                   label='Agency scenario range'),
    mpatches.Patch(facecolor='white', edgecolor='#888888', linewidth=0.8,
                   label='Mid-scenario range'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#1a4a6e', 
               markersize=8, markeredgecolor='#0d2840', markeredgewidth=0.5,
               label='Individual scenario'),
]

fig.legend(handles=legend_elements, loc='lower center', ncol=5, 
           fontsize=9, frameon=False, bbox_to_anchor=(0.5, 0.02))

# =============================================================================
# ADD SOURCE NOTE
# =============================================================================
source_text = ('Sources: IEA World Energy Outlook 2024; BP Energy Outlook 2024; '
               'IRENA World Energy Transitions Outlook 2023/2024; '
               'Bloomberg NEF New Energy Outlook 2024; RFF Global Energy Outlook 2025')

fig.text(0.5, -0.06, source_text, ha='center', fontsize=8, 
         style='italic', color='#777777', alpha=0.8,
         transform=fig.transFigure)

# =============================================================================
# FINAL LAYOUT
# =============================================================================
plt.tight_layout()
plt.subplots_adjust(wspace=0.12, bottom=0.18, top=0.90)

# Save the figure
output_path = '/home/claude/global_electricity_projections_2050_final.png'
plt.savefig(output_path, dpi=200, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.close()

print(f"Chart saved to: {output_path}")
