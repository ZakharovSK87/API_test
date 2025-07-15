import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

SPAM_API_KEY = os.getenv("NINJAS_API_KEY")

async def is_spam_text(text: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.api-ninjas.com/v1/spamfilter",
                headers={"X-Api-Key": SPAM_API_KEY},
                json={"text": text}
            ) as response:
                data = await response.json()
                return data.get("is_spam", False)
    except Exception:
        return False
