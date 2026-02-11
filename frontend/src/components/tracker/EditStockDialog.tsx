import React, { useState, useEffect, useMemo } from 'react';
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

interface EditStockDialogProps {
  open: boolean;
  onClose: () => void;
  symbol: string;
  currentName: string;
  currentSector: string | null;
}

export const EditStockDialog: React.FC<EditStockDialogProps> = ({
  open,
  onClose,
  symbol,
  currentName,
  currentSector,
}) => {
  const [name, setName] = useState(currentName);
  const [sector, setSector] = useState(currentSector || '');
  const [customSector, setCustomSector] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { watchlist, updateWatchlistItem } = useWatchlist();

  // Get unique sectors from watchlist
  const availableSectors = useMemo(() => {
    const sectors = new Set(
      watchlist
        .map((item) => item.sector)
        .filter((s): s is string => s !== null && s !== 'Unknown')
    );
    return Array.from(sectors).sort();
  }, [watchlist]);

  // Reset form when dialog opens
  useEffect(() => {
    if (open) {
      setName(currentName);
      setSector(currentSector || '');
      setCustomSector('');
      setError('');
    }
  }, [open, currentName, currentSector]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!name.trim()) {
      setError('Name is required');
      return;
    }

    const finalSector = sector === 'custom' ? customSector : sector;

    if (!finalSector.trim()) {
      setError('Sector is required');
      return;
    }

    setIsLoading(true);

    try {
      await updateWatchlistItem({
        symbol,
        data: {
          name: name.trim(),
          sector: finalSector.trim(),
        },
      });
      onClose();
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || 'Failed to update stock. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    if (!isLoading) {
      onClose();
    }
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <form onSubmit={handleSubmit}>
        <DialogHeader>
          <DialogTitle>Edit {symbol}</DialogTitle>
        </DialogHeader>

        <DialogContent>
          <div className="space-y-4">
            <Input
              label="Name"
              placeholder="Company or cryptocurrency name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={isLoading}
            />

            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">
                Sector
              </label>
              <select
                value={sector}
                onChange={(e) => setSector(e.target.value)}
                disabled={isLoading}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <option value="">Select a sector...</option>
                {availableSectors.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
                <option value="custom">+ Add Custom Sector</option>
              </select>
            </div>

            {sector === 'custom' && (
              <Input
                label="Custom Sector"
                placeholder="Enter sector name"
                value={customSector}
                onChange={(e) => setCustomSector(e.target.value)}
                disabled={isLoading}
              />
            )}

            {error && (
              <div className="bg-red-50 dark:bg-red-950 p-3 rounded-md text-sm text-red-800 dark:text-red-200">
                {error}
              </div>
            )}
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
            {isLoading ? 'Saving...' : 'Save Changes'}
          </Button>
        </DialogFooter>
      </form>
    </Dialog>
  );
};
