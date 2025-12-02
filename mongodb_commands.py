#!/usr/bin/env python3
"""
Direct MongoDB update - fix thumbnail URLs
"""
import re

# Videos that need fixing
videos_to_fix = [
    {
        'id': '4effec93-d5a1-46a2-b7c6-4d1c69f71ae4',
        'title': 'Testing',
        'youtube_url': 'https://youtu.be/DhTtsgUUI3Y?list=RDDhTtsgUUI3Y'
    },
    {
        'id': '657949bb-b246-439d-b148-b3c83e05c48c',
        'title': 'Duroon Duroon',
        'youtube_url': 'https://youtu.be/y_GVDbfaiwQ?list=RDy_GVDbfaiwQ'
    }
]

print("\nThumbnail URLs to set:\n")

for video in videos_to_fix:
    match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)', video['youtube_url'])
    if match:
        yt_id = match.group(1)
        thumbnail_url = f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg"
        
        print(f"Video: {video['title']}")
        print(f"  YouTube ID: {yt_id}")
        print(f"  Thumbnail: {thumbnail_url}")
        print(f"\nMongoDB Update Command:")
        print(f'  db.biotube_videos.updateOne(')
        print(f'    {{ id: "{video["id"]}" }},')
        print(f'    {{ $set: {{ thumbnail_url: "{thumbnail_url}" }} }}')
        print(f'  )\n')
