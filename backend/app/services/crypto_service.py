import requests
from typing import Optional
from datetime import datetime


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
