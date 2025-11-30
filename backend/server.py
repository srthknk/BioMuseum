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
import requests
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
suggestions_collection = None
mongodb_connected = False

async def init_mongodb():
    global db, organisms_collection, suggestions_collection, mongodb_connected
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
            suggestions_collection = db.suggestions
            
            # Test that we can actually query
            test_count = await organisms_collection.count_documents({})
            test_suggestions = await suggestions_collection.count_documents({})
            
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

class Suggestion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_name: str
    organism_name: str
    description: Optional[str] = ""
    educational_level: str  # 11th, 12th, B.Sc 1st, B.Sc 2nd, B.Sc 3rd, B.Sc 4th, BCS, BCA, B.Voc, Teacher, etc.
    status: str = "pending"  # pending, approved, rejected
    ai_verification: Optional[dict] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class SuggestionCreate(BaseModel):
    user_name: str
    organism_name: str
    description: Optional[str] = ""
    educational_level: str  # Required field

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
    """
    Verify admin token from either username/password or Google OAuth login.
    Accepts tokens from:
    1. Username/password: admin:adminSBES
    2. Google OAuth: admin:{authorized_email}
    """
    received_token = credentials.credentials
    
    # Check for username/password token
    expected_token_admin = hashlib.sha256("admin:adminSBES".encode()).hexdigest()
    if received_token == expected_token_admin:
        return True
    
    # Check for Google OAuth tokens from authorized emails
    authorized_emails_str = os.environ.get('AUTHORIZED_ADMIN_EMAILS', '')
    if authorized_emails_str:
        authorized_emails = [e.strip().lower() for e in authorized_emails_str.split(',')]
        for email in authorized_emails:
            expected_token_email = hashlib.sha256(f"admin:{email}".encode()).hexdigest()
            if received_token == expected_token_email:
                return True
    
    # If no token matches, raise error
    raise HTTPException(status_code=401, detail="Invalid admin token")

# Create app and router
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Async function to fetch images from web
async def get_images_from_web_async(organism_name: str, max_images: int = 5) -> List[str]:
    """
    Fetch images of an organism from Bing Image Search
    Returns list of base64 encoded images
    """
    try:
        images = []
        search_url = f"https://www.bing.com/images/search?q={organism_name}&qft=+filterui:imagesize-large"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Try to fetch from Wikimedia Commons API first (more reliable)
        try:
            wiki_url = f"https://commons.wikimedia.org/w/api.php?action=query&list=allimages&aisort=timestamp&aidir=descending&aifrom={organism_name}&ailimit=10&format=json"
            response = requests.get(wiki_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'query' in data and 'allimages' in data['query']:
                    for img in data['query']['allimages'][:max_images]:
                        if 'url' in img:
                            img_url = img['url']
                            # Download and convert to base64
                            try:
                                img_response = requests.get(img_url, headers=headers, timeout=10)
                                if img_response.status_code == 200:
                                    base64_img = base64.b64encode(img_response.content).decode('utf-8')
                                    images.append(f"data:image/jpeg;base64,{base64_img}")
                            except Exception as e:
                                logging.warning(f"Could not fetch image {img_url}: {e}")
                                continue
        except Exception as e:
            logging.warning(f"Wikimedia API error: {e}")
        
        # If we don't have enough images, try a simple placeholder approach
        if len(images) < max_images:
            # Create placeholder images with organism name
            for i in range(max_images - len(images)):
                # Create a simple colored placeholder
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
                color = colors[i % len(colors)]
                # Return a simple placeholder (you could use a real image generation service here)
                images.append(f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Crect width='300' height='300' fill='{color}'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white'{organism_name[:20]}</text>%3E%3C/svg%3E")
        
        return images[:max_images]
        
    except Exception as e:
        logging.warning(f"Error fetching images for {organism_name}: {e}")
        return []

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
        error_msg = "AI feature is not configured. GEMINI_API_KEY is missing. Please set the GEMINI_API_KEY environment variable in your .env file or on Render dashboard."
        logging.error(error_msg)
        raise HTTPException(status_code=503, detail=error_msg)
    
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


def get_search_terms_from_gemini(organism_name: str):
    """Use Gemini to generate better search terms for organism images."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f'Given the organism name "{organism_name}", generate 3-5 search keywords that would find relevant images on Unsplash. Each keyword should be a single word or short phrase. Return ONLY the keywords as comma-separated list. Example: "cobra, snake, reptile"'
        response = model.generate_content(prompt)
        search_terms = [term.strip() for term in response.text.split(',')]
        return search_terms
    except Exception as e:
        return [organism_name.lower()]

def search_unsplash_images(organism_name: str, count: int = 6):
    """Search Unsplash API for organism images using AI-enhanced search terms."""
    UNSPLASH_ACCESS_KEY = "vQ_yvjIskYKmvpXywThJ4u5kBjRzTAk1kDZkwYhwDbY"
    UNSPLASH_API_URL = "https://api.unsplash.com"
    images = []
    search_terms = get_search_terms_from_gemini(organism_name)
    search_terms.insert(0, organism_name)
    
    for query in search_terms:
        if len(images) >= count:
            break
        try:
            response = requests.get(
                f"{UNSPLASH_API_URL}/search/photos",
                params={
                    'query': query,
                    'client_id': UNSPLASH_ACCESS_KEY,
                    'per_page': 10,
                    'orientation': 'landscape'
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                for result in data.get('results', []):
                    if len(images) >= count:
                        break
                    img_url = result.get('urls', {}).get('regular', '')
                    if img_url and img_url not in images:
                        if '?' in img_url:
                            img_url += '&w=800&q=90'
                        else:
                            img_url += '?w=800&q=90'
                        images.append(img_url)
        except Exception as e:
            continue
    
    if not images:
        try:
            response = requests.get(
                f"{UNSPLASH_API_URL}/search/photos",
                params={
                    'query': organism_name,
                    'client_id': UNSPLASH_ACCESS_KEY,
                    'per_page': 6
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                for result in data.get('results', [])[:6]:
                    img_url = result.get('urls', {}).get('regular', '')
                    if img_url:
                        if '?' in img_url:
                            img_url += '&w=800&q=90'
                        else:
                            img_url += '?w=800&q=90'
                        images.append(img_url)
        except Exception as e:
            pass
    
    return images[:count]


@api_router.post("/admin/organisms/ai-generate-images")
async def generate_organism_images_ai(request: dict):
    """Generate organism images using Unsplash API with AI-enhanced search."""
    try:
        organism_name = request.get("organism_name", "").strip()
        
        if not organism_name:
            raise ValueError("organism_name is required")
        
        image_urls = search_unsplash_images(organism_name, count=6)
        
        if not image_urls:
            image_urls = [
                "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=90",
                "https://images.unsplash.com/photo-1489330911046-c894fdcc538d?w=800&q=90"
            ]
        
        return {
            "success": True,
            "organism_name": organism_name,
            "image_urls": image_urls[:6],
            "source": "unsplash",
            "message": f"Generated {len(image_urls)} images for {organism_name}"
        }
    except Exception as e:
        print(f"[ERROR] AI image generation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate images"
        }

@api_router.post("/admin/login", response_model=AdminToken)
async def admin_login(login: AdminLogin):
    if login.username == "admin" and login.password == "adminSBES":
        token = hashlib.sha256("admin:adminSBES".encode()).hexdigest()
        return AdminToken(access_token=token)
    raise HTTPException(status_code=401, detail="Invalid credentials")

@api_router.post("/admin/verify-email")
async def verify_admin_email(request: dict):
    """Verify if an email is in the authorized admin whitelist."""
    try:
        email = request.get("email", "").strip().lower()
        
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        # Get authorized emails from environment
        authorized_emails_str = os.environ.get('AUTHORIZED_ADMIN_EMAILS', '')
        if not authorized_emails_str:
            raise HTTPException(status_code=503, detail="Admin email whitelist not configured")
        
        # Parse authorized emails (comma-separated)
        authorized_emails = [e.strip().lower() for e in authorized_emails_str.split(',')]
        
        # Check if email is authorized
        if email in authorized_emails:
            # Generate admin token for this email
            token = hashlib.sha256(f"admin:{email}".encode()).hexdigest()
            return {
                "success": True,
                "email": email,
                "access_token": token,
                "message": f"Successfully logged in as {email}"
            }
        else:
            raise HTTPException(status_code=403, detail="Email not authorized. Access denied.")
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Email verification error: {e}")
        raise HTTPException(status_code=500, detail="Email verification failed")

@api_router.post("/admin/google-login")
async def google_login(request: dict):
    """Verify Google OAuth token and check if email is authorized."""
    try:
        google_token = request.get("token", "").strip()
        
        if not google_token:
            raise HTTPException(status_code=400, detail="Google token is required")
        
        # Verify Google token using google-auth library
        try:
            from google.auth.transport import requests
            from google.oauth2 import id_token
            
            # Get Google Client ID from environment
            google_client_id = os.environ.get('GOOGLE_CLIENT_ID')
            if not google_client_id:
                raise HTTPException(status_code=503, detail="Google OAuth not configured")
            
            # Verify the token
            idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), google_client_id)
            
            # Extract email from token
            email = idinfo.get('email', '').strip().lower()
            if not email:
                raise HTTPException(status_code=400, detail="No email in Google token")
            
            # Verify email is authorized
            authorized_emails_str = os.environ.get('AUTHORIZED_ADMIN_EMAILS', '')
            if not authorized_emails_str:
                raise HTTPException(status_code=503, detail="Admin email whitelist not configured")
            
            authorized_emails = [e.strip().lower() for e in authorized_emails_str.split(',')]
            
            if email not in authorized_emails:
                raise HTTPException(status_code=403, detail=f"Email {email} is not authorized. Access denied.")
            
            # Generate admin token for this email
            token = hashlib.sha256(f"admin:{email}".encode()).hexdigest()
            
            return {
                "success": True,
                "email": email,
                "name": idinfo.get('name', ''),
                "picture": idinfo.get('picture', ''),
                "access_token": token,
                "message": f"Successfully logged in with Google as {email}"
            }
            
        except ValueError as e:
            logging.error(f"Invalid Google token: {e}")
            raise HTTPException(status_code=401, detail="Invalid Google token")
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Google login error: {e}")
        raise HTTPException(status_code=500, detail=f"Google login failed: {str(e)}")

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

# ==================== SUGGESTION ENDPOINTS ====================

# Get all suggestions (admin only)
@api_router.get("/admin/suggestions")
async def get_all_suggestions(_: bool = Depends(verify_admin_token)):
    try:
        suggestions = await suggestions_collection.find().to_list(1000)
        result = []
        for sugg in suggestions:
            # Remove MongoDB's _id field to avoid Pydantic validation error
            sugg_copy = {k: v for k, v in sugg.items() if k != '_id'}
            # Add default values for missing fields
            sugg_copy.setdefault('educational_level', 'Not specified')
            sugg_copy.setdefault('description', '')
            sugg_copy.setdefault('status', 'pending')
            result.append(Suggestion(**sugg_copy))
        return result
    except Exception as e:
        logging.error(f"Error fetching suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get pending suggestions (admin only)
@api_router.get("/admin/suggestions/pending")
async def get_pending_suggestions(_: bool = Depends(verify_admin_token)):
    try:
        suggestions = await suggestions_collection.find({"status": "pending"}).to_list(1000)
        result = []
        for sugg in suggestions:
            # Remove MongoDB's _id field to avoid Pydantic validation error
            sugg_copy = {k: v for k, v in sugg.items() if k != '_id'}
            # Add default values for missing fields
            sugg_copy.setdefault('educational_level', 'Not specified')
            sugg_copy.setdefault('description', '')
            sugg_copy.setdefault('status', 'pending')
            result.append(Suggestion(**sugg_copy))
        return result
    except Exception as e:
        logging.error(f"Error fetching pending suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Create new suggestion (public)
@api_router.post("/suggestions")
async def create_suggestion(suggestion: SuggestionCreate):
    try:
        if not suggestion.user_name.strip() or not suggestion.organism_name.strip():
            raise HTTPException(status_code=400, detail="User name and organism name are required")
        
        if not suggestion.educational_level or not suggestion.educational_level.strip():
            raise HTTPException(status_code=400, detail="Class/Standard is required")
        
        suggestion_data = Suggestion(
            user_name=suggestion.user_name,
            organism_name=suggestion.organism_name,
            description=suggestion.description or "",
            educational_level=suggestion.educational_level
        )
        
        await suggestions_collection.insert_one(suggestion_data.dict())
        return {"message": "Suggestion submitted successfully", "id": suggestion_data.id}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error creating suggestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Update suggestion status (admin only)
@api_router.put("/admin/suggestions/{suggestion_id}/status")
async def update_suggestion_status(suggestion_id: str, status: str, _: bool = Depends(verify_admin_token)):
    try:
        if status not in ["pending", "approved", "rejected"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        result = await suggestions_collection.update_one(
            {"id": suggestion_id},
            {"$set": {"status": status, "updated_at": datetime.utcnow().isoformat()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Suggestion not found")
        
        return {"message": f"Suggestion {status} successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating suggestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Verify suggestion with AI (admin only)
@api_router.post("/admin/suggestions/{suggestion_id}/verify")
async def verify_suggestion_ai(suggestion_id: str, _: bool = Depends(verify_admin_token)):
    try:
        suggestion = await suggestions_collection.find_one({"id": suggestion_id})
        if not suggestion:
            raise HTTPException(status_code=404, detail="Suggestion not found")
        
        if not HAS_GENAI or not GEMINI_API_KEY:
            raise HTTPException(status_code=503, detail="AI service not available")
        
        # Use Gemini to verify organism
        model = genai.GenerativeModel('gemini-2.5-flash')
        verification_prompt = f"""
        Is "{suggestion['organism_name']}" a real organism/animal/plant species that exists in nature?
        
        Respond with a JSON object:
        {{
            "is_authentic": true/false,
            "reason": "explanation",
            "type": "animal/plant/microorganism/fungus/other",
            "common_name": "if authentic",
            "scientific_name": "if authentic"
        }}
        """
        
        response = model.generate_content(verification_prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response
        import json
        try:
            # Try to find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                verification_data = json.loads(response_text[json_start:json_end])
            else:
                verification_data = {"is_authentic": False, "reason": "Could not parse response"}
        except json.JSONDecodeError:
            verification_data = {"is_authentic": False, "reason": "Invalid response format"}
        
        # Update suggestion with verification
        await suggestions_collection.update_one(
            {"id": suggestion_id},
            {
                "$set": {
                    "ai_verification": verification_data,
                    "updated_at": datetime.utcnow().isoformat()
                }
            }
        )
        
        return verification_data
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error verifying suggestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Approve suggestion and generate complete organism data (admin only)
@api_router.post("/admin/suggestions/{suggestion_id}/approve")
async def approve_suggestion_and_generate(suggestion_id: str, _: bool = Depends(verify_admin_token)):
    try:
        suggestion = await suggestions_collection.find_one({"id": suggestion_id})
        if not suggestion:
            raise HTTPException(status_code=404, detail="Suggestion not found")
        
        if not HAS_GENAI or not GEMINI_API_KEY:
            raise HTTPException(status_code=503, detail="AI service not available")
        
        organism_name = suggestion['organism_name']
        
        # Generate complete organism data using the AI endpoint
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
    "description": "General overview of the organism, its habitat, and interesting facts (3-4 sentences)"
}}

Be accurate and scientific. If you cannot find specific information, make reasonable educated guesses based on the organism's taxonomy.
Make sure the JSON is valid and properly formatted."""

        # Call Gemini API to generate organism data
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
        
        # Now generate images using the get_images_from_web function
        images = []
        try:
            search_terms = [
                organism_data.get('name', organism_name),
                organism_data.get('scientific_name', ''),
                organism_name
            ]
            
            for search_term in search_terms:
                if search_term:
                    images = await get_images_from_web_async(search_term, max_images=5)
                    if images:
                        break
        except Exception as e:
            logging.warning(f"Could not fetch images: {e}")
            images = []
        
        # Update suggestion status to approved
        await suggestions_collection.update_one(
            {"id": suggestion_id},
            {
                "$set": {
                    "status": "approved",
                    "updated_at": datetime.utcnow().isoformat(),
                    "ai_verification": {
                        "is_authentic": True,
                        "reason": "Admin approved and generated complete data"
                    }
                }
            }
        )
        
        # Return organism data with images ready for auto-fill
        return {
            "success": True,
            "organism_data": {
                "name": organism_data.get('name', organism_name),
                "scientific_name": organism_data.get('scientific_name', ''),
                "classification": organism_data.get('classification', {
                    "kingdom": "",
                    "phylum": "",
                    "class": "",
                    "order": "",
                    "family": "",
                    "genus": "",
                    "species": ""
                }),
                "morphology": organism_data.get('morphology', ''),
                "physiology": organism_data.get('physiology', ''),
                "description": organism_data.get('description', ''),
                "images": images
            },
            "suggestion_id": suggestion_id,
            "message": "Suggestion approved and organism data generated successfully"
        }
    except HTTPException:
        raise
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {str(e)}")
    except Exception as e:
        logging.error(f"Error approving suggestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Delete suggestion (admin only)
@api_router.delete("/admin/suggestions/{suggestion_id}")
async def delete_suggestion(suggestion_id: str, _: bool = Depends(verify_admin_token)):
    try:
        result = await suggestions_collection.delete_one({"id": suggestion_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Suggestion not found")
        return {"message": "Suggestion deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting suggestion: {e}")
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
