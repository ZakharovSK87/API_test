import aiohttp
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

SPAM_API_KEY = os.getenv("NINJAS_API_KEY")

async def is_spam_text(text: str) -> bool:
    if not SPAM_API_KEY:
        logger.warning("NINJAS_API_KEY not found in environment variables")
        return False
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.api-ninjas.com/v1/spamcheck",
                headers={"X-Api-Key": SPAM_API_KEY},
                params={"text": text}
            ) as response:
                if response.status != 200:
                    logger.error(f"Spam API returned status {response.status}")
                    return False

                data = await response.json()
                return data.get("is_spam", False)
    except Exception as e:
        logger.error(f"Error in spam detection: {e}")
        return False
