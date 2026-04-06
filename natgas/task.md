# Natural Gas Price Estimation

## Data
Monthly natural gas price snapshots from a market data provider, representing the market price of natural gas delivered at the end of each calendar month. The dataset covers 31st October 2020 to 30th September 2024 (48 observations).

## Objective
Build a model that takes a date as input and returns an estimated purchase price of natural gas. The model should:

1. Estimate prices for any date within the historical range
2. Extrapolate prices for one additional year beyond the dataset (to September 2025)

## Considerations
- Look for seasonal trends (e.g. monthly/yearly cycles) that affect pricing
- Market holidays, weekends, and bank holidays need not be accounted for