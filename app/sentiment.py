import aiohttp
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

API_KEY = os.getenv("APILAYER_API_KEY")

async def analyze_sentiment(text: str) -> str:
    if not API_KEY:
        logger.warning("APILAYER_API_KEY not found in environment variables")
        return "unknown"

    url = "https://api.apilayer.com/sentiment"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json={"text": text}) as response:
                if response.status != 200:
                    logger.error(f"Sentiment API returned status {response.status}")
                    return "unknown"

                result = await response.json()
                return result.get("sentiment", "unknown")
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return "unknown"
