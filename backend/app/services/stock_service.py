import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional
import time
from app.services.crypto_service import CryptoService


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
        """Get current price and basic info (routes crypto to CoinGecko)"""
        # Route crypto symbols to CoinGecko
        if StockService.is_crypto(symbol):
            return CryptoService.get_current_price(symbol)

        # Use Yahoo Finance for stocks
        try:
            # Add delay to avoid rate limiting
            time.sleep(0.5)

            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Get latest price
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            previous_close = info.get('previousClose')

            if not current_price:
                # Fallback to historical data
                hist = ticker.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    if len(hist) > 1:
                        previous_close = hist['Close'].iloc[-2]

            change = None
            change_percent = None
            if current_price and previous_close:
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100

            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'current_price': current_price,
                'change_24h': change,
                'change_24h_percent': change_percent,
            }
        except Exception as e:
            print(f"Error fetching current price for {symbol}: {e}")
            return None

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
        """Fetch name and sector (routes crypto to CoinGecko)"""
        # Route crypto symbols to CoinGecko
        if asset_type.upper() == 'CRYPTO' or StockService.is_crypto(symbol):
            return CryptoService.get_crypto_info(symbol)

        # Use Yahoo Finance for stocks
        try:
            time.sleep(0.5)

            ticker = yf.Ticker(symbol)
            info = ticker.info

            name = info.get('longName') or info.get('shortName') or symbol
            sector = info.get('sector', 'Unknown')

            return {
                'name': name,
                'sector': sector
            }
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {e}")
            # Return default info with Unknown sector if we can't fetch (e.g., rate limited)
            return {
                'name': symbol,
                'sector': 'Unknown'
            }

    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """Check if symbol exists (routes crypto to CoinGecko)"""
        # Route crypto symbols to CoinGecko
        if StockService.is_crypto(symbol):
            return CryptoService.validate_symbol(symbol)

        # Use Yahoo Finance for stocks
        try:
            time.sleep(0.5)
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Check if we got valid data - yfinance returns empty dict for invalid symbols
            return info and len(info) > 1
        except Exception as e:
            error_msg = str(e)
            print(f"Error validating symbol {symbol}: {e}")
            # If rate limited, connection error, or JSON error, assume symbol is valid
            # Only reject if we can confirm it's invalid
            if any(x in error_msg for x in ['429', 'Too Many Requests', 'Expecting value', 'JSONDecodeError']):
                print(f"Rate limited or temporary error - assuming {symbol} is valid")
                return True
            # For other errors, also assume valid to be safe
            return True
