#!/usr/bin/env python3
"""
Diagnostic script to check Biotube suggestions database
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logging.basicConfig(level=logging.INFO)

async def diagnose_database():
    print("\n" + "="*70)
    print("🔍 BIOTUBE SUGGESTIONS DATABASE DIAGNOSTIC")
    print("="*70 + "\n")
    
    # Get connection details
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'biomuseum')
    
    print(f"📍 Connection Details:")
    print(f"   MongoDB URL: {mongo_url}")
    print(f"   Database Name: {db_name}")
    print()
    
    try:
        # Connect to MongoDB
        print("🔗 Connecting to MongoDB...")
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        print("✅ Connection successful!\n")
        
        # Get database
        db = client[db_name]
        
        # List all collections
        print("📚 Collections in database:")
        collections = await db.list_collection_names()
        for col in collections:
            print(f"   - {col}")
        print()
        
        # Check video_suggestions collection
        if 'video_suggestions' not in collections:
            print("❌ video_suggestions collection NOT FOUND!")
            print("   Suggestions will not work until this collection is created.")
            print()
        else:
            print("✅ video_suggestions collection found\n")
            
            # Get collection stats
            video_suggestions_col = db['video_suggestions']
            count = await video_suggestions_col.count_documents({})
            
            print(f"📊 Collection Statistics:")
            print(f"   Total documents: {count}")
            
            if count == 0:
                print("   ⚠️  Collection is empty!")
                print("      Go to /biotube page and submit a suggestion first")
            else:
                print(f"   ✅ Documents exist\n")
                
                # Count by status
                pending = await video_suggestions_col.count_documents({"status": "pending"})
                reviewed = await video_suggestions_col.count_documents({"status": "reviewed"})
                added = await video_suggestions_col.count_documents({"status": "added"})
                dismissed = await video_suggestions_col.count_documents({"status": "dismissed"})
                
                print(f"📈 Breakdown by Status:")
                print(f"   Pending:   {pending}")
                print(f"   Reviewed:  {reviewed}")
                print(f"   Added:     {added}")
                print(f"   Dismissed: {dismissed}")
                print()
                
                # Show sample document
                print("📋 Sample Suggestion Document:")
                sample = await video_suggestions_col.find_one()
                if sample:
                    print(f"   _id: {sample.get('_id')}")
                    print(f"   id: {sample.get('id')}")
                    print(f"   user_name: {sample.get('user_name')}")
                    print(f"   user_class: {sample.get('user_class')}")
                    print(f"   video_title: {sample.get('video_title')}")
                    print(f"   video_description: {sample.get('video_description')}")
                    print(f"   status: {sample.get('status')}")
                    print(f"   created_at: {sample.get('created_at')}")
                    print(f"   updated_at: {sample.get('updated_at')}")
                    print()
                    
                    # Check if all required fields are present
                    required_fields = ['id', 'user_name', 'user_class', 'video_title', 'status', 'created_at', 'updated_at']
                    missing = [f for f in required_fields if f not in sample]
                    
                    if missing:
                        print(f"   ❌ Missing fields: {missing}")
                        print(f"      This will cause API to fail!")
                    else:
                        print(f"   ✅ All required fields present")
        
        print()
        
        # Test the API endpoint response format
        print("🧪 Testing Response Format:")
        video_suggestions_col = db['video_suggestions']
        test_docs = await video_suggestions_col.find().limit(2).to_list(2)
        
        if test_docs:
            print(f"   Sample response format:")
            for i, doc in enumerate(test_docs):
                print(f"\n   Document {i+1}:")
                for key, value in doc.items():
                    if key != '_id':
                        print(f"      {key}: {value}")
        
        print("\n" + "="*70)
        print("✅ DIAGNOSTIC COMPLETE")
        print("="*70 + "\n")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\n⚠️  Make sure:")
        print(f"   1. MongoDB is running")
        print(f"   2. Connection string is correct: {mongo_url}")
        print(f"   3. Database '{db_name}' exists")
        print()

if __name__ == "__main__":
    asyncio.run(diagnose_database())
