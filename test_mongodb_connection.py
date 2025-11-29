#!/usr/bin/env python3
"""
Test MongoDB Connection Script
This script tests if the backend can connect to MongoDB locally
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from backend .env file
backend_dir = Path(__file__).parent / 'backend'
env_file = backend_dir / '.env'
load_dotenv(env_file)

# Import MongoDB client
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    print("[OK] ✓ Motor (async MongoDB driver) imported successfully")
except ImportError as e:
    print(f"[ERROR] ✗ Failed to import Motor: {e}")
    sys.exit(1)

async def test_mongodb_connection():
    """Test MongoDB connection with detailed output"""
    
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'biomuseum')
    
    if not mongo_url:
        print("[ERROR] ✗ MONGO_URL environment variable is not set")
        return False
    
    print(f"\n{'='*80}")
    print("[INFO] MongoDB Connection Test")
    print(f"{'='*80}")
    print(f"[INFO] MongoDB URL: {mongo_url[:70]}...")
    print(f"[INFO] Database Name: {db_name}")
    print(f"{'='*80}\n")
    
    try:
        print("[INFO] Creating MongoDB client...")
        client = AsyncIOMotorClient(
            mongo_url,
            serverSelectionTimeoutMS=30000,  # 30 seconds
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            maxPoolSize=3,
            minPoolSize=0,
            retryWrites=True,
            retryReads=True,
            ssl=True,
        )
        print("[OK] ✓ MongoDB client created")
        
        print("[INFO] Sending ping command to MongoDB...")
        await asyncio.wait_for(client.admin.command('ping'), timeout=30)
        print("[OK] ✓ MongoDB ping successful!")
        
        # Get the database
        db = client[db_name]
        print(f"[OK] ✓ Connected to database: {db_name}")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"[INFO] Collections in database: {collections if collections else 'No collections found'}")
        
        # Try to access organisms collection
        organisms_collection = db.organisms
        doc_count = await organisms_collection.count_documents({})
        print(f"[OK] ✓ Organisms collection has {doc_count} documents")
        
        # Close client
        client.close()
        
        print(f"\n{'='*80}")
        print("[SUCCESS] ✓✓✓ MongoDB connection test PASSED!")
        print(f"{'='*80}\n")
        return True
        
    except asyncio.TimeoutError:
        print(f"[ERROR] ✗ Connection timeout after 30 seconds")
        print("[HINT] MongoDB Atlas IP whitelist may not include your current IP")
        print("[HINT] Go to: https://cloud.mongodb.com > Network Access")
        return False
    except Exception as e:
        print(f"[ERROR] ✗ MongoDB connection failed: {str(e)}")
        print(f"[ERROR] Error type: {type(e).__name__}")
        return False

async def main():
    """Main function"""
    success = await test_mongodb_connection()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
