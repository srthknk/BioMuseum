# BioMuseum Deployment Guide

## Deployment Stack
- **Frontend**: Vercel (Free)
- **Backend**: Render (Free)
- **Database**: MongoDB Atlas (Free)

---

## Step 1: Push to GitHub

1. Create a new repository on GitHub at https://github.com/new
2. Name it `BioMuseum` (or your preferred name)
3. Run these commands:

```bash
cd d:\BioMuseum
git remote add origin https://github.com/YOUR_USERNAME/BioMuseum.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render

### Setup
1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in the settings:
   - **Name**: `biomuseum-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT`

### Environment Variables
Add these in Render dashboard under "Environment":
```
MONGO_URL=mongodb+srv://sarthaknk:adminSBES@biomuseum.m30zoo4.mongodb.net/?appName=biomuseum
DB_NAME=biomuseum
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-vercel-domain.vercel.app
FRONTEND_URL=https://your-vercel-domain.vercel.app
```

### Deploy
- Click "Create Web Service"
- Wait 3-5 minutes for deployment
- Get the backend URL from Render (e.g., `https://biomuseum-backend.onrender.com`)

---

## Step 3: Deploy Frontend to Vercel

### Setup
1. Go to https://vercel.com and sign up (free with GitHub)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Select `frontend` folder as root
5. Fill in settings:
   - **Framework**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### Environment Variables
Add in Vercel dashboard:
```
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
REACT_APP_OPENAI_API_KEY=your_key_here (if needed)
```

### Deploy
- Click "Deploy"
- Wait for build to complete
- Get your Vercel URL (e.g., `https://biomuseum.vercel.app`)

---

## Step 4: Update Backend CORS

After getting Vercel URL:
1. Go to Render dashboard
2. Edit backend service
3. Update `CORS_ORIGINS` environment variable with your Vercel URL
4. Redeploy backend

---

## Step 5: Update Frontend Environment

If needed, update `frontend/.env.local`:
```
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
REACT_APP_FRONTEND_URL=https://your-frontend.vercel.app
```

Then commit and push:
```bash
git add frontend/.env.local
git commit -m "Update deployment URLs"
git push
```

---

## Troubleshooting

### Backend Deploy Fails
- Check Render logs for Python errors
- Ensure `backend/requirements.txt` exists
- Verify Python version compatibility

### Frontend Deploy Fails
- Check Vercel build logs
- Ensure all imports are correct
- Verify `REACT_APP_BACKEND_URL` is set

### API Connection Issues
- Verify `CORS_ORIGINS` includes your Vercel domain
- Check MongoDB connection string
- Test: `curl https://your-backend.onrender.com/api/`

### MongoDB Connection Fails
- Verify IP whitelist in MongoDB Atlas (allow all for free tier)
- Check username/password credentials
- Ensure network connectivity

---

## Local Development

Run locally before deploying:

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn server:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

Visit: http://localhost:3000

---

## Database Backup

MongoDB Atlas free tier includes:
- 512 MB storage
- Automatic backups
- 3-node replica set

Data persists automatically across deployments.

---

## Free Tier Limits

| Service | Limit |
|---------|-------|
| Vercel | 100 GB bandwidth/month |
| Render | 0.5 GB memory, stops after 15 mins inactivity |
| MongoDB | 512 MB storage, 3 API requests/second |

To keep backend alive on Render, use a cron job service like https://www.freshping.com

---

## Support

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- MongoDB Docs: https://www.mongodb.com/docs/

