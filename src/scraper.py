"""
Telegram Scraper for Ethiopian Medical Channels
"""

import os
import csv
import json
import asyncio
import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto

# Add the project root to sys.path so we can import src.datalake
# This allows running from root via: python -m src.scraper
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import the datalake functions
from src.datalake import write_channel_messages_json, write_manifest

# =============================================================================
# CONFIGURATION
# =============================================================================

load_dotenv()

# We check for both TG_API_ID (standard) and Tg_API_ID (from your provided script)
api_id_str = os.getenv("TG_API_ID") or os.getenv("Tg_API_ID")
api_hash = os.getenv("TG_API_HASH") or os.getenv("Tg_API_HASH")

if not api_id_str or not api_hash:
    print("ERROR: Missing TG_API_ID or TG_API_HASH in .env file")
    sys.exit(1)

api_id = int(api_id_str)

TODAY = datetime.today().strftime("%Y-%m-%d")
DEFAULT_CHANNEL_DELAY = 3.0
DEFAULT_MESSAGE_DELAY = 1.0

# =============================================================================
# LOGGING SETUP
# =============================================================================

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("telegram_scraper")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    os.path.join(LOG_DIR, f"scrape_{TODAY}.log"),
    encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# =============================================================================
# SCRAPING FUNCTIONS
# =============================================================================

async def scrape_channel(
    client: TelegramClient,
    channel: str,
    writer: csv.writer,
    base_path: str,
    date_str: str,
    limit: int = 100,
    message_delay: float = DEFAULT_MESSAGE_DELAY,
    channel_delay: float = DEFAULT_CHANNEL_DELAY,
    max_retries: int = 3,
) -> int:
    channel_name = channel.strip('@')
    retries = 0
    while True:
        try:
            entity = await client.get_entity(channel)
            channel_title = entity.title
            messages = []

            # Image directory: data/raw/images/{channel_name}/
            channel_image_dir = os.path.join(base_path, "raw", "images", channel_name)
            os.makedirs(channel_image_dir, exist_ok=True)

            logger.info(f"Starting scrape of {channel} (limit={limit})")

            async for message in client.iter_messages(entity, limit=limit):
                image_path: Optional[str] = None
                has_media = message.media is not None

                if has_media and isinstance(message.media, MessageMediaPhoto):
                    filename = f"{message.id}.jpg"
                    image_path = os.path.join(channel_image_dir, filename)
                    # Only download if it doesn't exist already to save bandwidth
                    if not os.path.exists(image_path):
                        try:
                            await client.download_media(message.media, image_path)
                        except Exception as e:
                            logger.warning(f"Failed to download image: {e}")
                            image_path = None

                message_dict = {
                    "message_id": message.id,
                    "channel_name": channel_name,
                    "channel_title": channel_title,
                    "message_date": message.date.isoformat(),
                    "message_text": message.message or "",
                    "has_media": has_media,
                    "image_path": image_path,
                    "views": message.views or 0,
                    "forwards": message.forwards or 0,
                }

                writer.writerow([
                    message_dict["message_id"],
                    message_dict["channel_name"],
                    message_dict["channel_title"],
                    message_dict["message_date"],
                    message_dict["message_text"],
                    message_dict["has_media"],
                    message_dict["image_path"],
                    message_dict["views"],
                    message_dict["forwards"],
                ])

                messages.append(message_dict)

                if message_delay:
                    await asyncio.sleep(message_delay)

            write_channel_messages_json(
                base_path=base_path,
                date_str=date_str,
                channel_name=channel_name,
                messages=messages,
            )

            logger.info(f"Finished scraping {channel}: {len(messages)} messages saved")
            
            if channel_delay:
                await asyncio.sleep(channel_delay)
            return len(messages)

        except FloodWaitError as e:
            wait_seconds = int(getattr(e, "seconds", 0) or 0)
            wait_seconds = max(wait_seconds, 1)
            logger.warning(f"FloodWaitError for {channel}: sleeping {wait_seconds}s")
            await asyncio.sleep(wait_seconds)
            retries += 1
            if retries > max_retries:
                logger.error(f"Too many retries for {channel}. Skipping.")
                return 0
        except Exception as e:
            logger.error(f"Error scraping {channel}: {e}")
            return 0

async def scrape_all_channels(client, channels, base_path, limit, message_delay, channel_delay):
    await client.start()
    logger.info(f"Client authenticated. Scraping {len(channels)} channels...")
    
    csv_dir = os.path.join(base_path, "raw", "csv", TODAY)
    os.makedirs(csv_dir, exist_ok=True)
    
    csv_file_path = os.path.join(csv_dir, "telegram_data.csv")
    stats = {}
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['message_id', 'channel_name', 'channel_title', 'message_date', 
                         'message_text', 'has_media', 'image_path', 'views', 'forwards'])
        
        channel_counts = {}
        for channel in channels:
            logger.info(f"Scraping {channel}...")
            count = await scrape_channel(client, channel, writer, base_path, TODAY, limit, message_delay, channel_delay)
            stats[channel] = count
            channel_counts[channel.strip("@")] = count

        write_manifest(base_path=base_path, date_str=TODAY, channel_message_counts=channel_counts)
    
    return stats

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="data")
    parser.add_argument("--limit", type=int, default=100) # Default 100 messages
    parser.add_argument("--message-delay", type=float, default=DEFAULT_MESSAGE_DELAY)
    parser.add_argument("--channel-delay", type=float, default=DEFAULT_CHANNEL_DELAY)
    args = parser.parse_args()
    
    # Initialize Client
    client = TelegramClient("telegram_scraper_session", api_id, api_hash)
    
    # CHANNELS TO SCRAPE
    target_channels = [
        '@CheMed123',
        '@lobelia4cosmetics',
        '@tikvahpharma',
        '@tenamereja',
        '@DoctorsET' 
    ]
    
    async def main():
        async with client:
            await scrape_all_channels(client, target_channels, args.path, args.limit, args.message_delay, args.channel_delay)

    asyncio.run(main())