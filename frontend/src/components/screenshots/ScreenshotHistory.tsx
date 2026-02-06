import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { useScreenshots } from '@/hooks/useScreenshots';
import { format } from 'date-fns';
import { Sparkles, Trash2 } from 'lucide-react';

export const ScreenshotHistory: React.FC = () => {
  const { screenshots, analyzeScreenshot, deleteScreenshot, isAnalyzing } =
    useScreenshots();

  if (screenshots.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Screenshot History</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-8">
            No screenshots uploaded yet
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Screenshot History</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {screenshots.map((screenshot) => (
            <div
              key={screenshot.id}
              className="border rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex-1">
                  <div className="text-sm text-muted-foreground mb-1">
                    {format(new Date(screenshot.upload_timestamp), 'PPp')}
                  </div>
                  {screenshot.tickers_mentioned.length > 0 && (
                    <div className="flex gap-2 flex-wrap mb-2">
                      {screenshot.tickers_mentioned.map((ticker) => (
                        <span
                          key={ticker}
                          className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium"
                        >
                          ${ticker}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <button
                  onClick={() => deleteScreenshot(screenshot.id)}
                  className="text-red-500 hover:text-red-700 p-1"
                  title="Delete screenshot"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              {screenshot.investment_thesis && (
                <div className="text-sm mb-3 p-3 bg-gray-50 rounded">
                  <div className="font-medium mb-1">Investment Thesis:</div>
                  <div className="text-muted-foreground whitespace-pre-wrap">
                    {screenshot.investment_thesis}
                  </div>
                </div>
              )}

              {!screenshot.ai_analyzed ? (
                <button
                  onClick={() => analyzeScreenshot(screenshot.id)}
                  disabled={isAnalyzing}
                  className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                >
                  <Sparkles className="w-4 h-4" />
                  {isAnalyzing ? 'Analyzing...' : 'Analyze with AI (~$0.10-0.25)'}
                </button>
              ) : (
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-3 py-1 rounded text-sm font-medium ${
                        screenshot.recommendation === 'BUY'
                          ? 'bg-green-100 text-green-700'
                          : screenshot.recommendation === 'AVOID'
                          ? 'bg-red-100 text-red-700'
                          : 'bg-yellow-100 text-yellow-700'
                      }`}
                    >
                      {screenshot.recommendation}
                    </span>
                    <span
                      className={`px-3 py-1 rounded text-sm ${
                        screenshot.risk_rating === 'HIGH'
                          ? 'bg-red-100 text-red-700'
                          : screenshot.risk_rating === 'LOW'
                          ? 'bg-green-100 text-green-700'
                          : 'bg-yellow-100 text-yellow-700'
                      }`}
                    >
                      Risk: {screenshot.risk_rating}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      Cost: ${screenshot.analysis_cost?.toFixed(4)}
                    </span>
                  </div>
                  <div className="text-sm p-3 bg-blue-50 rounded whitespace-pre-wrap">
                    {screenshot.ai_analysis}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};
