from anthropic import Anthropic
import os
from typing import Optional, Dict
from app.config import get_settings

settings = get_settings()


class AIAnalysisService:
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.enabled = bool(self.api_key and self.api_key.strip())

        if self.enabled:
            self.client = Anthropic(api_key=self.api_key)
        else:
            self.client = None

    async def deep_analysis(self, extracted_text: str, tickers: list[str]) -> Optional[Dict]:
        """
        Optional deep analysis - only called when user clicks "Analyze" button
        Uses text-only (cheaper than vision API)
        """
        if not self.enabled:
            return {
                'error': 'AI analysis is disabled. Set ANTHROPIC_API_KEY to enable.',
                'analysis': '',
                'recommendation': 'N/A',
                'risk_rating': 'N/A',
                'cost': 0,
            }

        try:
            prompt = f"""
Analyze this investment advice from X/Twitter:

Tickers mentioned: {', '.join(tickers) if tickers else 'None'}
Content: {extracted_text}

Provide a structured analysis with:
1. Investment thesis summary (2-3 sentences)
2. Key claims and their validity
3. Risk factors to consider
4. Recommendation (BUY/HOLD/AVOID) based on Charlie Munger's value investing principles
5. Risk rating (LOW/MEDIUM/HIGH)

Be concise (max 300 words). Focus on fundamentals, not hype.
"""

            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",  # Cheaper model
                max_tokens=500,  # Limit tokens = lower cost
                messages=[{"role": "user", "content": prompt}]
            )

            analysis_text = response.content[0].text

            # Parse the response
            parsed = self._parse_response(analysis_text)

            # Estimate cost (rough calculation)
            # Haiku pricing: ~$0.25 per million input tokens, ~$1.25 per million output tokens
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = (input_tokens * 0.25 / 1_000_000) + (output_tokens * 1.25 / 1_000_000)

            return {
                'analysis': analysis_text,
                'recommendation': parsed['recommendation'],
                'risk_rating': parsed['risk_rating'],
                'cost': round(cost, 4),
            }

        except Exception as e:
            print(f"AI analysis error: {e}")
            return {
                'error': str(e),
                'analysis': '',
                'recommendation': 'ERROR',
                'risk_rating': 'N/A',
                'cost': 0,
            }

    def _parse_response(self, text: str) -> Dict[str, str]:
        """Extract recommendation and risk rating from AI response"""
        recommendation = 'HOLD'  # Default
        risk_rating = 'MEDIUM'  # Default

        text_upper = text.upper()

        # Extract recommendation
        if 'RECOMMENDATION: BUY' in text_upper or 'RECOMMENDATION:BUY' in text_upper:
            recommendation = 'BUY'
        elif 'RECOMMENDATION: AVOID' in text_upper or 'RECOMMENDATION:AVOID' in text_upper:
            recommendation = 'AVOID'
        elif 'RECOMMENDATION: HOLD' in text_upper or 'RECOMMENDATION:HOLD' in text_upper:
            recommendation = 'HOLD'
        else:
            # Fallback search
            if 'BUY' in text_upper and 'AVOID' not in text_upper:
                recommendation = 'BUY'
            elif 'AVOID' in text_upper or 'SELL' in text_upper:
                recommendation = 'AVOID'

        # Extract risk rating
        if 'RISK RATING: HIGH' in text_upper or 'RISK RATING:HIGH' in text_upper:
            risk_rating = 'HIGH'
        elif 'RISK RATING: LOW' in text_upper or 'RISK RATING:LOW' in text_upper:
            risk_rating = 'LOW'
        elif 'RISK RATING: MEDIUM' in text_upper or 'RISK RATING:MEDIUM' in text_upper:
            risk_rating = 'MEDIUM'
        else:
            # Fallback search
            if 'HIGH RISK' in text_upper:
                risk_rating = 'HIGH'
            elif 'LOW RISK' in text_upper:
                risk_rating = 'LOW'

        return {
            'recommendation': recommendation,
            'risk_rating': risk_rating,
        }


ai_service = AIAnalysisService()
