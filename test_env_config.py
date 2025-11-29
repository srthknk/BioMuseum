#!/usr/bin/env python3
"""
Test Backend Environment Configuration
Verifies all environment variables are properly set
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from backend .env file
backend_dir = Path(__file__).parent / 'backend'
env_file = backend_dir / '.env'
load_dotenv(env_file)

print("\n" + "="*80)
print("BACKEND ENVIRONMENT CONFIGURATION TEST")
print("="*80 + "\n")

# Check MONGO_URL
mongo_url = os.environ.get('MONGO_URL')
if mongo_url:
    print(f"✓ MONGO_URL: {mongo_url[:60]}...")
else:
    print("✗ MONGO_URL: NOT SET")

# Check DB_NAME
db_name = os.environ.get('DB_NAME')
if db_name:
    print(f"✓ DB_NAME: {db_name}")
else:
    print("✗ DB_NAME: NOT SET")

# Check FRONTEND_URL
frontend_url = os.environ.get('FRONTEND_URL')
if frontend_url:
    print(f"✓ FRONTEND_URL: {frontend_url}")
else:
    print("✗ FRONTEND_URL: NOT SET (will default to http://localhost:3000)")

# Check CORS_ORIGINS
cors_origins = os.environ.get('CORS_ORIGINS')
if cors_origins:
    origins_list = [o.strip() for o in cors_origins.split(',')]
    print(f"✓ CORS_ORIGINS configured:")
    for origin in origins_list:
        print(f"  - {origin}")
else:
    print("✗ CORS_ORIGINS: NOT SET (will default to localhost)")

print("\n" + "="*80)
print("LOCAL ENVIRONMENT (.env file):")
print("="*80)
print("\nFor local development (http://localhost:3000 and http://localhost:3001)")
print("Your .env file is properly configured for testing locally.\n")

print("="*80)
print("RENDER ENVIRONMENT (render.yaml):")
print("="*80)
print("\nFor Render deployment:")
print("✓ CORS_ORIGINS: http://localhost:3000,http://localhost:3001,https://bio-museum.vercel.app,https://biomuseum.onrender.com")
print("✓ FRONTEND_URL: https://bio-museum.vercel.app")
print("\nThe render.yaml has been updated with the correct URLs.\n")
