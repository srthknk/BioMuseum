#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend directory
load_dotenv(Path(__file__).parent / 'backend' / '.env')

async def fix_db():
    mongo_url = os.environ.get('MONGO_URL')
    if not mongo_url:
        print("No MONGO_URL found in .env")
        return
    
    print(f"Connecting to MongoDB...\n")
    client = AsyncIOMotorClient(mongo_url)
    db = client['biomuseum']
    videos_col = db['biotube_videos']
    
    # Update the two videos with correct YouTube thumbnails
    updates = [
        {
            'id': '4effec93-d5a1-46a2-b7c6-4d1c69f71ae4',
            'thumbnail': 'https://img.youtube.com/vi/DhTtsgUUI3Y/maxresdefault.jpg',
            'title': 'Testing'
        },
        {
            'id': '657949bb-b246-439d-b148-b3c83e05c48c',
            'thumbnail': 'https://img.youtube.com/vi/y_GVDbfaiwQ/maxresdefault.jpg',
            'title': 'Duroon Duroon'
        }
    ]
    
    print("Updating thumbnails...\n")
    for update in updates:
        result = await videos_col.update_one(
            {'id': update['id']},
            {'$set': {'thumbnail_url': update['thumbnail']}}
        )
        print(f"{update['title']}")
        if result.modified_count > 0:
            print(f"  ✓ Updated to: {update['thumbnail']}")
        else:
            print(f"  ? No change")
        print()
    
    client.close()
    print("✓ Done! Restart frontend to see changes.")

asyncio.run(fix_db())
