#!/usr/bin/env python3
"""
Test what the API is actually returning
"""

import asyncio
import os
import aiohttp

async def test_api():
    """Test the API endpoint"""
    
    backend_url = os.environ.get('BACKEND_URL', 'http://localhost:8000')
    api_url = f"{backend_url}/api/biotube/videos"
    
    print("\n" + "="*80)
    print("API RESPONSE TEST")
    print("="*80 + "\n")
    
    print(f"Testing endpoint: {api_url}\n")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                print(f"Status: {resp.status}\n")
                
                if resp.status == 200:
                    data = await resp.json()
                    
                    if isinstance(data, list):
                        print(f"Total videos returned: {len(data)}\n")
                        
                        if len(data) > 0:
                            # Show first video in detail
                            video = data[0]
                            print("First video details:")
                            print(f"  Title: {video.get('title', 'N/A')}")
                            print(f"  ID: {video.get('id', 'N/A')}")
                            print(f"  thumbnail_url: {repr(video.get('thumbnail_url', 'MISSING'))}")
                            print(f"  YouTube URL: {video.get('youtube_url', 'N/A')}")
                            print(f"  visibility: {video.get('visibility', 'N/A')}")
                            print()
                            
                            # Check all videos
                            with_thumb = sum(1 for v in data if v.get('thumbnail_url'))
                            print(f"Videos with thumbnail_url: {with_thumb}/{len(data)}")
                            
                            # Show thumbnail values
                            print("\nAll thumbnail_url values:")
                            for i, video in enumerate(data, 1):
                                thumb = video.get('thumbnail_url', '')
                                title = video.get('title', 'N/A')
                                print(f"  {i}. {title[:30]:30} | {thumb[:50] if thumb else 'EMPTY'}")
                        else:
                            print("No videos in database")
                    else:
                        print(f"Response type: {type(data)} (expected list)")
                        print(f"Response: {data}")
                else:
                    print(f"Error: {resp.status}")
                    text = await resp.text()
                    print(f"Response: {text}")
    except aiohttp.ClientConnectorError as e:
        print(f"❌ Connection error: {e}")
        print(f"   Is backend running on {backend_url}?")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_api())
