# electricity-price-render

Automatically create electricity price diagrams for East Denmark in DKK/kWh for each day [here](./daily_prices)

- Uses this python project to look up the prices: https://github.com/kipe/nordpool
- Uses matplotlib to render a diagram.
- Uses GitHub Actions to run once an hour (but only uploads when there is new data).


Used in my ![electricity price widget](https://github.com/mathiastj/electricity-price-widget). 
