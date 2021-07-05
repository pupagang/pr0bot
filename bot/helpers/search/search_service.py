from __future__ import annotations

import json
import aiohttp


class Pr0Items:
    tags: str
    params: dict

    def __init__(self, cookies: json = None) -> None:
        self.__COOKIES = cookies
        self.__API_URL = "https://pr0gramm.com/api/items/get"

    async def make_api_call(self, params: dict) -> dict:
        async with aiohttp.ClientSession(cookies=self.__COOKIES) as session:
            async with session.get(self.__API_URL, params=params) as resp:
                return await resp.json()
