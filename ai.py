import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

FEW_SHOT_EXAMPLES = """
<example>
Ticker: AAPL, P/E: 30, 52wk_High: 190, Current: 185

**Analysis** P/E is slightly above historical average (25), but trading near 52-week high with strong momentum from news.

**Recommendation** HOLD : The stock is near a resistance level; wait for a pullback despite strong fundamentals.
</example>

<example>
Ticker: TSLA, P/E: 75, 52wk_High: 290, Current: 150

**Analysis** Valuation is extremely high relative to peers, and price is down 48% from highs. Negative news creates further downside risk.

**Recommendation** SELL : High valuation and technical breakdown suggest further weakness.
</example>
"""

def get_ai_analysis(ticker, data):
    """Sends stock data to Gemini for analysis."""
    prompt = f"""
    You are a professional stock analyst. 
    You will format your response based on the following patterns:\n{FEW_SHOT_EXAMPLES}\n
    Analyze the following data for {ticker} ({data['name']} 
    - Current Price: ${data['current_price']}
    - Forward P/E Ratio: {data['pe_ratio']}
    - 52-Week Range: ${data['52_week_low']} - ${data['52_week_high']}
    - Market Cap: {data['market_cap']}
    - General Analyst Consensus: {data['analyst_recommendation']}

    Task:
    1. Determine if the stock is a 'Buy', 'Hold', or 'Sell'.
    2. Provide a 3-sentence justification focusing on the stock's recent performance, P/E ratio, and price position.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text