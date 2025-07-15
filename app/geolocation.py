import aiohttp
import logging

logger = logging.getLogger(__name__)

async def get_country_by_ip(ip: str) -> str:
    if not ip or ip == "127.0.0.1" or ip.startswith("192.168.") or ip.startswith("10."):
        return "unknown"
    
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"http://ip-api.com/json/{ip}") as resp:
                if resp.status != 200:
                    logger.error(f"Geolocation API returned status {resp.status}")
                    return "unknown"
                
                data = await resp.json()
                return data.get("country", "unknown")
    except aiohttp.ClientError as e:
        logger.error(f"Network error in geolocation: {e}")
        return "unknown"
    except Exception as e:
        logger.error(f"Unexpected error in geolocation: {e}")
        return "unknown"
