import React, { useState } from 'react';
import { TrackerGrid } from '@/components/tracker/TrackerGrid';
import { ScreenshotUpload } from '@/components/screenshots/ScreenshotUpload';
import { ScreenshotHistory } from '@/components/screenshots/ScreenshotHistory';

export const Dashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'tracker' | 'screenshots'>('tracker');

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b">
        <button
          onClick={() => setActiveTab('tracker')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'tracker'
              ? 'border-b-2 border-primary text-primary'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          Price Tracker
        </button>
        <button
          onClick={() => setActiveTab('screenshots')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'screenshots'
              ? 'border-b-2 border-primary text-primary'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          Screenshot Analysis
        </button>
      </div>

      {/* Content */}
      {activeTab === 'tracker' ? (
        <div>
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">Your Watchlist</h2>
            <p className="text-muted-foreground">
              Track stocks relative to moving averages and 52-week ranges
            </p>
          </div>
          <TrackerGrid />
        </div>
      ) : (
        <div className="space-y-6">
          <div>
            <h2 className="text-xl font-semibold mb-2">Investment Screenshot Analysis</h2>
            <p className="text-muted-foreground">
              Extract tickers and ideas from X/Twitter screenshots with optional AI analysis
            </p>
          </div>
          <ScreenshotUpload />
          <ScreenshotHistory />
        </div>
      )}
    </div>
  );
};
