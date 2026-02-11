import React, { useState } from 'react';
import { Search, Filter, X, TrendingUp, TrendingDown, ArrowUpDown, ChevronDown } from 'lucide-react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { SortOption, PerformanceFilter } from '../../types/filter';

interface SearchFilterBarProps {
  searchTerm: string;
  onSearchChange: (term: string) => void;
  selectedSectors: string[];
  availableSectors: string[];
  onSectorToggle: (sector: string) => void;
  performanceFilter: PerformanceFilter;
  onPerformanceChange: (filter: PerformanceFilter) => void;
  sortBy: SortOption;
  onSortChange: (sort: SortOption) => void;
  onClearFilters: () => void;
  resultsCount: number;
  totalCount: number;
}

const SORT_OPTIONS: { value: SortOption; label: string }[] = [
  { value: 'alpha-asc', label: 'A-Z' },
  { value: 'alpha-desc', label: 'Z-A' },
  { value: 'percent-desc', label: '% Change ↓' },
  { value: 'percent-asc', label: '% Change ↑' },
  { value: 'price-desc', label: 'Price ↓' },
  { value: 'price-asc', label: 'Price ↑' },
];

export const SearchFilterBar: React.FC<SearchFilterBarProps> = ({
  searchTerm,
  onSearchChange,
  selectedSectors,
  availableSectors,
  onSectorToggle,
  performanceFilter,
  onPerformanceChange,
  sortBy,
  onSortChange,
  onClearFilters,
  resultsCount,
  totalCount,
}) => {
  const [showSectorDropdown, setShowSectorDropdown] = useState(false);

  const hasActiveFilters =
    searchTerm.trim() !== '' ||
    selectedSectors.length > 0 ||
    performanceFilter !== 'all' ||
    sortBy !== 'alpha-asc';

  const activeFilterCount =
    (searchTerm.trim() !== '' ? 1 : 0) +
    (selectedSectors.length > 0 ? 1 : 0) +
    (performanceFilter !== 'all' ? 1 : 0) +
    (sortBy !== 'alpha-asc' ? 1 : 0);

  return (
    <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-6 space-y-4">
      {/* Search and Results Count */}
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            type="text"
            placeholder="Search by symbol or name..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="pl-10"
          />
        </div>

        <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
          <span className="font-medium">
            {resultsCount} of {totalCount} stocks
          </span>
        </div>
      </div>

      {/* Filters Row */}
      <div className="flex flex-wrap gap-3 items-center">
        {/* Sector Filter */}
        <div className="relative">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSectorDropdown(!showSectorDropdown)}
            className="gap-2"
          >
            <Filter className="h-4 w-4" />
            Sectors
            {selectedSectors.length > 0 && (
              <span className="bg-primary text-primary-foreground rounded-full px-2 py-0.5 text-xs font-medium">
                {selectedSectors.length}
              </span>
            )}
            <ChevronDown className="h-3 w-3" />
          </Button>

          {showSectorDropdown && (
            <>
              <div
                className="fixed inset-0 z-10"
                onClick={() => setShowSectorDropdown(false)}
              />
              <div className="absolute top-full left-0 mt-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-20 max-h-64 overflow-y-auto">
                {availableSectors.length === 0 ? (
                  <div className="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">
                    No sectors available
                  </div>
                ) : (
                  availableSectors.map((sector) => (
                    <button
                      key={sector}
                      onClick={() => onSectorToggle(sector)}
                      className="w-full flex items-center gap-2 px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 text-sm text-left"
                    >
                      <div
                        className={`w-4 h-4 border-2 rounded flex items-center justify-center ${
                          selectedSectors.includes(sector)
                            ? 'bg-primary border-primary'
                            : 'border-gray-300 dark:border-gray-600'
                        }`}
                      >
                        {selectedSectors.includes(sector) && (
                          <svg
                            className="w-3 h-3 text-white"
                            fill="none"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </div>
                      <span className="text-gray-900 dark:text-gray-100">{sector}</span>
                    </button>
                  ))
                )}
              </div>
            </>
          )}
        </div>

        {/* Performance Filter */}
        <div className="flex gap-1 bg-white dark:bg-gray-800 rounded-md p-1 border border-gray-200 dark:border-gray-700">
          <button
            onClick={() => onPerformanceChange('all')}
            className={`px-3 py-1.5 text-sm rounded transition-colors ${
              performanceFilter === 'all'
                ? 'bg-primary text-primary-foreground'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            All
          </button>
          <button
            onClick={() => onPerformanceChange('gainers')}
            className={`px-3 py-1.5 text-sm rounded transition-colors flex items-center gap-1.5 ${
              performanceFilter === 'gainers'
                ? 'bg-green-500 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            <TrendingUp className="h-3.5 w-3.5" />
            Gainers
          </button>
          <button
            onClick={() => onPerformanceChange('losers')}
            className={`px-3 py-1.5 text-sm rounded transition-colors flex items-center gap-1.5 ${
              performanceFilter === 'losers'
                ? 'bg-red-500 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            <TrendingDown className="h-3.5 w-3.5" />
            Losers
          </button>
        </div>

        {/* Sort Dropdown */}
        <div className="flex items-center gap-2">
          <ArrowUpDown className="h-4 w-4 text-gray-400" />
          <select
            value={sortBy}
            onChange={(e) => onSortChange(e.target.value as SortOption)}
            className="h-9 px-3 rounded-md border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
          >
            {SORT_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {/* Clear Filters Button */}
        {hasActiveFilters && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onClearFilters}
            className="gap-1.5 text-gray-600 dark:text-gray-400"
          >
            <X className="h-4 w-4" />
            Clear {activeFilterCount > 1 && `(${activeFilterCount})`}
          </Button>
        )}
      </div>

      {/* Selected Sector Chips */}
      {selectedSectors.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedSectors.map((sector) => (
            <div
              key={sector}
              className="inline-flex items-center gap-1.5 bg-primary/10 text-primary px-2.5 py-1 rounded-full text-sm"
            >
              <span>{sector}</span>
              <button
                onClick={() => onSectorToggle(sector)}
                className="hover:bg-primary/20 rounded-full p-0.5"
              >
                <X className="h-3 w-3" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
