import api from './api';
import { WatchlistItem, WatchlistCreate } from '@/types/watchlist';

export const watchlistService = {
  getWatchlist: async (): Promise<WatchlistItem[]> => {
    const response = await api.get('/api/watchlist');
    return response.data;
  },

  addToWatchlist: async (item: WatchlistCreate): Promise<WatchlistItem> => {
    const response = await api.post('/api/watchlist', item);
    return response.data;
  },

  removeFromWatchlist: async (symbol: string): Promise<void> => {
    await api.delete(`/api/watchlist/${symbol}`);
  },
};
