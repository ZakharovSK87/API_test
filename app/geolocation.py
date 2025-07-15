import aiohttp

async def get_country_by_ip(ip: str) -> str:
    try:
        url = f"http://ip-api.com/json/{ip}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data.get("country", "unknown")
    except Exception:
        return "unknown"
