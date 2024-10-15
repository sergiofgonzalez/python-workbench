import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the stock tickers
tickers = ['NVDA', 'TSLA']

# Define the start and end dates
start_date = '2024-01-01'
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

# Fetch the stock data
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# Calculate the returns
returns = data.pct_change().dropna()

# Calculate cumulative returns
cumulative_returns = (1 + returns).cumprod() - 1

# Plot the cumulative returns
plt.figure(figsize=(10, 6))
for ticker in tickers:
    plt.plot(cumulative_returns.index, cumulative_returns[ticker], label=ticker)

plt.title('NVIDIA vs TSLA Stock Returns YTD')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.grid(True)
plt.savefig('nvidia_vs_tsla_returns_ytd.png')