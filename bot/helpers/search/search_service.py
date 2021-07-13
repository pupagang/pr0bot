from __future__ import annotations

import json
import aiohttp
import re


class Pr0Items:
    tags: str
    params: dict

    def __init__(self, cookies: json = None) -> None:
        self.__COOKIES = cookies
        self.__API_URL = "https://pr0gramm.com/api/items/get"
        self.__API_URL_INFO = "https://pr0gramm.com/api/items/info"

    async def make_api_call(self, params: dict) -> json:
        async with aiohttp.ClientSession(cookies=self.__COOKIES) as session:
            async with session.get(self.__API_URL, params=params) as resp:
                return await resp.json()

    async def get_tags(self, id: str or int) -> json:
        async with aiohttp.ClientSession(cookies=self.__COOKIES) as session:
            async with session.get(self.__API_URL_INFO, params={"itemId": id}) as resp:
                response = await resp.json()
                for x in response["tags"]:
                    return re.sub(" ", "", x["tag"])
