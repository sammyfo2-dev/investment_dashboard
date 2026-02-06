import React from 'react';
import { TrendingUp } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="border-b bg-white">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center gap-3">
          <TrendingUp className="w-8 h-8 text-primary" />
          <div>
            <h1 className="text-2xl font-bold">Investing Dashboard</h1>
            <p className="text-sm text-muted-foreground">
              Track stocks with Charlie Munger's strategy
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};
