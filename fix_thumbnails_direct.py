#!/usr/bin/env python3
import requests
import re

# Get all videos
response = requests.get('http://localhost:8000/api/biotube/videos')
videos = response.json()

print("\nFixing thumbnails...\n")

for video in videos:
    youtube_url = video.get('youtube_url', '')
    video_id = video.get('id')
    title = video.get('title')
    
    # Extract YouTube video ID
    match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)', youtube_url)
    if match:
        yt_id = match.group(1)
        new_thumbnail = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg"
        
        print(f"{title}: {yt_id}")
        print(f"  New URL: {new_thumbnail}")
        
        # Update via API
        try:
            update_response = requests.put(
                f'http://localhost:8000/api/admin/biotube/videos/{video_id}',
                json={'thumbnail_url': new_thumbnail},
                headers={'Authorization': f'Bearer YOUR_ADMIN_TOKEN'}
            )
            print(f"  Status: {update_response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
        print()
