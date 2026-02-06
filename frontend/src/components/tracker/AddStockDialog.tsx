import React, { useState } from 'react';
import {
  Dialog,
  DialogHeader,
  DialogTitle,
  DialogContent,
  DialogFooter,
} from '@/components/ui/Dialog';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { useWatchlist } from '@/hooks/useWatchlist';

interface AddStockDialogProps {
  open: boolean;
  onClose: () => void;
}

export const AddStockDialog: React.FC<AddStockDialogProps> = ({
  open,
  onClose,
}) => {
  const [symbol, setSymbol] = useState('');
  const [assetType, setAssetType] = useState<'STOCK' | 'CRYPTO'>('STOCK');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { addToWatchlist } = useWatchlist();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!symbol.trim()) {
      setError('Symbol is required');
      return;
    }

    setIsLoading(true);

    try {
      await addToWatchlist(
        {
          symbol: symbol.toUpperCase(),
          asset_type: assetType,
        },
        {
          onSuccess: () => {
            setSymbol('');
            setAssetType('STOCK');
            setError('');
            onClose();
          },
          onError: (err: any) => {
            setError(
              err?.response?.data?.detail || 'Failed to add stock. Please try again.'
            );
          },
        }
      );
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || 'Failed to add stock. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    if (!isLoading) {
      setSymbol('');
      setAssetType('STOCK');
      setError('');
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <form onSubmit={handleSubmit}>
        <DialogHeader>
          <DialogTitle>Add Stock to Watchlist</DialogTitle>
        </DialogHeader>

        <DialogContent>
          <div className="space-y-4">
            <Input
              label="Symbol"
              placeholder="e.g., AAPL, GOOGL, BTC-USD"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              disabled={isLoading}
              error={error}
            />

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                Asset Type
              </label>
              <div className="flex gap-4">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    value="STOCK"
                    checked={assetType === 'STOCK'}
                    onChange={(e) =>
                      setAssetType(e.target.value as 'STOCK' | 'CRYPTO')
                    }
                    disabled={isLoading}
                    className="w-4 h-4"
                  />
                  <span className="text-sm">Stock</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    value="CRYPTO"
                    checked={assetType === 'CRYPTO'}
                    onChange={(e) =>
                      setAssetType(e.target.value as 'STOCK' | 'CRYPTO')
                    }
                    disabled={isLoading}
                    className="w-4 h-4"
                  />
                  <span className="text-sm">Cryptocurrency</span>
                </label>
              </div>
            </div>

            <div className="bg-blue-50 dark:bg-blue-950 p-3 rounded-md text-sm text-blue-800 dark:text-blue-200">
              Name and sector will be automatically fetched from the symbol.
            </div>
          </div>
        </DialogContent>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            onClick={handleClose}
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Adding...' : 'Add Stock'}
          </Button>
        </DialogFooter>
      </form>
    </Dialog>
  );
};
