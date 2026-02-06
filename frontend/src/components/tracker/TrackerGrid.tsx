import React, { useState, useMemo } from 'react';
import { PriceCard } from './PriceCard';
import { AddStockDialog } from './AddStockDialog';
import { useWatchlist } from '@/hooks/useWatchlist';
import { Button } from '@/components/ui/Button';
import { Plus, ChevronRight, ChevronDown } from 'lucide-react';

export const TrackerGrid: React.FC = () => {
  const { watchlist, isLoading, error } = useWatchlist();
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [collapsedSectors, setCollapsedSectors] = useState<Set<string>>(
    new Set()
  );

  // Group watchlist by sector
  const groupedBySector = useMemo(() => {
    const groups: { sector: string; items: typeof watchlist }[] = [];
    const sectorMap = new Map<string, typeof watchlist>();

    watchlist.forEach((item) => {
      const sector = item.sector || 'Unknown';
      if (!sectorMap.has(sector)) {
        sectorMap.set(sector, []);
      }
      sectorMap.get(sector)!.push(item);
    });

    // Convert to array and sort: Cryptocurrency first, then alphabetically
    const sectors = Array.from(sectorMap.keys()).sort((a, b) => {
      if (a === 'Cryptocurrency') return -1;
      if (b === 'Cryptocurrency') return 1;
      return a.localeCompare(b);
    });

    sectors.forEach((sector) => {
      groups.push({
        sector,
        items: sectorMap.get(sector)!,
      });
    });

    return groups;
  }, [watchlist]);

  const toggleSector = (sector: string) => {
    setCollapsedSectors((prev) => {
      const next = new Set(prev);
      if (next.has(sector)) {
        next.delete(sector);
      } else {
        next.add(sector);
      }
      return next;
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-muted-foreground">Loading watchlist...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-red-500">Error loading watchlist</div>
      </div>
    );
  }

  if (watchlist.length === 0) {
    return (
      <>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg p-12 max-w-md">
            <h3 className="text-xl font-semibold text-foreground mb-2">
              Your watchlist is empty
            </h3>
            <p className="text-muted-foreground mb-6">
              Start tracking stocks and cryptocurrencies by adding your first symbol
            </p>
            <Button onClick={() => setIsAddDialogOpen(true)}>
              <Plus className="w-4 h-4 mr-2" />
              Add Your First Stock
            </Button>
          </div>
        </div>
        <AddStockDialog
          open={isAddDialogOpen}
          onClose={() => setIsAddDialogOpen(false)}
        />
      </>
    );
  }

  const totalStocks = watchlist.length;
  const totalSectors = groupedBySector.length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Your Watchlist</h2>
          <p className="text-muted-foreground">
            {totalStocks} {totalStocks === 1 ? 'stock' : 'stocks'} across{' '}
            {totalSectors} {totalSectors === 1 ? 'sector' : 'sectors'}
          </p>
        </div>
        <Button onClick={() => setIsAddDialogOpen(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Add Stock
        </Button>
      </div>

      {/* Sector groups */}
      <div className="space-y-4">
        {groupedBySector.map((group) => {
          const isCollapsed = collapsedSectors.has(group.sector);

          return (
            <div
              key={group.sector}
              className="border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden"
            >
              {/* Sector header */}
              <button
                onClick={() => toggleSector(group.sector)}
                className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors flex items-center justify-between"
              >
                <div className="flex items-center gap-2">
                  {isCollapsed ? (
                    <ChevronRight className="w-5 h-5 text-muted-foreground" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-muted-foreground" />
                  )}
                  <h3 className="text-lg font-semibold text-foreground">
                    {group.sector}
                  </h3>
                  <span className="text-sm text-muted-foreground">
                    ({group.items.length})
                  </span>
                </div>
              </button>

              {/* Sector content */}
              {!isCollapsed && (
                <div className="p-4 bg-white dark:bg-black">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    {group.items.map((item) => (
                      <PriceCard
                        key={item.id}
                        symbol={item.symbol}
                        name={item.name}
                      />
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <AddStockDialog
        open={isAddDialogOpen}
        onClose={() => setIsAddDialogOpen(false)}
      />
    </div>
  );
};
