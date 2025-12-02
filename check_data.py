#!/usr/bin/env python3
import requests

response = requests.get('http://localhost:8000/api/biotube/videos')
videos = response.json()

for video in videos:
    print(f"\nVideo: {video.get('title')}")
    print(f"  ID: {video.get('id')}")
    print(f"  YouTube URL: {video.get('youtube_url')}")
    print(f"  Thumbnail URL: {video.get('thumbnail_url')}")
    print(f"  QR Code: {('YES' if video.get('qr_code') else 'NO')}")
