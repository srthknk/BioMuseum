#!/usr/bin/env python3
"""
Diagnose thumbnail URL storage in MongoDB
"""

import asyncio
import os
from motor.motor_asyncio import AsyncClient

async def check_thumbnails():
    """Check if thumbnail_url is stored in videos"""
    
    # MongoDB connection
    mongo_url = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017')
    client = AsyncClient(mongo_url)
    db = client['biomuseum']
    
    try:
        videos_collection = db['biotube_videos']
        
        # Get all videos
        videos = await videos_collection.find({}).to_list(None)
        
        print("\n" + "="*70)
        print("THUMBNAIL URL DIAGNOSTIC")
        print("="*70 + "\n")
        
        if not videos:
            print("No videos found in database!\n")
            return
        
        print(f"Total videos: {len(videos)}\n")
        
        for idx, video in enumerate(videos, 1):
            print(f"Video {idx}: {video.get('title', 'N/A')}")
            print(f"  - ID: {video.get('id', 'N/A')}")
            print(f"  - Thumbnail URL: {video.get('thumbnail_url', 'MISSING')}")
            print(f"  - Has thumbnail_url field: {'thumbnail_url' in video}")
            
            # Check if it's a valid URL
            thumb = video.get('thumbnail_url', '')
            if thumb and thumb.startswith('http'):
                print(f"  - Status: VALID URL")
            elif thumb == '':
                print(f"  - Status: EMPTY STRING")
            else:
                print(f"  - Status: INVALID (no http)")
            print()
        
        print("="*70 + "\n")
        
        # Count videos with valid thumbnails
        with_thumb = sum(1 for v in videos if v.get('thumbnail_url', '').startswith('http'))
        print(f"Summary:")
        print(f"  - Videos with valid thumbnails: {with_thumb}/{len(videos)}")
        print(f"  - Videos missing thumbnails: {len(videos) - with_thumb}/{len(videos)}\n")
        
    except Exception as e:
        print(f"Error: {e}\n")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_thumbnails())
