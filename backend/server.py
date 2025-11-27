from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import qrcode
import io
import base64
import hashlib
import json
import ssl
import asyncio
import socket
import dns.resolver

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB setup - REQUIRED, no fallback
MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    raise ValueError("ERROR: MONGO_URL environment variable is not set. MongoDB is required.")

db = None
organisms_collection = None
mongodb_connected = False

async def init_mongodb():
    global db, organisms_collection, mongodb_connected
    max_retries = 10
    retry_count = 0
    
    # Test DNS resolution first
    try:
        print("[INFO] Testing DNS resolution for MongoDB...")
        dns_records = await asyncio.get_event_loop().getaddrinfo(
            'ac-ojscwyo-shard-00-00.m30zoo4.mongodb.net', 27017
        )
        print(f"[OK] DNS resolved successfully: {len(dns_records)} records found")
    except Exception as e:
        print(f"[WARN] DNS resolution failed: {str(e)[:100]}")
    
    while retry_count < max_retries:
        try:
            print(f"[INFO] Attempting MongoDB connection (attempt {retry_count + 1}/{max_retries})...")
            
            # Build connection options with extended timeouts for Render
            client_kwargs = {
                'serverSelectionTimeoutMS': 60000,      # 60 seconds
                'connectTimeoutMS': 60000,               # 60 seconds
                'socketTimeoutMS': 60000,                # 60 seconds
                'maxPoolSize': 3,
                'minPoolSize': 0,
                'retryWrites': True,
                'retryReads': True,
                'ssl': True,
                'tlsAllowInvalidCertificates': False,
                'tlsAllowInvalidHostnames': False,
                'appName': 'biomuseum',
                'family': socket.AF_INET,  # Force IPv4
            }
            
            print(f"[INFO] MongoDB URL: {MONGO_URL[:50]}...")
            client = AsyncIOMotorClient(MONGO_URL, **client_kwargs)
            
            # Verify connection with extended timeout
            print("[INFO] Verifying MongoDB connection with ping command...")
            await asyncio.wait_for(client.admin.command('ping'), timeout=60)
            
            db = client[os.environ.get('DB_NAME', 'biomuseum')]
            organisms_collection = db.organisms
            
            # Test that we can actually query
            test_count = await organisms_collection.count_documents({})
            
            mongodb_connected = True
            print(f"[OK] ✓ Successfully connected to MongoDB! Found {test_count} organisms in database")
            return
            
        except asyncio.TimeoutError:
            retry_count += 1
            print(f"[WARN] MongoDB connection timeout (attempt {retry_count}/{max_retries})")
            if retry_count < max_retries:
                wait_time = min(15, 3 ** (retry_count - 1))  # Exponential backoff: 1, 3, 9, 15, 15...
                print(f"[INFO] Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
        except Exception as e:
            retry_count += 1
            error_msg = str(e)[:200]
            print(f"[WARN] MongoDB connection error (attempt {retry_count}/{max_retries}): {error_msg}")
            if retry_count < max_retries:
                wait_time = min(15, 3 ** (retry_count - 1))  # Exponential backoff: 1, 3, 9, 15, 15...
                print(f"[INFO] Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
    
    # FAIL HARD - No fallback to unreliable local storage
    error_msg = (
        "\n" + "="*80 + "\n"
        "[CRITICAL] ✗ MONGODB CONNECTION FAILED - APPLICATION WILL NOT START\n"
        "\n"
        "REQUIRED ACTIONS:\n"
        "1. Check MongoDB Atlas IP whitelist:\n"
        "   - Go to: https://cloud.mongodb.com\n"
        "   - Select 'biomuseum' cluster\n"
        "   - Go to 'Network Access' section\n"
        "   - Click 'ADD IP ADDRESS'\n"
        "   - Choose 'ALLOW ACCESS FROM ANYWHERE' and enter 0.0.0.0/0\n"
        "   - Click 'Confirm'\n"
        "   - Wait 5-10 minutes for the rule to apply\n"
        "\n"
        "2. Verify MongoDB cluster is running and healthy\n"
        "3. Check your internet connection and network settings\n"
        "4. Redeploy application after fixing the above\n"
        "\n"
        "NOTE: This application requires MongoDB. There is no fallback to\n"
        "unreliable local storage. All data must be persisted in MongoDB.\n"
        "="*80
    )
    print(error_msg)
    raise RuntimeError("MongoDB connection failed. Application startup aborted.")

# Define Models
class OrganismBase(BaseModel):
    name: str
    scientific_name: str
    classification: dict
    morphology: str
    physiology: str
    images: List[str] = []
    description: Optional[str] = ""

class Organism(OrganismBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    qr_code_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    qr_code_image: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class OrganismCreate(OrganismBase):
    pass

class OrganismUpdate(BaseModel):
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    classification: Optional[dict] = None
    morphology: Optional[str] = None
    physiology: Optional[str] = None
    images: Optional[List[str]] = None
    description: Optional[str] = None

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Database functions - MongoDB only (no JSON fallback)
async def get_organisms_list():
    return await organisms_collection.find().to_list(1000)

async def insert_organism(organism_data):
    await organisms_collection.insert_one(organism_data)

async def find_organism(organism_id):
    return await organisms_collection.find_one({"id": organism_id})

async def find_organism_by_qr(qr_code_id):
    return await organisms_collection.find_one({"qr_code_id": qr_code_id})

async def update_organism_db(organism_id, update_data):
    await organisms_collection.update_one({"id": organism_id}, {"$set": update_data})
    return await organisms_collection.find_one({"id": organism_id})

async def delete_organism_db(organism_id):
    result = await organisms_collection.delete_one({"id": organism_id})
    return result.deleted_count > 0

# Helper functions
def generate_qr_code(organism_id: str) -> str:
    frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
    qr_url = f"{frontend_url}/organism/{organism_id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

security = HTTPBearer()

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    expected_token = hashlib.sha256("admin:adminSBES".encode()).hexdigest()
    if credentials.credentials != expected_token:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    return True

# Create app and router
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Routes
@api_router.get("/")
async def root():
    return {"message": "Biology Museum API"}

@api_router.get("/organisms", response_model=List[Organism])
async def get_organisms():
    try:
        organisms = await get_organisms_list()
        return [Organism(**org) for org in organisms]
    except Exception as e:
        logging.error(f"Error fetching organisms: {e}")
        return []

@api_router.get("/organisms/{organism_id}", response_model=Organism)
async def get_organism(organism_id: str):
    try:
        organism = await find_organism(organism_id)
        if not organism:
            raise HTTPException(status_code=404, detail="Organism not found")
        return Organism(**organism)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching organism: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/organisms/qr/{qr_code_id}", response_model=Organism)
async def get_organism_by_qr(qr_code_id: str):
    try:
        organism = await find_organism_by_qr(qr_code_id)
        if not organism:
            raise HTTPException(status_code=404, detail="Organism not found")
        return Organism(**organism)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching organism by QR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/search")
async def search_organisms(q: str):
    try:
        organisms = await get_organisms_list()
        q_lower = q.lower()
        results = []
        for org in organisms:
            if (q_lower in org.get('name', '').lower() or 
                q_lower in org.get('scientific_name', '').lower()):
                results.append(Organism(**org))
        return results
    except Exception as e:
        logging.error(f"Error searching organisms: {e}")
        return []

@api_router.post("/admin/login", response_model=AdminToken)
async def admin_login(login: AdminLogin):
    if login.username == "admin" and login.password == "adminSBES":
        token = hashlib.sha256("admin:adminSBES".encode()).hexdigest()
        return AdminToken(access_token=token)
    raise HTTPException(status_code=401, detail="Invalid credentials")

@api_router.post("/admin/organisms", response_model=Organism)
async def create_organism(organism: OrganismCreate, _: bool = Depends(verify_admin_token)):
    try:
        organism_obj = Organism(**organism.dict())
        organism_obj.qr_code_image = generate_qr_code(organism_obj.id)
        
        await insert_organism(organism_obj.model_dump())
        return organism_obj
    except Exception as e:
        logging.error(f"Error creating organism: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating organism: {str(e)}")

@api_router.put("/admin/organisms/{organism_id}", response_model=Organism)
async def update_organism(organism_id: str, updates: OrganismUpdate, _: bool = Depends(verify_admin_token)):
    try:
        existing = await find_organism(organism_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Organism not found")
        
        update_data = {k: v for k, v in updates.dict().items() if v is not None}
        update_data['updated_at'] = datetime.utcnow().isoformat()
        
        updated_org = await update_organism_db(organism_id, update_data)
        if not updated_org:
            raise HTTPException(status_code=404, detail="Organism not found")
        return Organism(**updated_org)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating organism: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/admin/organisms/{organism_id}")
async def delete_organism(organism_id: str, _: bool = Depends(verify_admin_token)):
    try:
        deleted = await delete_organism_db(organism_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Organism not found")
        return {"message": "Organism deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting organism: {e}")
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins
    allow_credentials=False,  # must be FALSE when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    await init_mongodb()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
