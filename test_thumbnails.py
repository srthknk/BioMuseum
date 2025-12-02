#!/usr/bin/env python3
import requests
import json

response = requests.get('http://localhost:8000/api/biotube/videos')
if response.status_code == 200:
    videos = response.json()
    print(f"\nTotal videos: {len(videos)}\n")
    for i, video in enumerate(videos[:3], 1):
        print(f"Video {i}: {video.get('title')}")
        print(f"  Thumbnail: {video.get('thumbnail_url', 'MISSING')[:60]}")
        print()
else:
    print(f"Error: {response.status_code}")
