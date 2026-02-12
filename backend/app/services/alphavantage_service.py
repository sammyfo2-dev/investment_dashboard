import requests
import os
from typing import Optional
from datetime import datetime
import statistics


class AlphaVantageService:
    """Service for fetching stock data from Alpha Vantage API"""

    BASE_URL = "https://www.alphavantage.co/query"
    API_KEY = os.getenv('ALPHAVANTAGE_API_KEY', 'demo')  # 'demo' for testing

    @staticmethod
    def get_current_price(symbol: str) -> Optional[dict]:
        """Get current stock price and daily change from Alpha Vantage"""
        try:
            # Use GLOBAL_QUOTE endpoint for current price
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': AlphaVantageService.API_KEY
            }

            response = requests.get(AlphaVantageService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Check for API limit or error
            if 'Note' in data:
                print(f"Alpha Vantage API limit reached: {data['Note']}")
                return None

            if 'Error Message' in data:
                print(f"Alpha Vantage error for {symbol}: {data['Error Message']}")
                return None

            quote = data.get('Global Quote', {})
            if not quote:
                return None

            current_price = float(quote.get('05. price', 0))
            previous_close = float(quote.get('08. previous close', 0))
            change = float(quote.get('09. change', 0))
            change_percent = float(quote.get('10. change percent', '0').replace('%', ''))

            if not current_price:
                return None

            return {
                'symbol': symbol,
                'name': symbol,  # Alpha Vantage doesn't provide name in GLOBAL_QUOTE
                'current_price': current_price,
                'change_24h': change,
                'change_24h_percent': change_percent,
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Alpha Vantage data for {symbol}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching Alpha Vantage data for {symbol}: {e}")
            return None

    @staticmethod
    def get_historical_data(symbol: str, outputsize: str = 'full') -> Optional[list]:
        """Get daily historical data from Alpha Vantage"""
        try:
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'outputsize': outputsize,  # 'compact' = 100 days, 'full' = 20+ years
                'apikey': AlphaVantageService.API_KEY
            }

            response = requests.get(AlphaVantageService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Check for API limit or error
            if 'Note' in data:
                print(f"Alpha Vantage API limit reached: {data['Note']}")
                return None

            if 'Error Message' in data:
                print(f"Alpha Vantage error for {symbol}: {data['Error Message']}")
                return None

            time_series = data.get('Time Series (Daily)', {})
            if not time_series:
                return None

            # Convert to list of dicts sorted by date
            prices = []
            for date_str, values in sorted(time_series.items()):
                prices.append({
                    'date': date_str,
                    'close': float(values.get('4. close', 0)),
                    'high': float(values.get('2. high', 0)),
                    'low': float(values.get('3. low', 0)),
                })

            return prices

        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None

    @staticmethod
    def calculate_moving_averages(prices: list, current_price: float) -> dict:
        """Calculate moving averages from historical price data"""
        if not prices or len(prices) < 50:
            return {
                'ma_50': None,
                'ma_100': None,
                'ma_150': None,
                'ma_200_day': None,
                'ma_200_week': None,
            }

        # Extract just the closing price values (most recent last)
        close_prices = [p['close'] for p in prices]

        def calc_ma(days):
            if len(close_prices) >= days:
                return statistics.mean(close_prices[-days:])
            return None

        # Calculate moving averages
        ma_50 = calc_ma(50)
        ma_100 = calc_ma(100)
        ma_150 = calc_ma(150)
        ma_200_day = calc_ma(200)

        # 200-week MA = 200 weeks * 5 trading days = 1000 days
        ma_200_week = calc_ma(min(1000, len(close_prices)))

        return {
            'ma_50': ma_50,
            'ma_100': ma_100,
            'ma_150': ma_150,
            'ma_200_day': ma_200_day,
            'ma_200_week': ma_200_week,
        }

    @staticmethod
    def calculate_52week_range(prices: list, current_price: float) -> dict:
        """Calculate 52-week high/low from historical data"""
        # 52 weeks * 5 trading days = 260 trading days
        if not prices or len(prices) < 260:
            return {
                'week_52_high': None,
                'week_52_low': None,
                'current_price': current_price,
                'position_percent': None,
            }

        # Get last 260 trading days
        recent_prices = prices[-260:]
        highs = [p['high'] for p in recent_prices]
        lows = [p['low'] for p in recent_prices]

        week_52_high = max(highs)
        week_52_low = min(lows)

        # Calculate position percentage
        price_range = week_52_high - week_52_low
        if price_range > 0:
            position_percent = ((current_price - week_52_low) / price_range) * 100
        else:
            position_percent = 50.0

        return {
            'week_52_high': week_52_high,
            'week_52_low': week_52_low,
            'current_price': current_price,
            'position_percent': position_percent,
        }

    @staticmethod
    def get_company_overview(symbol: str) -> dict:
        """Get company name and sector from Alpha Vantage"""
        try:
            params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': AlphaVantageService.API_KEY
            }

            response = requests.get(AlphaVantageService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'Note' in data or 'Error Message' in data:
                return {'name': symbol, 'sector': 'Unknown'}

            return {
                'name': data.get('Name', symbol),
                'sector': data.get('Sector', 'Unknown')
            }

        except Exception as e:
            print(f"Error fetching company overview for {symbol}: {e}")
            return {'name': symbol, 'sector': 'Unknown'}

    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """Check if stock symbol exists"""
        # Try to get quote - if it returns data, symbol is valid
        data = AlphaVantageService.get_current_price(symbol)
        return data is not None
