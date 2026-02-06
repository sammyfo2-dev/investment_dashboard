import pandas as pd
import numpy as np
from typing import Optional, Dict
from datetime import datetime, timedelta


class TechnicalAnalysisService:
    @staticmethod
    def calculate_moving_averages(df: pd.DataFrame) -> Dict[str, Optional[float]]:
        """
        Calculate moving averages: 50, 100, 150, 200-day, and 200-week
        """
        if df is None or df.empty:
            return {
                'ma_50': None,
                'ma_100': None,
                'ma_150': None,
                'ma_200_day': None,
                'ma_200_week': None,
            }

        close_prices = df['Close']

        result = {}

        # Calculate daily moving averages
        if len(close_prices) >= 50:
            result['ma_50'] = close_prices.rolling(window=50).mean().iloc[-1]
        else:
            result['ma_50'] = None

        if len(close_prices) >= 100:
            result['ma_100'] = close_prices.rolling(window=100).mean().iloc[-1]
        else:
            result['ma_100'] = None

        if len(close_prices) >= 150:
            result['ma_150'] = close_prices.rolling(window=150).mean().iloc[-1]
        else:
            result['ma_150'] = None

        if len(close_prices) >= 200:
            result['ma_200_day'] = close_prices.rolling(window=200).mean().iloc[-1]
        else:
            result['ma_200_day'] = None

        # Calculate 200-week MA (approximately 1000 trading days)
        week_window = 1000
        if len(close_prices) >= week_window:
            result['ma_200_week'] = close_prices.rolling(window=week_window).mean().iloc[-1]
        else:
            result['ma_200_week'] = None

        return result

    @staticmethod
    def get_52_week_range(df: pd.DataFrame, current_price: float) -> Dict[str, Optional[float]]:
        """
        Get 52-week high/low and current position in that range
        """
        if df is None or df.empty:
            return {
                'week_52_high': None,
                'week_52_low': None,
                'current_price': current_price,
                'position_percent': None,
            }

        # Get last 52 weeks (approximately 252 trading days)
        lookback_days = 252
        recent_data = df.tail(lookback_days)

        if recent_data.empty:
            return {
                'week_52_high': None,
                'week_52_low': None,
                'current_price': current_price,
                'position_percent': None,
            }

        week_52_high = recent_data['High'].max()
        week_52_low = recent_data['Low'].min()

        # Calculate position in range (0-100%)
        position_percent = None
        if week_52_high and week_52_low and week_52_high != week_52_low:
            position_percent = ((current_price - week_52_low) / (week_52_high - week_52_low)) * 100

        return {
            'week_52_high': week_52_high,
            'week_52_low': week_52_low,
            'current_price': current_price,
            'position_percent': position_percent,
        }

    @staticmethod
    def get_full_analysis(df: pd.DataFrame, current_price: float) -> dict:
        """
        Get complete technical analysis including MAs and 52-week range
        """
        moving_averages = TechnicalAnalysisService.calculate_moving_averages(df)
        high_low_range = TechnicalAnalysisService.get_52_week_range(df, current_price)

        return {
            'moving_averages': moving_averages,
            'high_low_range': high_low_range,
        }

    @staticmethod
    def calculate_ma_signals(current_price: float, moving_averages: dict) -> dict:
        """
        Calculate signals based on price position relative to MAs
        Returns dict with signal for each MA (above/below) and distance percentage
        """
        signals = {}

        for ma_name, ma_value in moving_averages.items():
            if ma_value is not None and ma_value > 0:
                distance_percent = ((current_price - ma_value) / ma_value) * 100
                signal = 'above' if current_price > ma_value else 'below'

                signals[ma_name] = {
                    'signal': signal,
                    'distance_percent': distance_percent,
                    'ma_value': ma_value,
                }
            else:
                signals[ma_name] = {
                    'signal': 'unknown',
                    'distance_percent': None,
                    'ma_value': None,
                }

        return signals
