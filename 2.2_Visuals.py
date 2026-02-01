import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

# ----------------------------
# 0) Paths
# ----------------------------
DATA_PATH = Path("WorldEnergyInvestment2025_DataFile.xlsx")  # change to your local path
OUT_DIR = Path(".")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# 1) Load "World" sheet and build a label->value lookup for 2025
# ----------------------------
world = pd.read_excel(DATA_PATH, sheet_name="World", header=None)

years = world.iloc[1, 2:13].astype(int).tolist()  # 2015..2025
labels = world.iloc[:, 1].astype(str).str.strip()
values = world.iloc[:, 2:13]
tidy = pd.DataFrame(values.values, columns=years)
tidy.insert(0, "label", labels)
tidy = tidy[tidy["label"].ne("nan")]

def val(label: str) -> float:
    s = tidy.loc[tidy["label"] == label, 2025]
    if s.empty:
        s = tidy.loc[tidy["label"].str.lower() == label.lower(), 2025]
    return float(s.iloc[0])

# Pull components (World, 2025)
renewables = val("Renewables")
end_use = val("End-use")
electricity_networks = val("Electricity networks")
battery_storage = val("Battery storage")
nuclear = val("Nuclear")

clean_fuels = val("Clean Fuels")
direct_air_capture = val("Direct Air Capture")
fossil_power_ccus = val("Fossil fuels: with CCUS")
other_clean_power = val("Other clean power")
large_scale_heat_pumps = val("o/w Large scale heat pumps")

oil_supply = val("Oil")
gas_supply = val("Gas")
coal_supply = val("Coal")
coal_unabated_power = val("Coal (unabated)")
oil_gas_unabated_power = val("Oil and natural gas (unabated)")

# Build the exact buckets used in the treemap
clean = {
    "Renewable power": renewables,
    "Energy efficiency and end-use": end_use,
    "Grids and storage": electricity_networks + battery_storage,
    "Nuclear": nuclear,
    "LEF": clean_fuels + direct_air_capture + fossil_power_ccus + other_clean_power + large_scale_heat_pumps,
}

fossil = {
    "Oil": oil_supply,
    "Natural gas": gas_supply + oil_gas_unabated_power,
    "Coal": coal_supply + coal_unabated_power,
}

df = pd.DataFrame(
    [{"group": "Clean energy", "sub_sector": k, "investment_billion_usd_2024MER": v, "year": 2025} for k, v in clean.items()]
    + [{"group": "Fossil fuels", "sub_sector": k, "investment_billion_usd_2024MER": v, "year": 2025} for k, v in fossil.items()]
)

df.to_csv(OUT_DIR / "wei2025_breakdown_clean_vs_fossil_2025_world.csv", index=False)

# ----------------------------
# 2) Treemap drawing (manual layout to match IEA-style diagram)
# ----------------------------
def draw_rect(ax, x, y, w, h, color, title, value):
    rect = Rectangle((x, y), w, h, facecolor=color, edgecolor="white", linewidth=2)
    ax.add_patch(rect)
    pad = 0.01
    ax.text(
        x + pad * w,
        y + h - pad * h,
        f"{title}\nUSD\n{int(round(value))} billion",
        va="top",
        ha="left",
        fontsize=10,
        color="black",
        wrap=True,
    )

colors_clean = {
    "Renewable power": "#69F0AE",
    "Energy efficiency and end-use": "#4FC3F7",
    "Grids and storage": "#3F7CCF",
    "Nuclear": "#B388FF",
    "LEF": "#00BFA5",
}
colors_fossil = {
    "Oil": "#FFB74D",
    "Natural gas": "#FFF176",
    "Coal": "#E0E0E0",
}

C = sum(clean.values())
F = sum(fossil.values())
T = C + F

w_clean = C / T
gap = 0.02

fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Outer boxes
x_clean = 0.0
x_foss = w_clean + gap
cw = w_clean - gap / 2
fw = 1.0 - x_foss

ax.text(x_clean + cw / 2, 1.02, "Clean energy", ha="center", va="bottom", fontsize=12, fontweight="bold")
ax.text(x_foss + fw / 2, 1.02, "Fossil fuels", ha="center", va="bottom", fontsize=12, fontweight="bold")

# Clean layout (match your example)
R = clean["Renewable power"]
E = clean["Energy efficiency and end-use"]
G = clean["Grids and storage"]
N = clean["Nuclear"]
L = clean["LEF"]

# Renewable power left column
w_R = cw * (R / C)
draw_rect(ax, x_clean, 0, w_R, 1, colors_clean["Renewable power"], "Renewable power", R)

# Right region for E (top) and G/N/L (bottom)
rx, rw = x_clean + w_R, cw - w_R
B = G + N + L
h_E = 1.0 * (E / (E + B))
draw_rect(ax, rx, 1 - h_E, rw, h_E, colors_clean["Energy efficiency and end-use"], "Energy efficiency and end-use", E)

# Bottom region split: G left, N+L right strip; N on top of L
bh = 1 - h_E
S = N + L
w_G = rw * (G / (G + S))
draw_rect(ax, rx, 0, w_G, bh, colors_clean["Grids and storage"], "Grids and storage", G)

sx, sw = rx + w_G, rw - w_G
h_N = bh * (N / (N + L))
draw_rect(ax, sx, bh - h_N, sw, h_N, colors_clean["Nuclear"], "Nuclear", N)
draw_rect(ax, sx, 0, sw, bh - h_N, colors_clean["LEF"], "LEF", L)

# Fossil layout (oil left, gas top-right, coal bottom-right)
O = fossil["Oil"]
NG = fossil["Natural gas"]
CO = fossil["Coal"]

w_O = fw * (O / F)
draw_rect(ax, x_foss, 0, w_O, 1, colors_fossil["Oil"], "Oil", O)

frx, frw = x_foss + w_O, fw - w_O
h_NG = 1.0 * (NG / (NG + CO))
draw_rect(ax, frx, 1 - h_NG, frw, h_NG, colors_fossil["Natural gas"], "Natural gas", NG)
draw_rect(ax, frx, 0, frw, 1 - h_NG, colors_fossil["Coal"], "Coal", CO)

# Titles
fig.suptitle("Breakdown of clean energy and fossil fuel investment by sub-sector, 2025",
             fontsize=16, fontweight="bold", y=1.08)
ax.text(0, 1.05, "billion USD (MER, 2024)", ha="left", va="bottom", fontsize=11, color="#555555")
ax.text(0, -0.05, "Notes: LEF = low-emission fuels. Values from IEA World Energy Investment 2025 datafile (World sheet, 2025 column).",
        ha="left", va="top", fontsize=9, color="#666666")

fig.savefig(OUT_DIR / "figure_wei2025_clean_vs_fossil_treemap_2025_world.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("Saved:",
      OUT_DIR / "figure_wei2025_clean_vs_fossil_treemap_2025_world.png",
      OUT_DIR / "wei2025_breakdown_clean_vs_fossil_2025_world.csv")
