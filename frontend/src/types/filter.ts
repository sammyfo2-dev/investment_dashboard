import { WatchlistItem } from './watchlist';
import { StockData } from './stock';

export type SortOption =
  | 'percent-desc'
  | 'percent-asc'
  | 'price-desc'
  | 'price-asc'
  | 'alpha-asc'
  | 'alpha-desc';

export type PerformanceFilter = 'all' | 'gainers' | 'losers';

export interface EnrichedWatchlistItem extends WatchlistItem {
  stockData?: StockData;
  isLoading?: boolean;
  error?: boolean;
}
