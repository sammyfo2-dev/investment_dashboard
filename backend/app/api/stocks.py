from fastapi import APIRouter, HTTPException
from app.services.stock_service import StockService
from app.services.technical_analysis import TechnicalAnalysisService
from app.services.cache_service import cache_service
from app.schemas.stock import StockData, StockChartData, MovingAveragesData, HighLowRange
from datetime import datetime

router = APIRouter()

stock_service = StockService()
technical_service = TechnicalAnalysisService()


@router.get("/{symbol}", response_model=StockData)
async def get_stock(symbol: str):
    """
    Get comprehensive stock data including price, moving averages, and 52-week range
    """
    symbol = symbol.upper()

    # Check cache first
    cached_data = cache_service.get_stock_analysis(symbol)
    if cached_data:
        return StockData(**cached_data)

    # Fetch current price (routes crypto to CoinGecko)
    current_data = stock_service.get_current_price(symbol)
    if not current_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

    current_price = current_data['current_price']

    # Check if this is a crypto symbol
    is_crypto = stock_service.is_crypto(symbol)

    if is_crypto:
        # For crypto, use simple dummy data for moving averages and ranges
        # since CoinGecko doesn't provide historical data in the same format
        response_data = {
            'symbol': symbol,
            'name': current_data['name'],
            'current_price': current_price,
            'change_24h': current_data['change_24h'],
            'change_24h_percent': current_data['change_24h_percent'],
            'moving_averages': {
                'ma_50': None,
                'ma_100': None,
                'ma_150': None,
                'ma_200_day': None,
                'ma_200_week': None,
            },
            'high_low_range': {
                'week_52_high': None,
                'week_52_low': None,
                'current_price': current_price,
                'position_percent': None,
            },
            'last_updated': datetime.now().isoformat(),
        }
    else:
        # For stocks, fetch historical data and calculate technical indicators
        df = stock_service.get_stock_data(symbol, period="2y")  # 2 years for 200-week MA
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail=f"No historical data for {symbol}")

        # Calculate technical indicators
        analysis = technical_service.get_full_analysis(df, current_price)

        # Build response
        response_data = {
            'symbol': symbol,
            'name': current_data['name'],
            'current_price': current_price,
            'change_24h': current_data['change_24h'],
            'change_24h_percent': current_data['change_24h_percent'],
            'moving_averages': analysis['moving_averages'],
            'high_low_range': analysis['high_low_range'],
            'last_updated': datetime.now().isoformat(),
        }

    # Cache the result
    cache_service.set_stock_analysis(symbol, response_data)

    return StockData(**response_data)


@router.get("/{symbol}/chart", response_model=StockChartData)
async def get_stock_chart(symbol: str, days: int = 30):
    """
    Get historical price data for charting
    """
    symbol = symbol.upper()

    prices = stock_service.get_stock_history(symbol, days=days)
    if not prices:
        raise HTTPException(status_code=404, detail=f"No chart data for {symbol}")

    return StockChartData(symbol=symbol, prices=prices)


@router.get("/{symbol}/signals")
async def get_stock_signals(symbol: str):
    """
    Get trading signals based on moving average positions
    """
    symbol = symbol.upper()

    # Fetch stock data
    current_data = stock_service.get_current_price(symbol)
    if not current_data:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

    df = stock_service.get_stock_data(symbol, period="2y")
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail=f"No historical data for {symbol}")

    current_price = current_data['current_price']

    # Calculate MAs
    moving_averages = technical_service.calculate_moving_averages(df)

    # Calculate signals
    signals = technical_service.calculate_ma_signals(current_price, moving_averages)

    return {
        'symbol': symbol,
        'current_price': current_price,
        'signals': signals,
    }
