from motor.motor_asyncio import AsyncIOMotorClient


class DbService:
    def __init__(self, db: AsyncIOMotorClient) -> None:
        self.__DB = db

    async def add_posts(self, posts: dict) -> None:
        tmp_dict = {"_id": posts["id"]}
        await self.__DB.insert_one(tmp_dict)

    async def check_post(self, id: int) -> None:
        return await self.__DB.find_one({"_id": id})
