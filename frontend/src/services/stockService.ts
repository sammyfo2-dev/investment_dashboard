import api from './api';
import { StockData, StockChartData } from '@/types/stock';

export const stockService = {
  getStock: async (symbol: string): Promise<StockData> => {
    const response = await api.get(`/api/stocks/${symbol}`);
    return response.data;
  },

  getStockChart: async (symbol: string, days: number = 30): Promise<StockChartData> => {
    const response = await api.get(`/api/stocks/${symbol}/chart`, {
      params: { days },
    });
    return response.data;
  },

  getStockSignals: async (symbol: string) => {
    const response = await api.get(`/api/stocks/${symbol}/signals`);
    return response.data;
  },
};
