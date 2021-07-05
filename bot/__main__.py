from typing import BinaryIO

from . import pr0, db, app, config

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import asyncio
import time


sched = AsyncIOScheduler(daemon=True)


async def main():
    for x in config["tags"].keys():
        await process_posts(x)


async def send_video_post(video: str or BinaryIO) -> None:
    await app.send_video(chat_id=config["core"]["channel"], video=video)


async def send_photo_post(photo: str or BinaryIO) -> None:
    await app.send_photo(chat_id=config["core"]["channel"], photo=photo)


async def process_posts(tag: str) -> None:
    current_time = round(time.time(), 6)
    old_time = current_time - 172800
    for x in config["tags"][tag]:
        result = await pr0.make_api_call(config["tags"][tag][x])
        for z in result["items"]:
            if z["created"] > old_time:
                db_check = await db.check_post(z["id"])

                if not db_check:
                    if not z["source"] and z["image"].endswith(".mp4"):
                        await send_video_post(
                            video=f'https://vid.pr0gramm.com/{z["image"]}',
                        )
                        await db.add_posts(z)
                        await asyncio.sleep(5)

                    elif z["source"].endswith(".mp4"):
                        await send_video_post(video=z["source"])
                        await db.add_posts(z)
                        await asyncio.sleep(5)

                    elif z["image"].endswith(".jpg"):
                        await send_photo_post(
                            photo=f'https://img.pr0gramm.com/{z["image"]}',
                        )
                        await db.add_posts(z)
                        await asyncio.sleep(5)


sched.add_job(main, "interval", seconds=300)
sched.start()
app.start()
asyncio.get_event_loop().run_forever()
