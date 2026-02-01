## Script: demand_supply_charts.R
##
## Loads WEO2023 and World Energy Investment 2023 data and builds
## three main diagrams + one Eurostat renewables diagram.

setwd("C:/Users/krevi/OneDrive/Documents/Diss_Data")

library(tidyverse)
library(readxl)
library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(stringr)
library(purrr)

## Set the scenario of interest.
scenario <- "Stated Policies Scenario"

## ----------------------------------------------------------------------
## Diagram 1 – Global Total Energy Supply vs. Final Consumption

world <- read_csv("WEO2023_AnnexA_Free_Dataset_World.csv",
                  show_col_types = FALSE)

df1 <- world %>%
  filter(
    SCENARIO == scenario,
    CATEGORY == "Energy",
    PRODUCT == "Total",
    REGION == "World",
    FLOW %in% c("Total energy supply", "Total final consumption")
  ) %>%
  select(YEAR, FLOW, VALUE)

p1 <- ggplot(df1, aes(x = YEAR, y = VALUE, colour = FLOW)) +
  geom_line() +
  geom_point() +
  labs(
    x = "Year",
    y = "Energy (EJ)",
    title = paste0("Global Total Energy Supply vs Final Consumption\n", scenario),
    colour = "Flow"
  ) +
  theme_minimal()

ggsave("diagram1_global_supply_demand_R.png", p1, width = 8, height = 5)

## ----------------------------------------------------------------------
## Diagram 2 – Regional Supply and Consumption Comparison

regions <- read_csv("WEO2023_AnnexA_Free_Dataset_Regions.csv",
                    show_col_types = FALSE)

target_regions <- c("United States", "China", "India", "European Union")

df2 <- regions %>%
  filter(
    SCENARIO == scenario,
    CATEGORY == "Energy",
    PRODUCT == "Total",
    REGION %in% target_regions,
    FLOW %in% c("Total energy supply", "Total final consumption")
  ) %>%
  select(REGION, YEAR, FLOW, VALUE)

p2 <- ggplot(df2, aes(x = YEAR, y = VALUE, colour = FLOW)) +
  geom_line() +
  geom_point() +
  facet_wrap(~ REGION, scales = "free_y") +
  labs(
    x = "Year",
    y = "Energy (EJ)",
    title = paste0("Energy Supply vs Final Consumption by Region\n", scenario),
    colour = "Flow"
  ) +
  theme_minimal()

ggsave("diagram2_region_supply_demand_R.png", p2, width = 10, height = 8)

## ----------------------------------------------------------------------
## Diagram 3 – Global Energy Investment Trends

inv_raw <- readxl::read_excel(
  "WorldEnergyInvestment2023_DataFile.xlsx",
  sheet = "World",
  col_names = FALSE
)

# 1) Find row that contains "World" in any column
world_row <- which(
  apply(
    inv_raw,
    1,
    function(row) any(str_trim(as.character(row)) == "World")
  )
)[1]

if (is.na(world_row)) {
  stop("Could not locate any cell with 'World' in the 'World' sheet.")
}

# 2) Find the column where "World" is located on that row
world_col <- which(
  str_trim(as.character(inv_raw[world_row, ])) == "World"
)[1]

if (is.na(world_col)) {
  stop("Logic error: 'World' row found but column not identified.")
}

# 3) Extract years from the cells to the right of "World"
raw_years <- inv_raw[world_row, (world_col + 1):ncol(inv_raw)]
years <- as.numeric(raw_years)

# Keep only columns where years are not NA (avoids blank middle segments)
valid_cols <- which(!is.na(years))
years <- years[valid_cols]

# 4) Helper to convert a data row to long format
row_to_tibble <- function(i) {
  category <- inv_raw[[2]][i]  # category names live in column 2 in this file
  if (is.na(category)) return(NULL)
  
  row_vals <- inv_raw[i, (world_col + 1):ncol(inv_raw)]
  values   <- as.numeric(row_vals[valid_cols])
  
  tibble(
    Category = as.character(category),
    Year     = years,
    Value    = values
  )
}

# 5) Apply to all rows below the 'World' row
long_data <- purrr::map_dfr(
  seq(from = world_row + 1L, to = nrow(inv_raw)),
  row_to_tibble
)

categories_to_plot <- c(
  "Total (billion $2022)",
  "of which: Clean energy",
  "Fossil fuels without CCUS",
  "Renewables",
  "Electricity networks"
)

df3 <- long_data %>%
  filter(Category %in% categories_to_plot) %>%
  filter(!is.na(Value))  # drop any remaining NA values

p3 <- ggplot(df3, aes(x = Year, y = Value, colour = Category)) +
  geom_line() +
  geom_point() +
  labs(
    x = "Year",
    y = "Investment (billion USD 2022)",
    title = "Global Energy Investment by Category",
    colour = "Category"
  ) +
  theme_minimal()

ggsave("diagram3_energy_investment_R.png", p3, width = 9, height = 6)

## ----------------------------------------------------------------------
## Eurostat – Europe’s Energy Mix Shifting Towards Renewables

ren_raw <- read_tsv(
  "estat_nrg_ind_ren.tsv",
  na = ":",      # Eurostat uses ":" for missing
  trim_ws = TRUE
)

names(ren_raw) <- str_trim(names(ren_raw))

ren_long <- ren_raw %>%
  rename(key = 1) %>%  # key column: "freq,nrg_bal,unit,geo\\TIME_PERIOD"
  pivot_longer(
    cols      = -key,
    names_to  = "year",
    values_to = "share_ren"
  ) %>%
  separate(
    key,
    into = c("freq", "nrg_bal", "unit", "geo"),
    sep  = ","
  ) %>%
  mutate(
    year = as.integer(str_trim(year)),
    share_ren = str_replace(share_ren, "\\s.*$", ""),
    share_ren = as.numeric(share_ren)
  )

eu_ren <- ren_long %>%
  filter(
    freq    == "A",
    nrg_bal == "REN",
    unit    == "PC",
    geo     == "EU27_2020"
  ) %>%
  filter(!is.na(share_ren)) %>%   # drop NA rows so no warnings
  arrange(year)

p4 <- ggplot(eu_ren, aes(x = year, y = share_ren)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title    = "Europe’s Energy Mix is Shifting Towards Renewables",
    subtitle = "EU27 share of energy from renewable sources in gross final energy consumption",
    x        = "Year",
    y        = "Renewables share (% of gross final energy consumption)",
    caption  = "Source: Eurostat nrg_ind_ren (EU27_2020, REN, PC)"
  ) +
  theme_minimal(base_size = 12)

ggsave("diagram4_eu_renewables_share_R.png", p4, width = 8, height = 5)

## ----------------------------------------------------------------------
## Display all plots in the active R session

print(p1)
print(p2)
print(p3)
print(p4)
