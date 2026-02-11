import { WatchlistItem } from '../types/watchlist';
import { EnrichedWatchlistItem, SortOption, PerformanceFilter } from '../types/filter';

/**
 * Filter watchlist items by search term (symbol or name)
 */
export const filterBySearch = (
  items: WatchlistItem[],
  searchTerm: string
): WatchlistItem[] => {
  if (!searchTerm.trim()) return items;

  const term = searchTerm.toLowerCase().trim();
  return items.filter(
    (item) =>
      item.symbol.toLowerCase().includes(term) ||
      item.name.toLowerCase().includes(term)
  );
};

/**
 * Filter watchlist items by selected sectors
 */
export const filterBySector = (
  items: WatchlistItem[],
  selectedSectors: string[]
): WatchlistItem[] => {
  if (selectedSectors.length === 0) return items;

  return items.filter((item) => {
    const sector = item.sector || 'Unknown';
    return selectedSectors.includes(sector);
  });
};

/**
 * Filter enriched watchlist items by performance (gainers/losers)
 */
export const filterByPerformance = (
  items: EnrichedWatchlistItem[],
  filter: PerformanceFilter
): EnrichedWatchlistItem[] => {
  if (filter === 'all') return items;

  return items.filter((item) => {
    const changePercent = item.stockData?.change_24h_percent;
    if (changePercent === null || changePercent === undefined) return false;

    if (filter === 'gainers') {
      return changePercent > 0;
    } else if (filter === 'losers') {
      return changePercent < 0;
    }
    return true;
  });
};

/**
 * Sort enriched watchlist items by the specified option
 */
export const sortWatchlist = (
  items: EnrichedWatchlistItem[],
  sortBy: SortOption
): EnrichedWatchlistItem[] => {
  const sorted = [...items];

  switch (sortBy) {
    case 'percent-desc':
      return sorted.sort((a, b) => {
        const aPercent = a.stockData?.change_24h_percent ?? -Infinity;
        const bPercent = b.stockData?.change_24h_percent ?? -Infinity;
        return bPercent - aPercent;
      });

    case 'percent-asc':
      return sorted.sort((a, b) => {
        const aPercent = a.stockData?.change_24h_percent ?? Infinity;
        const bPercent = b.stockData?.change_24h_percent ?? Infinity;
        return aPercent - bPercent;
      });

    case 'price-desc':
      return sorted.sort((a, b) => {
        const aPrice = a.stockData?.current_price ?? -Infinity;
        const bPrice = b.stockData?.current_price ?? -Infinity;
        return bPrice - aPrice;
      });

    case 'price-asc':
      return sorted.sort((a, b) => {
        const aPrice = a.stockData?.current_price ?? Infinity;
        const bPrice = b.stockData?.current_price ?? Infinity;
        return aPrice - bPrice;
      });

    case 'alpha-asc':
      return sorted.sort((a, b) => a.symbol.localeCompare(b.symbol));

    case 'alpha-desc':
      return sorted.sort((a, b) => b.symbol.localeCompare(a.symbol));

    default:
      return sorted;
  }
};
