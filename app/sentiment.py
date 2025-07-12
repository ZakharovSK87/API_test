import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("APILAYER_API_KEY")
API_URL = "https://api.apilayer.com/sentiment/analysis"

headers = {
    "apikey": API_KEY
}

async def analyze_sentiment(text: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json={"text": text}, headers=headers) as resp:
                data = await resp.json()
                return data.get("sentiment", "unknown")
    except Exception:
        return "unknown"
