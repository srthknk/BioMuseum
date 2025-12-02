#!/usr/bin/env python3
"""Analyze MongoDB database size and capacity"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')

try:
    client = MongoClient(mongo_url)
    db = client['biotube_db']
    
    # Get database stats
    stats = db.command('dbStats')
    
    print('='*60)
    print('MONGODB DATABASE SIZE ANALYSIS')
    print('='*60)
    print(f'Total Database Size: {stats["dataSize"] / (1024**2):.2f} MB')
    print(f'Storage Size: {stats["storageSize"] / (1024**2):.2f} MB')
    print(f'Available Space: 512 MB')
    print(f'Used Space: {stats["storageSize"] / (1024**2):.2f} MB')
    print(f'Remaining Space: {512 - (stats["storageSize"] / (1024**2)):.2f} MB')
    print()
    
    # Check collections
    print('COLLECTIONS:')
    for collection_name in db.list_collection_names():
        coll = db[collection_name]
        count = coll.count_documents({})
        size = db.command('collStats', collection_name)['size']
        avg_doc = size / count if count > 0 else 0
        print(f'  {collection_name}: {count} docs, {size / 1024:.2f} KB, avg {avg_doc / 1024:.2f} KB per doc')
    
    print()
    print('ESTIMATED CAPACITY:')
    
    # Check videos collection
    videos = db['biotube_videos']
    video_count = videos.count_documents({})
    if video_count > 0:
        video_size = db.command('collStats', 'biotube_videos')['size']
        avg_video_size = video_size / video_count
        remaining_mb = 512 - (stats['storageSize'] / (1024**2))
        remaining_bytes = remaining_mb * (1024**2)
        videos_remaining = int(remaining_bytes / avg_video_size)
        print(f'  Current videos: {video_count}')
        print(f'  Avg video size: {avg_video_size / 1024:.2f} KB')
        print(f'  Videos we can add: ~{videos_remaining} more')
    
    # Check organisms collection
    organisms = db['organisms']
    org_count = organisms.count_documents({})
    if org_count > 0:
        org_size = db.command('collStats', 'organisms')['size']
        avg_org_size = org_size / org_count
        remaining_mb = 512 - (stats['storageSize'] / (1024**2))
        remaining_bytes = remaining_mb * (1024**2)
        org_remaining = int(remaining_bytes / avg_org_size)
        print(f'  Current organisms: {org_count}')
        print(f'  Avg organism size: {avg_org_size / 1024:.2f} KB')
        print(f'  Organisms we can add: ~{org_remaining} more')
    
    print()
    print('='*60)
    print('CAPACITY ESTIMATE:')
    print('='*60)
    
    # Conservative estimate
    if video_count > 0:
        print(f'✓ Additional videos at current rate: ~{videos_remaining}')
    if org_count > 0:
        print(f'✓ Additional organisms at current rate: ~{org_remaining}')
    
    client.close()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
