import React from 'react';
import { cn, formatCurrency } from '@/lib/utils';

interface MovingAverageIndicatorProps {
  label: string;
  maValue: number | null;
  currentPrice: number;
}

export const MovingAverageIndicator: React.FC<MovingAverageIndicatorProps> = ({
  label,
  maValue,
  currentPrice,
}) => {
  if (maValue === null) {
    return (
      <div className="flex items-center justify-between py-1">
        <span className="text-sm text-muted-foreground">{label}</span>
        <span className="text-sm text-muted-foreground">N/A</span>
      </div>
    );
  }

  const isAbove = currentPrice > maValue;
  const distance = ((currentPrice - maValue) / maValue) * 100;

  return (
    <div className="flex items-center justify-between py-1">
      <span className="text-sm font-medium">{label}</span>
      <div className="flex items-center gap-2">
        <span
          className={cn(
            'text-sm font-medium',
            isAbove ? 'text-green-600' : 'text-red-600'
          )}
        >
          {isAbove ? '▲' : '▼'} {Math.abs(distance).toFixed(2)}%
        </span>
        <span className="text-xs text-muted-foreground">
          {formatCurrency(maValue)}
        </span>
      </div>
    </div>
  );
};
