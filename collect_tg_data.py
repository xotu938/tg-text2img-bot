# collect_tg_data.py
import os
import asyncio
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, DocumentAttributeFilename
from dotenv import load_dotenv

from db import init_db, insert_message, insert_image

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = "collector_session"
SOURCE_CHAT_USERNAME = os.getenv("SOURCE_CHAT_USERNAME", "")

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "data", "images")


async def collect(limit: int = 500):
    if not (API_ID and API_HASH and SOURCE_CHAT_USERNAME):
        raise RuntimeError("请先在 .env 中配置 API_ID / API_HASH / SOURCE_CHAT_USERNAME")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    await init_db()

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    entity = await client.get_entity(SOURCE_CHAT_USERNAME)

    async for msg in client.iter_messages(entity, limit=limit):
        # 存文本
        if msg.message:
            await insert_message(
                message_id=msg.id,
                chat_id=entity.id,
                text=msg.message,
                date=msg.date.isoformat() if msg.date else "",
            )

        # 存图片
        if isinstance(msg.media, MessageMediaPhoto) or (
            msg.document
            and any(
                isinstance(a, DocumentAttributeFilename)
                and (a.file_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
                for a in msg.document.attributes
            )
        ):
            filename = f"{entity.id}_{msg.id}.jpg"
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            try:
                await client.download_media(msg, file=filepath)
                await insert_image(
                    message_id=msg.id,
                    chat_id=entity.id,
                    file_path=filepath,
                    caption=msg.message or "",
                    date=msg.date.isoformat() if msg.date else "",
                )
                print(f"下载并记录图片: {filepath}")
            except Exception as e:
                print(f"下载图片失败 message_id={msg.id}: {e}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(collect(limit=500))
