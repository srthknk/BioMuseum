# BioMuseum - Setup & Deployment Guide

## Project Overview
BioMuseum is a full-stack biology museum application for managing and displaying organisms with QR code scanning capabilities.

### Tech Stack
- **Backend**: FastAPI (Python) with MongoDB
- **Frontend**: React with Tailwind CSS
- **Database**: MongoDB (Local or Atlas Cloud)

---

## Local Setup Instructions

### Prerequisites
- Python 3.8+ (installed)
- Node.js 16+ (for frontend)
- MongoDB (local installation or MongoDB Atlas account)

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Install Python dependencies**
The virtual environment is already set up. Dependencies installed:
- fastapi
- uvicorn
- motor (async MongoDB driver)
- python-dotenv
- qrcode
- pillow
- pymongo

3. **Configure MongoDB**

**Option A: Local MongoDB Installation**
- Download MongoDB Community Edition from https://www.mongodb.com/try/download/community
- Install and start MongoDB service
- Update `.env`: `MONGO_URL=mongodb://localhost:27017`

**Option B: MongoDB Atlas Cloud (Recommended for simplicity)**
- Create free account at https://www.mongodb.com/cloud/atlas
- Create a cluster and database
- Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`
- Update `.env` with your connection string
- In Atlas: Whitelist your IP address (or allow all IPs: 0.0.0.0/0 for development)

4. **Seed initial data**
```bash
D:/BioMuseum/.venv/Scripts/python.exe seed_data.py
```

5. **Start the backend server**
```bash
D:/BioMuseum/.venv/Scripts/python.exe -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

3. **Start the development server**
```bash
npm start
# or
yarn start
```

The frontend will open at: `http://localhost:3000`

---

## API Endpoints

### Public Endpoints
- `GET /api/` - API info
- `GET /api/organisms` - List all organisms
- `GET /api/organisms/{id}` - Get organism by ID
- `GET /api/organisms/qr/{qr_id}` - Get organism by QR code
- `GET /api/search?q=query` - Search organisms

### Admin Endpoints
- `POST /api/admin/login` - Admin login (credentials: admin/adminSBES)
- `POST /api/admin/organisms` - Create organism
- `PUT /api/admin/organisms/{id}` - Update organism
- `DELETE /api/admin/organisms/{id}` - Delete organism

---

## Database Schema

### Collections

**organisms**
```javascript
{
  id: UUID,
  name: String,
  scientific_name: String,
  classification: {
    kingdom: String,
    phylum: String,
    class: String,
    order: String,
    family: String,
    genus: String,
    species: String
  },
  morphology: String,
  physiology: String,
  description: String,
  images: [String], // Base64 encoded
  qr_code_id: UUID,
  qr_code_image: String, // Base64 PNG
  created_at: DateTime,
  updated_at: DateTime
}
```

---

## Deployment Guide

### Backend Deployment (Heroku, Railway, Render)

1. **Install production dependencies**
```bash
pip install -r backend/requirements.txt
```

2. **Create Procfile** in root directory:
```
web: cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT
```

3. **Environment Variables on Platform**
Set the following on your deployment platform:
```
MONGO_URL=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=biomuseum
FRONTEND_URL=https://your-frontend-domain.com
CORS_ORIGINS=https://your-frontend-domain.com
```

4. **Deploy**
```bash
# Using Heroku CLI
heroku create your-app-name
git push heroku main
```

### Frontend Deployment (Vercel, Netlify)

1. **Build the production bundle**
```bash
cd frontend
npm run build
```

2. **Environment Variables**
Set `REACT_APP_BACKEND_URL` to your deployed backend URL

3. **Deploy**
```bash
# Using Vercel CLI
npm i -g vercel
vercel
```

Or push to GitHub and connect to Vercel/Netlify for auto-deployment

---

## Testing

### Backend API Tests
```bash
# Run test suite
python backend_test.py

# Run edge case tests
python edge_case_tests.py
```

### Frontend Testing
```bash
cd frontend
npm test
```

---

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running (local) or Atlas credentials are correct
- Check `.env` file has correct `MONGO_URL`
- Verify IP whitelist in MongoDB Atlas if using cloud

### CORS Errors
- Check `CORS_ORIGINS` in `.env` matches your frontend URL
- Ensure backend server is restarted after changing .env

### Port Already in Use
- Backend: Change port in startup command: `--port 8001`
- Frontend: Change port: `PORT=3001 npm start`

### Import Errors in Backend
- Reinstall packages: `pip install --upgrade -r backend/requirements.txt`
- Verify Python version: `python --version` (should be 3.8+)

---

## Important Notes

- Admin credentials hardcoded: `admin:adminSBES` - Change in production!
- QR codes generated with organism ID
- Images stored as base64 in database (consider cloud storage for production)
- All timestamps in UTC

---

## Project Cleanup Done

✅ Removed `.emergent/` folder (Emergent AI specific)
✅ Removed `.gitconfig`
✅ Updated to local MongoDB setup
✅ Cleaned requirements.txt (removed unnecessary dev dependencies)
✅ Created `.env` files with proper configuration

---

## Next Steps

1. Install MongoDB locally OR create MongoDB Atlas account
2. Run backend server with `uvicorn server:app --reload`
3. Seed initial data with `python seed_data.py`
4. Run frontend with `npm start`
5. Access application at `http://localhost:3000`

