import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { MovingAverageIndicator } from './MovingAverageIndicator';
import { HighLowRangeBar } from './HighLowRangeBar';
import { EditStockDialog } from './EditStockDialog';
import { useStockData } from '@/hooks/useStockData';
import { useWatchlist } from '@/hooks/useWatchlist';
import { formatCurrency, formatPercent } from '@/lib/utils';
import { TrendingUp, TrendingDown, X, Pencil } from 'lucide-react';

interface PriceCardProps {
  symbol: string;
  name: string;
}

export const PriceCard: React.FC<PriceCardProps> = ({ symbol, name }) => {
  const { data, isLoading, error } = useStockData(symbol);
  const { removeFromWatchlist, watchlist } = useWatchlist();
  const [isRemoving, setIsRemoving] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);

  // Get current watchlist item for editing
  const watchlistItem = watchlist.find((item) => item.symbol === symbol);

  const handleRemove = async () => {
    if (
      window.confirm(`Remove ${symbol} from watchlist?`)
    ) {
      setIsRemoving(true);
      try {
        await removeFromWatchlist(symbol);
      } catch (err) {
        alert('Failed to remove stock. Please try again.');
        setIsRemoving(false);
      }
    }
  };

  if (isLoading) {
    return (
      <Card className="h-full">
        <CardContent className="flex items-center justify-center h-48">
          <div className="text-muted-foreground">Loading {symbol}...</div>
        </CardContent>
      </Card>
    );
  }

  if (error || !data) {
    return (
      <Card className="h-full border-red-200">
        <CardContent className="flex items-center justify-center h-48">
          <div className="text-red-500">Error loading {symbol}</div>
        </CardContent>
      </Card>
    );
  }

  const isPositive = (data.change_24h_percent || 0) >= 0;

  return (
    <Card className="h-full hover:shadow-lg transition-shadow relative">
      {/* Action buttons */}
      <div className="absolute top-2 right-2 flex gap-1">
        <button
          onClick={() => setIsEditDialogOpen(true)}
          className="p-1 rounded-full hover:bg-blue-100 dark:hover:bg-blue-900 text-gray-400 hover:text-blue-600 transition-colors"
          aria-label="Edit stock"
        >
          <Pencil className="w-4 h-4" />
        </button>
        <button
          onClick={handleRemove}
          disabled={isRemoving}
          className="p-1 rounded-full hover:bg-red-100 dark:hover:bg-red-900 text-gray-400 hover:text-red-600 transition-colors disabled:opacity-50"
          aria-label="Remove from watchlist"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <CardHeader className="pb-3">
        <div className="flex justify-between items-start pr-6">
          <div>
            <CardTitle className="text-lg font-bold">{symbol}</CardTitle>
            <p className="text-sm text-muted-foreground">{name}</p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold">
              {formatCurrency(data.current_price)}
            </div>
            {data.change_24h_percent !== null && (
              <div
                className={`flex items-center gap-1 text-sm font-medium ${
                  isPositive ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {isPositive ? (
                  <TrendingUp className="w-4 h-4" />
                ) : (
                  <TrendingDown className="w-4 h-4" />
                )}
                {formatPercent(data.change_24h_percent)}
              </div>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* 52-Week Range */}
        <HighLowRangeBar range={data.high_low_range} />

        {/* Moving Averages */}
        <div className="space-y-1 border-t pt-3">
          <div className="text-sm font-semibold mb-2">Moving Averages</div>
          <MovingAverageIndicator
            label="50-Day"
            maValue={data.moving_averages.ma_50}
            currentPrice={data.current_price}
          />
          <MovingAverageIndicator
            label="100-Day"
            maValue={data.moving_averages.ma_100}
            currentPrice={data.current_price}
          />
          <MovingAverageIndicator
            label="150-Day"
            maValue={data.moving_averages.ma_150}
            currentPrice={data.current_price}
          />
          <MovingAverageIndicator
            label="200-Day"
            maValue={data.moving_averages.ma_200_day}
            currentPrice={data.current_price}
          />
          <MovingAverageIndicator
            label="200-Week"
            maValue={data.moving_averages.ma_200_week}
            currentPrice={data.current_price}
          />
        </div>
      </CardContent>

      {/* Edit Dialog */}
      {watchlistItem && (
        <EditStockDialog
          open={isEditDialogOpen}
          onClose={() => setIsEditDialogOpen(false)}
          symbol={symbol}
          currentName={watchlistItem.name}
          currentSector={watchlistItem.sector}
        />
      )}
    </Card>
  );
};
