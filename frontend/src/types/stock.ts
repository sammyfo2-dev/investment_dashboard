export interface MovingAveragesData {
  ma_50: number | null;
  ma_100: number | null;
  ma_150: number | null;
  ma_200_day: number | null;
  ma_200_week: number | null;
}

export interface HighLowRange {
  week_52_high: number | null;
  week_52_low: number | null;
  current_price: number;
  position_percent: number | null;
}

export interface StockData {
  symbol: string;
  name: string;
  current_price: number;
  change_24h: number | null;
  change_24h_percent: number | null;
  moving_averages: MovingAveragesData;
  high_low_range: HighLowRange;
  last_updated: string;
}

export interface PricePoint {
  date: string;
  price: number;
}

export interface StockChartData {
  symbol: string;
  prices: PricePoint[];
}
