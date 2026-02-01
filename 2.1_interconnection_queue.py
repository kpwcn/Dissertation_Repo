import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------
# 0) Configure
# ----------------------------
OUT_DIR = Path(".")  # change to your local folder if you want
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# 1) US chart – active queue capacity by technology group (2014–2024)
#    Source sheet: "07. Active Capacity by Type"
# ----------------------------
us_path = Path("lbnl_ix_queue_data_file_thru2024_v2.xlsx")
raw = pd.read_excel(us_path, sheet_name="07. Active Capacity by Type")

# Table starts at row 24 (0-index 23) in this workbook version
t = raw.iloc[23:].copy()
t.columns = ["Type", "Year", "Configuration", "Capacity_GW"]
t = t[t["Type"].astype(str) != "Type"]

t["Year"] = pd.to_numeric(t["Year"], errors="coerce")
t["Capacity_GW"] = pd.to_numeric(t["Capacity_GW"], errors="coerce")
t = t.dropna(subset=["Year", "Capacity_GW", "Type"])
t["Year"] = t["Year"].astype(int)

def group_type(x: str) -> str:
    if x == "Solar":
        return "Solar"
    if x in ["Wind", "Offshore Wind"]:
        return "Wind"
    if x == "Storage":
        return "Storage"
    if x == "Gas":
        return "Natural gas"
    return "Other (coal+nuclear+other)"

t["Type_grouped"] = t["Type"].map(group_type)

g = (
    t.groupby(["Year", "Type_grouped"], as_index=False)["Capacity_GW"]
    .sum()
)

pivot = (
    g.pivot_table(index="Year", columns="Type_grouped", values="Capacity_GW", aggfunc="sum")
    .fillna(0)
)
pivot["Total"] = pivot.sum(axis=1)

stack_cols = ["Solar", "Wind", "Storage", "Natural gas", "Other (coal+nuclear+other)"]
colors = {
    "Solar": "#69F0AE",
    "Wind": "#4CAF50",
    "Storage": "#3F7CCF",
    "Natural gas": "#FFF176",
    "Other (coal+nuclear+other)": "#E0E0E0"
}
stack_colors = [colors[c] for c in stack_cols]
pivot = pivot.sort_index()

fig, ax = plt.subplots(figsize=(12, 7))
years = pivot.index.values

ax.stackplot(years, [pivot[c].values for c in stack_cols], colors=stack_colors, labels=stack_cols)
ax.plot(years, pivot["Total"].values, linewidth=1.5, color="black", label="Total")

ax.set_title("U.S. active interconnection queue capacity (2014–2024)\nby technology group (GW)", fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Capacity (GW)")
ax.grid(True, axis="y", alpha=0.25)

ax.legend(loc="upper left", frameon=True, fontsize=9)
ax.text(0, -0.08, "Notes: Values from US (Berkeley Lab) – Interconnection queue data through end-2024 (XLSX).",
        ha="left", va="top", fontsize=9, color="#666666", transform=ax.transAxes)

fig.tight_layout()
fig.savefig(OUT_DIR / "figure_us_interconnection_queues_2014_2024.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("Done. Chart saved to:", OUT_DIR.resolve())
