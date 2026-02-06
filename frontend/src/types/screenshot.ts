export interface Screenshot {
  id: number;
  image_path: string;
  upload_timestamp: string;
  extracted_text: string | null;
  tickers_mentioned: string[];
  investment_thesis: string | null;
  ai_analyzed: boolean;
  ai_analysis: string | null;
  recommendation: string | null;
  risk_rating: string | null;
  analysis_cost: number | null;
  analyzed_at: string | null;
}

export interface ScreenshotUploadResponse {
  id: number;
  extracted_text: string;
  tickers_mentioned: string[];
  investment_thesis: string;
  upload_timestamp: string;
}

export interface AIAnalysisResponse {
  id: number;
  ai_analysis: string;
  recommendation: string;
  risk_rating: string;
  analysis_cost: number;
  analyzed_at: string;
}
