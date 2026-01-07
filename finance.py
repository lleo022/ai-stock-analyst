import yfinance as yf
import re

def get_stock_data(ticker_symbol):
    """Fetches key metrics from Yahoo Finance."""
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    
    data_summary = {
        "name": info.get("longName"),
        "current_price": info.get("currentPrice"),
        "pe_ratio": info.get("forwardPE"),
        "market_cap": info.get("marketCap"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "analyst_recommendation": info.get("recommendationKey"),
    }
    return data_summary

def valid_ticker(ticker):
    if not valid_format(ticker):
        return False, "Invalid format. Tickers should be 1-5 uppercase letters."
    if not ticker_exists(ticker):
        return False, "Ticker not found on Yahoo Finance."
    return True, "Valid"

def valid_format(ticker_name):
    # checks if string is in proper format (1-5 uppercase letters)
    # allows dots or hyphens 
    pattern = r'^[A-Z]{1,5}([.\-][A-Z]{1,2})?$'
    return bool(re.match(pattern, ticker_name))

def ticker_exists(ticker_name):
    # checks for a ticker's history in the past day
    ticker = yf.Ticker(ticker_name)
    hist = ticker.history(period="1d")
    return not hist.empty