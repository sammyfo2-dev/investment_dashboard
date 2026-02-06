import pytesseract
from PIL import Image
import re
from typing import List, Optional


class OCRService:
    def extract_text_from_screenshot(self, image_path: str) -> str:
        """Extract all text from screenshot using Tesseract OCR"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"OCR error: {e}")
            return ""

    def extract_tickers(self, text: str) -> List[str]:
        """
        Find stock tickers in text (e.g., $AAPL, TSLA)
        Pattern: $TICKER or uppercase 1-5 letter words
        """
        # Pattern 1: $TICKER format
        dollar_pattern = r'\$([A-Z]{1,5})\b'
        dollar_matches = re.findall(dollar_pattern, text)

        # Pattern 2: Standalone uppercase 2-5 letter words (excluding common words)
        word_pattern = r'\b([A-Z]{2,5})\b'
        word_matches = re.findall(word_pattern, text)

        # Common words to exclude
        excluded_words = {
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
            'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM',
            'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO',
            'WAY', 'WHO', 'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'SHE',
            'TOO', 'USE', 'USA', 'USD', 'EUR', 'GBP', 'JPY', 'CEO', 'CFO',
            'IPO', 'ETF', 'ESG', 'GDP', 'CPI', 'API', 'FAQ', 'PDF', 'URL',
            'HTTP', 'WWW', 'COM', 'ORG', 'NET', 'GOV', 'EDU', 'BTC', 'ETH',
        }

        # Combine and filter
        all_tickers = set(dollar_matches + word_matches)
        valid_tickers = [t for t in all_tickers if t not in excluded_words]

        return sorted(list(set(valid_tickers)))

    def extract_investment_thesis(self, text: str) -> str:
        """
        Extract key phrases related to investing
        Look for keywords: buy, sell, target, price, growth, etc.
        """
        keywords = [
            'buy', 'sell', 'target', 'price', 'growth', 'revenue',
            'earnings', 'profit', 'bullish', 'bearish', 'catalyst',
            'valuation', 'undervalued', 'overvalued', 'market cap',
            'dividend', 'stock', 'shares', 'long', 'short', 'position',
            'invest', 'trading', 'gains', 'loss', 'upside', 'downside',
            'rally', 'dip', 'breakout', 'support', 'resistance',
        ]

        lines = text.split('\n')
        relevant_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line contains investment keywords
            if any(keyword in line.lower() for keyword in keywords):
                relevant_lines.append(line)

            # Limit to top 5 most relevant lines
            if len(relevant_lines) >= 5:
                break

        return '\n'.join(relevant_lines) if relevant_lines else text[:500]  # Fallback to first 500 chars


ocr_service = OCRService()
