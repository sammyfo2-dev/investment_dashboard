import api from './api';
import { WatchlistItem, WatchlistCreate, WatchlistUpdate } from '@/types/watchlist';

export const watchlistService = {
  getWatchlist: async (): Promise<WatchlistItem[]> => {
    const response = await api.get('/api/watchlist');
    return response.data;
  },

  addToWatchlist: async (item: WatchlistCreate): Promise<WatchlistItem> => {
    const response = await api.post('/api/watchlist', item);
    return response.data;
  },

  updateWatchlistItem: async (symbol: string, data: WatchlistUpdate): Promise<WatchlistItem> => {
    const response = await api.patch(`/api/watchlist/${symbol}`, data);
    return response.data;
  },

  removeFromWatchlist: async (symbol: string): Promise<void> => {
    await api.delete(`/api/watchlist/${symbol}`);
  },
};
