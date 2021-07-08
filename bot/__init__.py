from motor import motor_asyncio
from pyrogram import Client

import yaml
import json

from .helpers.search.search_service import Pr0Items
from .helpers.mongo_db.mongo_service import DbService

config = yaml.safe_load(open("config.yaml", "r"))
motor = motor_asyncio.AsyncIOMotorClient(config["core"]["mongodb_url"]).main
cookies = json.load(open("cookie.json", "r"))
token = config["core"]["token"]
api_id = config["core"]["api_id"]
api_hash = config["core"]["api_hash"]

pr0 = Pr0Items(cookies)
db = DbService(motor.posts)
app = Client("pr0", bot_token=token, api_id=api_id, api_hash=api_hash)
