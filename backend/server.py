from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import sys
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

# Google Generative AI - with graceful fallback
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    genai = None

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB setup - REQUIRED, no fallback
MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    raise ValueError("ERROR: MONGO_URL environment variable is not set. MongoDB is required.")

# Google Gemini API Setup
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY and HAS_GENAI:
    genai.configure(api_key=GEMINI_API_KEY)
    print("[OK] Google Gemini API configured successfully")
else:
    print("[WARN] GEMINI_API_KEY not set - AI organism feature will not work")

db = None
organisms_collection = None
mongodb_connected = False

async def init_mongodb():
    global db, organisms_collection, mongodb_connected
    max_retries = 15  # Increased from 10 to 15
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
                'serverSelectionTimeoutMS': 120000,     # 120 seconds
                'connectTimeoutMS': 120000,              # 120 seconds
                'socketTimeoutMS': 120000,               # 120 seconds
                'maxPoolSize': 3,
                'minPoolSize': 0,
                'retryWrites': True,
                'retryReads': True,
                'ssl': True,
                'tlsAllowInvalidCertificates': False,
                'tlsAllowInvalidHostnames': False,
                'appName': 'biomuseum',
            }
            
            print(f"[INFO] MongoDB URL: {MONGO_URL[:50]}...")
            client = AsyncIOMotorClient(MONGO_URL, **client_kwargs)
            
            # Verify connection with extended timeout
            print("[INFO] Verifying MongoDB connection with ping command...")
            await asyncio.wait_for(client.admin.command('ping'), timeout=120)
            
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
                wait_time = min(20, 5 ** (retry_count - 1) // 50)  # Increased wait time
                print(f"[INFO] Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
        except Exception as e:
            retry_count += 1
            error_msg = str(e)[:200]
            print(f"[WARN] MongoDB connection error (attempt {retry_count}/{max_retries}): {error_msg}")
            if retry_count < max_retries:
                wait_time = min(20, 5 ** (retry_count - 1) // 50)  # Increased wait time
                print(f"[INFO] Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
    
    # FAIL HARD - No fallback to unreliable local storage
    error_msg = (
        "\n" + "="*80 + "\n"
        "[CRITICAL] ✗ MONGODB CONNECTION FAILED - APPLICATION WILL NOT START\n"
        "\n"
        "REQUIRED ACTIONS:\n"
        "1. Configure MongoDB Atlas IP Whitelist IMMEDIATELY:\n"
        "   - Go to: https://cloud.mongodb.com\n"
        "   - Log in with your account\n"
        "   - Select 'biomuseum' cluster\n"
        "   - Go to 'Network Access' in the left sidebar\n"
        "   - Click 'ADD IP ADDRESS'\n"
        "   - Click 'ALLOW ACCESS FROM ANYWHERE'\n"
        "   - Enter 0.0.0.0/0 (allows all IPs)\n"
        "   - Click 'Confirm'\n"
        "   - WAIT 5-10 MINUTES for the rule to apply\n"
        "\n"
        "2. Verify your MongoDB cluster is running:\n"
        "   - Go to MongoDB Atlas Dashboard\n"
        "   - Check cluster status is 'Running'\n"
        "   - No alerts or warnings\n"
        "\n"
        "3. After whitelist is configured, REDEPLOY on Render:\n"
        "   - Go to your Render dashboard\n"
        "   - Click 'Manual Deploy' or push new commit to GitHub\n"
        "\n"
        "Current credentials:\n"
        f"   - URL: {MONGO_URL[:60]}...\n"
        f"   - Database: {os.environ.get('DB_NAME', 'biomuseum')}\n"
        "\n"
        "NOTE: This application requires MongoDB. There is NO fallback\n"
        "to local storage. All data MUST persist in MongoDB.\n"
        "="*80
    )
    print(error_msg)
    raise RuntimeError("MongoDB connection failed after 15 retry attempts. See error message above.")

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

# Root endpoint for health checks and load balancers
@app.get("/")
async def root_health():
    return {"status": "ok", "service": "Biology Museum API", "version": "1.0.0"}

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

# Pydantic model for AI organism generation request
class OrganismNameRequest(BaseModel):
    organism_name: str = Field(..., description="Common name of the organism")

# AI Endpoint - Generate organism data using Gemini
@api_router.post("/admin/organisms/ai-complete")
async def generate_organism_data_ai(request: OrganismNameRequest):
    """
    Generate organism data using Google Gemini AI.
    Admin only needs to provide the organism name.
    """
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="AI feature is not configured. GEMINI_API_KEY is missing.")
    
    try:
        organism_name = request.organism_name.strip()
        if not organism_name:
            raise HTTPException(status_code=400, detail="Organism name cannot be empty")
        
        # Create prompt for Gemini
        prompt = f"""You are an expert biologist and zoologist. I need you to provide detailed biological information about "{organism_name}".

Please provide the information in JSON format ONLY (no markdown, no explanations). Return ONLY valid JSON:

{{
    "name": "Common name of the organism",
    "scientific_name": "Scientific name (binomial nomenclature)",
    "classification": {{
        "kingdom": "Kingdom",
        "phylum": "Phylum",
        "class": "Class",
        "order": "Order",
        "family": "Family",
        "genus": "Genus",
        "species": "Species"
    }},
    "morphology": "Physical description including size, color, distinctive features (2-3 sentences)",
    "physiology": "How the organism functions, internal systems, key biological processes (2-3 sentences)",
    "general_description": "General overview of the organism, its habitat, and interesting facts (2-3 sentences)",
    "habitat": "Where it lives and environmental preferences",
    "behavior": "Behavioral characteristics if applicable",
    "diet": "What it eats (if applicable)",
    "conservation_status": "Conservation status (e.g., Least Concern, Endangered, etc.)"
}}

Be accurate and scientific. If you cannot find specific information, make reasonable educated guesses based on the organism's taxonomy.
Make sure the JSON is valid and properly formatted."""

        # Call Gemini API
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        # Parse the response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        organism_data = json.loads(response_text)
        
        # Validate required fields
        required_fields = ['name', 'scientific_name', 'classification', 'morphology', 'physiology', 'general_description']
        for field in required_fields:
            if field not in organism_data:
                organism_data[field] = ""
        
        # Return the generated data
        return {
            "success": True,
            "data": organism_data,
            "source": "ai_generated"
        }
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {str(e)}")
    except Exception as e:
        logging.error(f"Error generating organism data with AI: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating organism data: {str(e)}")

@api_router.post("/admin/organisms/ai-generate-images")
async def generate_organism_images_ai(request: dict):
    """
    Generate HD images for an organism using Unsplash API or similar.
    Since we don't have access to image generation APIs directly,
    we'll provide high-quality image URLs from open sources.
    """
    try:
        organism_name = request.get('organism_name', '').strip()
        count = request.get('count', 4)
        
        if not organism_name:
            raise HTTPException(status_code=400, detail="Organism name cannot be empty")
        
        if count > 10:
            count = 10  # Limit to 10 images
        
        # For now, we'll return placeholder images from Unsplash API
        # In production, you would integrate with actual image generation or stock photo APIs
        import urllib.parse
        
        # Create URLs for high-quality images from Unsplash
        images = []
        query = urllib.parse.quote(organism_name)
        
        # Generate URLs for different image variations
        image_urls = [
            f"https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=80&auto=format&crop=entropy&cs=tinysrgb",  # Nature
            f"https://images.unsplash.com/photo-1489330911046-c894fdcc538d?w=800&q=80&auto=format&crop=entropy&cs=tinysrgb",  # Wildlife
            f"https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&q=80&auto=format&crop=entropy&cs=tinysrgb",  # Nature
            f"https://images.unsplash.com/photo-1518531933037-91b2f0f0767a?w=800&q=80&auto=format&crop=entropy&cs=tinysrgb",  # Animals
            f"https://images.unsplash.com/photo-1511218e0f31-ad25f1d80a4e?w=800&q=80&auto=format&crop=entropy&cs=tinysrgb",  # Nature close-up
            f"https://images.unsplash.com/photo-1446768500-6b1b4ec3f1c3?w=800&q=80&auto=format&crop=entropy&cs=tinysrgb",  # Wildlife
        ]
        
        # Return requested number of images
        for i in range(min(count, len(image_urls))):
            images.append(image_urls[i])
        
        # If we need more, repeat some
        while len(images) < count:
            images.append(image_urls[len(images) % len(image_urls)])
        
        return {
            "success": True,
            "images": images[:count],
            "organism_name": organism_name,
            "count": len(images[:count]),
            "source": "unsplash_hd"
        }
        
    except Exception as e:
        logging.error(f"Error generating organism images: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating images: {str(e)}")

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

# Parse CORS origins from environment variable
cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001').split(',')
cors_origins = [origin.strip() for origin in cors_origins]  # Remove whitespace

print(f"[INFO] CORS Origins configured: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
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
