#!/usr/bin/env python3
"""
Debug script to test Biotube suggestions API
"""

import asyncio
from datetime import datetime
import uuid

# Simulating the models
class VideoSuggestion:
    def __init__(self, user_name, user_class, video_title, video_description="", 
                 id=None, status="pending", created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.user_name = user_name
        self.user_class = user_class
        self.video_title = video_title
        self.video_description = video_description
        self.status = status
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()
    
    def dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'user_class': self.user_class,
            'video_title': self.video_title,
            'video_description': self.video_description,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Test data
print("Testing VideoSuggestion model serialization...\n")

# Create a suggestion
suggestion = VideoSuggestion(
    user_name="Test User",
    user_class="12th",
    video_title="Lion Hunting Behavior",
    video_description="Amazing lion behavior"
)

print(f"Created suggestion:")
print(f"  ID: {suggestion.id}")
print(f"  User: {suggestion.user_name}")
print(f"  Class: {suggestion.user_class}")
print(f"  Title: {suggestion.video_title}")
print(f"  Status: {suggestion.status}")
print(f"  Created: {suggestion.created_at}\n")

# Test dict conversion
suggestion_dict = suggestion.dict()
print(f"Suggestion as dict:")
print(suggestion_dict)
print()

# Simulate what the API returns
print("Simulating API response with multiple suggestions:")
suggestions = []
for i in range(3):
    sugg = VideoSuggestion(
        user_name=f"User {i+1}",
        user_class=["11th", "12th", "B.Sc"][i],
        video_title=f"Video Title {i+1}",
        video_description=f"Description for video {i+1}"
    )
    suggestions.append(sugg.dict())

print(f"Number of suggestions: {len(suggestions)}\n")
for i, sugg in enumerate(suggestions):
    print(f"Suggestion {i+1}:")
    print(f"  - Video: {sugg['video_title']}")
    print(f"  - User: {sugg['user_name']} ({sugg['user_class']})")
    print(f"  - Status: {sugg['status']}")
    print()

# Test the conversion that happens in the backend
print("Testing backend conversion process:")
print("-" * 60)

# Simulate MongoDB document (with _id)
mongodb_doc = {
    '_id': 'mongodb_id_12345',
    'id': str(uuid.uuid4()),
    'user_name': 'Test User',
    'user_class': '12th',
    'video_title': 'Test Video',
    'video_description': 'Test Description',
    'status': 'pending',
    'created_at': datetime.utcnow().isoformat(),
    'updated_at': datetime.utcnow().isoformat()
}

print(f"Original MongoDB document:")
print(f"  Keys: {list(mongodb_doc.keys())}\n")

# Remove _id
sugg_copy = {k: v for k, v in mongodb_doc.items() if k != '_id'}
print(f"After removing _id:")
print(f"  Keys: {list(sugg_copy.keys())}\n")

# Convert to model and back to dict
try:
    sugg_obj = VideoSuggestion(**sugg_copy)
    result_dict = sugg_obj.dict()
    print(f"After VideoSuggestion conversion:")
    print(f"  Keys: {list(result_dict.keys())}")
    print(f"  Data: {result_dict}")
    print(f"\n✅ Conversion successful!")
except Exception as e:
    print(f"\n❌ Error during conversion: {e}")

print("\n" + "="*60)
print("If you're seeing 'no suggestions', check:")
print("1. Backend is running on http://localhost:8000")
print("2. MongoDB is running and has data in 'video_suggestions' collection")
print("3. Admin token is valid in the browser")
print("4. Check browser console for error messages")
print("5. Check backend server logs for errors")
print("="*60)
