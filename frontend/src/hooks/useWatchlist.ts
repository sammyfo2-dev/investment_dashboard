import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { watchlistService } from '@/services/watchlistService';
import { WatchlistCreate } from '@/types/watchlist';

export const useWatchlist = () => {
  const queryClient = useQueryClient();

  const watchlistQuery = useQuery({
    queryKey: ['watchlist'],
    queryFn: watchlistService.getWatchlist,
  });

  const addMutation = useMutation({
    mutationFn: (item: WatchlistCreate) => watchlistService.addToWatchlist(item),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['watchlist'] });
    },
  });

  const removeMutation = useMutation({
    mutationFn: (symbol: string) => watchlistService.removeFromWatchlist(symbol),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['watchlist'] });
    },
  });

  return {
    watchlist: watchlistQuery.data || [],
    isLoading: watchlistQuery.isLoading,
    error: watchlistQuery.error,
    addToWatchlist: addMutation.mutateAsync,
    removeFromWatchlist: removeMutation.mutateAsync,
    isAddingStock: addMutation.isPending,
    isRemovingStock: removeMutation.isPending,
  };
};
