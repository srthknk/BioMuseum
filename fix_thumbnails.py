#!/usr/bin/env python3
"""
Fix missing thumbnail URLs using pymongo (sync version)
"""

import os
import re
from pymongo import MongoClient

def fix_thumbnails():
    """Add YouTube thumbnails to videos missing thumbnail_url"""
    
    mongo_url = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017')
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
    
    try:
        # Test connection
        client.admin.command('ping')
        db = client['biomuseum']
        videos_collection = db['biotube_videos']
        
        # Find all videos
        videos = list(videos_collection.find({}))
        
        print("\n" + "="*70)
        print("THUMBNAIL URL FIX - MongoDB Migration")
        print("="*70 + "\n")
        
        if not videos:
            print("No videos found in database!\n")
            return
        
        # Extract YouTube video ID
        def get_youtube_id(youtube_url):
            """Extract video ID from YouTube URL"""
            patterns = [
                r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
                r'youtube\.com\/embed/([^&\n?#]+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, youtube_url)
                if match:
                    return match.group(1)
            return None
        
        updated = 0
        skipped = 0
        failed = 0
        
        print(f"Processing {len(videos)} videos...\n")
        
        for video in videos:
            title = video.get('title', 'Unknown')[:40]
            video_id = video.get('id', 'N/A')
            youtube_url = video.get('youtube_url', '')
            current_thumbnail = video.get('thumbnail_url', '')
            
            print(f"{title:40} | ", end='')
            
            # Check if thumbnail_url is missing or empty
            if not current_thumbnail or current_thumbnail == '':
                yt_id = get_youtube_id(youtube_url)
                if yt_id:
                    thumbnail_url = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg"
                    
                    try:
                        result = videos_collection.update_one(
                            {'id': video_id},
                            {'$set': {'thumbnail_url': thumbnail_url}}
                        )
                        
                        if result.modified_count > 0:
                            print("UPDATED")
                            updated += 1
                        else:
                            print("SKIPPED")
                            skipped += 1
                    except Exception as e:
                        print(f"FAILED: {e}")
                        failed += 1
                else:
                    print("FAILED (no YT ID)")
                    failed += 1
            else:
                print("OK")
                skipped += 1
        
        print("\n" + "="*70)
        print(f"Results:")
        print(f"  Updated: {updated}")
        print(f"  Skipped: {skipped}")
        print(f"  Failed: {failed}")
        print(f"  Total: {len(videos)}\n")
        
        if updated > 0:
            print("✓ Videos updated! Restart the backend to see changes.\n")
        
    except Exception as e:
        print(f"Error: {e}\n")
        print("Make sure MongoDB is running!\n")
    finally:
        client.close()

if __name__ == "__main__":
    fix_thumbnails()
