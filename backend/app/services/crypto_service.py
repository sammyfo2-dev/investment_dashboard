import requests
from typing import Optional
from datetime import datetime, timedelta
import statistics


class CryptoService:
    """Service for fetching cryptocurrency data from CoinGecko API"""

    BASE_URL = "https://api.coingecko.com/api/v3"

    # Map of common crypto symbols to CoinGecko IDs
    SYMBOL_MAP = {
        'BTC-USD': 'bitcoin',
        'ETH-USD': 'ethereum',
        'SOL-USD': 'solana',
        'DOGE-USD': 'dogecoin',
        'ADA-USD': 'cardano',
        'XRP-USD': 'ripple',
        'DOT-USD': 'polkadot',
        'MATIC-USD': 'matic-network',
        'AVAX-USD': 'avalanche-2',
        'LINK-USD': 'chainlink',
    }

    @staticmethod
    def get_coingecko_id(symbol: str) -> Optional[str]:
        """Convert symbol (e.g., BTC-USD) to CoinGecko ID (e.g., bitcoin)"""
        return CryptoService.SYMBOL_MAP.get(symbol.upper())

    @staticmethod
    def get_current_price(symbol: str) -> Optional[dict]:
        """Get current crypto price and 24h change from CoinGecko"""
        try:
            coin_id = CryptoService.get_coingecko_id(symbol)
            if not coin_id:
                print(f"Unknown crypto symbol: {symbol}")
                return None

            # Fetch data from CoinGecko
            url = f"{CryptoService.BASE_URL}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false',
                'sparkline': 'false'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract price data
            market_data = data.get('market_data', {})
            current_price = market_data.get('current_price', {}).get('usd')
            price_change_24h = market_data.get('price_change_24h')
            price_change_percentage_24h = market_data.get('price_change_percentage_24h')

            if not current_price:
                return None

            return {
                'symbol': symbol,
                'name': data.get('name', symbol),
                'current_price': current_price,
                'change_24h': price_change_24h,
                'change_24h_percent': price_change_percentage_24h,
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching crypto data for {symbol}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching crypto data for {symbol}: {e}")
            return None

    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """Check if crypto symbol is supported"""
        return symbol.upper() in CryptoService.SYMBOL_MAP

    @staticmethod
    def get_historical_data(symbol: str, days: int = 365) -> Optional[list]:
        """Get historical price data from CoinGecko"""
        try:
            coin_id = CryptoService.get_coingecko_id(symbol)
            if not coin_id:
                return None

            url = f"{CryptoService.BASE_URL}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract prices [timestamp, price]
            prices = data.get('prices', [])
            return [{'timestamp': p[0], 'price': p[1]} for p in prices]

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

        # Extract just the price values
        price_values = [p['price'] for p in prices]

        def calc_ma(days):
            if len(price_values) >= days:
                return statistics.mean(price_values[-days:])
            return None

        # Calculate moving averages
        ma_50 = calc_ma(50)
        ma_100 = calc_ma(100)
        ma_150 = calc_ma(150)
        ma_200_day = calc_ma(200)

        # 200-week MA = 200 weeks * 7 days = 1400 days (approx)
        # But we only have 365 days, so use 52 weeks = 364 days
        ma_200_week = calc_ma(min(364, len(price_values)))

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
        if not prices or len(prices) < 365:
            return {
                'week_52_high': None,
                'week_52_low': None,
                'current_price': current_price,
                'position_percent': None,
            }

        # Get last 365 days of prices
        recent_prices = [p['price'] for p in prices[-365:]]

        week_52_high = max(recent_prices)
        week_52_low = min(recent_prices)

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
    def get_crypto_info(symbol: str) -> dict:
        """Get basic crypto info (name)"""
        coin_id = CryptoService.get_coingecko_id(symbol)
        if not coin_id:
            return {'name': symbol, 'sector': 'Cryptocurrency'}

        try:
            url = f"{CryptoService.BASE_URL}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'false',
                'community_data': 'false',
                'developer_data': 'false'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                'name': data.get('name', symbol),
                'sector': 'Cryptocurrency'
            }
        except Exception as e:
            print(f"Error fetching crypto info for {symbol}: {e}")
            return {'name': symbol, 'sector': 'Cryptocurrency'}
