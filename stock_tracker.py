import streamlit as st
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

# Disabling yfinance cache mechanism
yf.pdr_override(use_cache=False)

# Streamlit Title
st.title("Stock Tracker App")

# Default values
default_start_date = datetime.date.today() - datetime.timedelta(days=365)
default_end_date = datetime.date.today()

# User Inputs
start_date = st.date_input("Start date", default_start_date)
end_date = st.date_input("End date", default_end_date)
stock_symbol = st.text_input("Enter stock symbols (comma separated for multiple):").upper().split(',')
indices = st.multiselect("Compare with:", ["S&P500", "Nasdaq"], default=None)
submit = st.button("Submit")

def plot_stock_data(stock_symbol, start_date, end_date, indices):
    # Fetching the stock data
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)['Close']
    
    # Plotting stock data
    plt.figure(figsize=(12,6))
    plt.plot(stock_data.index, stock_data.values, label=stock_symbol)
    
    # Fetching index data if required
    if "S&P500" in indices:
        sp500 = yf.download('^GSPC', start=start_date, end=end_date)['Close']
        plt.plot(sp500.index, sp500.values, label='S&P500')
    if "Nasdaq" in indices:
        nasdaq = yf.download('^IXIC', start=start_date, end=end_date)['Close']
        plt.plot(nasdaq.index, nasdaq.values, label='Nasdaq')
    
    plt.title(f"{stock_symbol} vs. Selected Indices")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

if submit:
    if stock_symbol:
        for symbol in stock_symbol:
            plot_stock_data(symbol.strip(), start_date, end_date, indices)
    else:
        st.write("Please enter a valid stock symbol.")

