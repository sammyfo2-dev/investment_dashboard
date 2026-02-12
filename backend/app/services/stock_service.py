import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional
import time
from app.services.crypto_service import CryptoService
from app.services.alphavantage_service import AlphaVantageService


class StockService:
    @staticmethod
    def is_crypto(symbol: str) -> bool:
        """Check if symbol is a cryptocurrency"""
        return symbol.upper().endswith('-USD') and symbol.upper() in CryptoService.SYMBOL_MAP
    @staticmethod
    def get_stock_data(symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch stock data from yfinance
        period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            # Add delay to avoid rate limiting
            time.sleep(0.5)

            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)

            if df.empty:
                return None

            return df
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return None

    @staticmethod
    def get_current_price(symbol: str) -> Optional[dict]:
        """Get current price and basic info (routes crypto to CoinGecko, stocks to Alpha Vantage)"""
        # Route crypto symbols to CoinGecko
        if StockService.is_crypto(symbol):
            return CryptoService.get_current_price(symbol)

        # Use Alpha Vantage for stocks
        return AlphaVantageService.get_current_price(symbol)

    @staticmethod
    def get_stock_history(symbol: str, days: int = 30) -> list[dict]:
        """Get historical prices for charting"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)

            if df.empty:
                return []

            prices = []
            for date, row in df.iterrows():
                prices.append({
                    'date': date.isoformat(),
                    'price': row['Close']
                })

            return prices
        except Exception as e:
            print(f"Error fetching stock history for {symbol}: {e}")
            return []

    @staticmethod
    def get_stock_info(symbol: str, asset_type: str) -> Optional[dict]:
        """Fetch name and sector (routes crypto to CoinGecko, stocks to Alpha Vantage)"""
        # Route crypto symbols to CoinGecko
        if asset_type.upper() == 'CRYPTO' or StockService.is_crypto(symbol):
            return CryptoService.get_crypto_info(symbol)

        # Use Alpha Vantage for stocks
        return AlphaVantageService.get_company_overview(symbol)

    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """Check if symbol exists (routes crypto to CoinGecko, stocks to Alpha Vantage)"""
        # Route crypto symbols to CoinGecko
        if StockService.is_crypto(symbol):
            return CryptoService.validate_symbol(symbol)

        # Use Alpha Vantage for stocks
        return AlphaVantageService.validate_symbol(symbol)
