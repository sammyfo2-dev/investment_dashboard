import React from 'react';
import { HighLowRange } from '@/types/stock';
import { formatCurrency } from '@/lib/utils';

interface HighLowRangeBarProps {
  range: HighLowRange;
}

export const HighLowRangeBar: React.FC<HighLowRangeBarProps> = ({ range }) => {
  const { week_52_high, week_52_low, current_price, position_percent } = range;

  if (week_52_high === null || week_52_low === null || position_percent === null) {
    return (
      <div className="space-y-2">
        <div className="text-sm font-medium">52-Week Range</div>
        <div className="text-sm text-muted-foreground">Data unavailable</div>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="font-medium">52-Week Range</span>
        <span className="text-muted-foreground">
          {position_percent.toFixed(0)}% of range
        </span>
      </div>

      <div className="relative h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className="absolute h-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500"
          style={{ width: '100%' }}
        />
        <div
          className="absolute top-0 h-full w-1 bg-blue-600 shadow-lg"
          style={{ left: `${position_percent}%` }}
        >
          <div className="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap text-xs font-bold text-blue-600">
            {formatCurrency(current_price)}
          </div>
        </div>
      </div>

      <div className="flex justify-between text-xs text-muted-foreground">
        <span>Low: {formatCurrency(week_52_low)}</span>
        <span>High: {formatCurrency(week_52_high)}</span>
      </div>
    </div>
  );
};
