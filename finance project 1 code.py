import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- STEP 1: FETCH DATA (Day 1) ---
def fetch_stock_data(ticker, period="5y"):
    """
    Fetches historical stock data for a given ticker.
    """
    print(f"Fetching data for {ticker}...")
    # 'auto_adjust=True' fixes historical splits/dividends for accurate analysis
    df = yf.download(ticker, period=period, auto_adjust=True)
    
    # Ensure data is sorted by date
    df = df.sort_index()
    return df

# --- STEP 2: QUANT LOGIC (Day 2) ---
def calculate_signals(df):
    """
    Calculates 50-day and 200-day Moving Averages and generates Buy/Sell signals.
    """
    # Calculate Moving Averages (The "Strategy")
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    # Define Signal Logic:
    # 1. Buy when 50 crosses ABOVE 200
    # 2. Sell when 50 crosses BELOW 200
    df['Signal'] = 0  # Default to 0
    
    # We use a trick here: Set signal to 1 where 50 > 200, else 0
    df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1
    
    # Calculate 'Position' to identify the exact day of crossover
    # diff() checks the difference from the previous row. 
    # +1 means it went from 0 to 1 (Buy), -1 means 1 to 0 (Sell)
    df['Position'] = df['Signal'].diff()
    
    return df

# --- VISUALIZATION (To verify logic) ---
def plot_strategy(df, ticker):
    plt.figure(figsize=(14, 7))
    
    # Plot Close Price, SMA 50, and SMA 200
    plt.plot(df['Close'], label='Close Price', alpha=0.5)
    plt.plot(df['SMA_50'], label='50-Day SMA', color='orange', linestyle='--')
    plt.plot(df['SMA_200'], label='200-Day SMA', color='blue', linestyle='--')

    # Plot Buy Signals (Green Triangle Up)
    plt.plot(df[df['Position'] == 1].index, 
             df['SMA_50'][df['Position'] == 1], 
             '^', markersize=10, color='green', lw=0, label='Buy Signal')

    # Plot Sell Signals (Red Triangle Down)
    plt.plot(df[df['Position'] == -1].index, 
             df['SMA_50'][df['Position'] == -1], 
             'v', markersize=10, color='red', lw=0, label='Sell Signal')

    plt.title(f'{ticker} - Golden Cross Strategy Analysis')
    plt.legend()
    plt.grid()
    plt.show()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # DBS Ticker on Singapore Exchange is D05.SI
    ticker_symbol = "D05.SI" 
    
    # Run the pipeline
    stock_data = fetch_stock_data(ticker_symbol)
    analyzed_data = calculate_signals(stock_data)
    
    # Show last 5 rows to check the math
    print("\nLatest Data Points:")
    print(analyzed_data[['Close', 'SMA_50', 'SMA_200', 'Signal', 'Position']].tail())

    # Visualize
    plot_strategy(analyzed_data, ticker_symbol)