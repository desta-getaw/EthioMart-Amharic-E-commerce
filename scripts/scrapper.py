# scripts/scrapper.py

import os
import re
import asyncio
import pandas as pd
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors.rpcerrorlist import ChannelInvalidError, ChannelPrivateError

# Load environment variables
load_dotenv()

# Get credentials
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE_NUMBER")

if not all([api_id, api_hash, phone]):
    raise ValueError("Missing API_ID, API_HASH, or PHONE_NUMBER in .env file.")

# Channels to scrape
channels_to_scrape = [
    'ZemenExpress',
    'nevacomputer',
    'qnashcom',
    'helloomarketethiopia',
    'modernshoppingcenter'
]

async def fetch_messages(client, channel_identifier, limit=300):
    """Fetch messages from a single Telegram channel."""
    all_messages = []
    try:
        channel_entity = await client.get_entity(channel_identifier)
        async for message in client.iter_messages(channel_entity, limit=limit):
            if message.text:
                all_messages.append({
                    'channel_name': getattr(channel_entity, 'username', str(channel_identifier)),
                    'message_id': message.id,
                    'timestamp': message.date,
                    'text_original': message.text,
                    'views': message.views if message.views else 0,
                    'has_image': message.photo is not None
                })
        print(f"✅ Scraped {len(all_messages)} messages from @{channel_identifier}")
        return all_messages

    except (ChannelInvalidError, ValueError):
        print(f"❌ Channel '@{channel_identifier}' not found or invalid.")
    except ChannelPrivateError:
        print(f"🔒 Channel '@{channel_identifier}' is private. Join required.")
    except Exception as e:
        print(f"⚠️ Error fetching from @{channel_identifier}: {e}")
    return []

async def main(limit=300):
    """Run the scraping for all channels."""
    all_scraped_data = []
    async with TelegramClient('session_name', api_id, api_hash) as client:
        print("🔌 Connected to Telegram. Scraping...")
        for channel in channels_to_scrape:
            print(f"--- Processing: {channel} ---")
            channel_data = await fetch_messages(client, channel, limit)
            all_scraped_data.extend(channel_data)

    if not all_scraped_data:
        print("⚠️ No data collected.")
        return pd.DataFrame()

    df = pd.DataFrame(all_scraped_data)
    df.to_csv('data/scraped_data.csv', index=False, encoding='utf-8-sig')
    print(f"📁 Saved raw scraped data to 'data/scraped_data.csv'")
    return df

def clean_text(text):
    """Cleans Telegram text messages for NER or NLP."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+|www\S+|t\.me/\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[💥📌💵✅👉📍📞☎️👇✨✔®©™❤🔥]', '', text)
    text = re.sub(r'[\n\r\s]+', ' ', text).strip()
    return text

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Adds cleaned text column and saves result."""
    df['text_cleaned'] = df['text_original'].apply(clean_text)
    df.to_csv('data/preprocessed_data.csv', index=False, encoding='utf-8-sig')
    print("✅ Preprocessing done. Saved to 'data/preprocessed_data.csv'")
    return df
