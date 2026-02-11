export interface WatchlistItem {
  id: number;
  symbol: string;
  asset_type: 'STOCK' | 'CRYPTO';
  name: string;
  sector: string | null;
  added_at: string;
}

export interface WatchlistCreate {
  symbol: string;
  asset_type: 'STOCK' | 'CRYPTO';
  name?: string;
}

export interface WatchlistUpdate {
  name?: string;
  sector?: string;
}
