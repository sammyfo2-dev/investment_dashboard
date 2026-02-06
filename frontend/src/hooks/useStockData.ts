import { useQuery } from '@tanstack/react-query';
import { stockService } from '@/services/stockService';

export const useStockData = (symbol: string) => {
  return useQuery({
    queryKey: ['stock', symbol],
    queryFn: () => stockService.getStock(symbol),
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
    staleTime: 2 * 60 * 1000, // Consider data stale after 2 minutes
  });
};

export const useStockChart = (symbol: string, days: number = 30) => {
  return useQuery({
    queryKey: ['stockChart', symbol, days],
    queryFn: () => stockService.getStockChart(symbol, days),
    staleTime: 5 * 60 * 1000,
  });
};
