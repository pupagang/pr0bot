from typing import BinaryIO
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from motor import motor_asyncio

from . import pr0, db, app, config, db_gore

import asyncio
import time


sched = AsyncIOScheduler(daemon=True)


async def main():
    for x in config["tags"].keys():
        await process_posts(yaml_config=config["tags"][x],
                            chat_id=config["core"]["channel"],
                            mongo=db)
    await process_posts(chat_id=config["core"]["goreguy"],
                        yaml_config=config["Gore"],
                        mongo=db_gore)


async def send_video_post(video: str or BinaryIO, caption: str, chat_id: str) -> None:
    await app.send_video(chat_id=chat_id, video=video, caption=f"#{caption}")


async def send_photo_post(photo: str or BinaryIO, caption: str, chat_id: str) -> None:
    await app.send_photo(chat_id=chat_id, photo=photo, caption=f"#{caption}")


async def process_posts(yaml_config: dict, chat_id: str, mongo: motor_asyncio) -> None:
    current_time = round(time.time(), 6)
    old_time = current_time - 172800
    for x in yaml_config:
        result = await pr0.make_api_call(yaml_config[x])
        for z in result["items"]:
            if z["created"] > old_time:
                db_check = await mongo.check_post(z["id"])

                if not db_check:
                    tag = await pr0.get_tags(z["id"])
                    if not z["source"] and z["image"].endswith(".mp4"):
                        await send_video_post(
                            video=f'https://vid.pr0gramm.com/{z["image"]}', caption=tag, chat_id=chat_id
                        )
                        await mongo.add_posts(z)
                        await asyncio.sleep(5)

                    elif z["source"].endswith(".mp4"):
                        await send_video_post(video=z["source"], caption=tag, chat_id=chat_id)
                        await mongo.add_posts(z)
                        await asyncio.sleep(5)

                    elif z["image"].endswith(".jpg") or z["image"].endswith(".png"):
                        await send_photo_post(
                            photo=f'https://img.pr0gramm.com/{z["image"]}', caption=tag, chat_id=chat_id
                        )
                        await mongo.add_posts(z)
                        await asyncio.sleep(5)


sched.add_job(main, "interval", seconds=200)
sched.start()
app.start()
asyncio.get_event_loop().run_forever()
