# BioMuseum Deployment Guide

Complete guide to deploy BioMuseum for FREE on popular platforms including Vercel, Heroku, Railway, and Render.

---

## Table of Contents
1. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
2. [Backend Deployment (Render)](#backend-deployment-render)
3. [Alternative: Heroku Deployment](#alternative-heroku-deployment)
4. [Alternative: Railway Deployment](#alternative-railway-deployment)
5. [Database Setup](#database-setup)
6. [Environment Variables](#environment-variables)
7. [Connecting Frontend & Backend](#connecting-frontend--backend)
8. [Troubleshooting](#troubleshooting)

---

## Frontend Deployment (Vercel)

### Prerequisites
- GitHub account (free)
- Vercel account (free)
- Your code pushed to GitHub

### Step 1: Push Code to GitHub

1. **Create GitHub Repository**
   - Go to https://github.com/new
   - Create a new repository named `BioMuseum`
   - Don't add README, gitignore, or license

2. **Initialize Git in Your Project**
   ```bash
   cd D:\BioMuseum
   git init
   git add .
   git commit -m "Initial BioMuseum commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/BioMuseum.git
   git push -u origin main
   ```

3. **Replace YOUR_USERNAME** with your actual GitHub username

### Step 2: Deploy Frontend to Vercel

1. **Go to Vercel**
   - Visit https://vercel.com
   - Click "Sign Up" → Choose "Continue with GitHub"
   - Authorize Vercel to access your GitHub

2. **Import Project**
   - Click "New Project"
   - Select your `BioMuseum` repository
   - Click "Import"

3. **Configure Project**
   - **Framework**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Environment Variables**
   - Click "Environment Variables"
   - Add:
     ```
     REACT_APP_BACKEND_URL=https://your-backend-url.com
     ```
   - Replace with your actual backend URL (we'll deploy backend next)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your site will be live at `https://your-project.vercel.app`

### Step 3: Update Vercel Backend URL

Once your backend is deployed (see next section), update the environment variable:

1. Go to Vercel Dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Edit `REACT_APP_BACKEND_URL` with your backend URL
5. Redeploy by pushing to GitHub or clicking "Redeploy"

---

## Backend Deployment (Render)

### Prerequisites
- Render account (free) https://render.com
- Python backend code
- GitHub repository

### Step 1: Create Render Account

1. Visit https://render.com
2. Click "Sign Up"
3. Choose "GitHub" for easy deployment
4. Authorize Render to access your GitHub

### Step 2: Create Web Service

1. **Go to Dashboard**
   - Click "New +" button
   - Select "Web Service"

2. **Connect Repository**
   - Select your `BioMuseum` repository
   - Click "Connect"

3. **Configure Service**
   - **Name**: `biomuseum-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`

4. **Set Environment Variables**
   - Scroll down to "Environment"
   - Add variables:
     ```
     FLASK_ENV=production
     FLASK_APP=server.py
     ```

5. **Choose Plan**
   - Select **Free** plan
   - Click "Create Web Service"

6. **Wait for Deployment**
   - Render will build and deploy automatically
   - Takes 2-5 minutes
   - You'll get a URL like `https://biomuseum-api.onrender.com`

### Step 3: Enable CORS in Backend

Your backend needs to allow requests from Vercel frontend:

**File**: `backend/server.py`

Find the CORS section and update:
```python
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-vercel-url.vercel.app", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

Replace `https://your-vercel-url.vercel.app` with your actual Vercel URL.

### Important: Keep Render Free Tier Awake

**Issue**: Free Render instances spin down after 15 minutes of inactivity

**Solution Options**:

**Option 1: Use Cron Job (Recommended)**
- Create a simple uptime monitor
- Tools: https://uptimerobot.com (free)
- Configure to ping your backend every 10 minutes

**Option 2: Upgrade to Paid**
- Render offers affordable paid plans ($7/month)

**Option 3: Use Alternative Services**
- Railway (more generous free tier)
- Fly.io (free tier available)

---

## Alternative: Heroku Deployment

⚠️ **Note**: Heroku free tier ended in November 2022. Use paid tier or alternatives.

---

## Alternative: Railway Deployment

### Backend Deployment on Railway

1. **Create Railway Account**
   - Visit https://railway.app
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose `BioMuseum` repository

3. **Configure**
   - Select `backend` directory
   - Railway auto-detects Python
   - Add environment variables (same as Render)

4. **View Deployment**
   - Railway provides a public URL automatically
   - Takes 2-5 minutes

### Frontend Deployment on Railway

1. **Add to Existing Project**
   - In Railway, click "Add Service"
   - Select "GitHub repo"
   - Choose same `BioMuseum` repo

2. **Configure Frontend**
   - Select `frontend` directory
   - Build command: `npm run build`
   - Start command: `npm start`

3. **Set Environment Variables**
   - Add `REACT_APP_BACKEND_URL`

4. **View Live Site**
   - Railway provides public URL
   - Same as backend URL prefix

---

## Database Setup

### Option 1: SQLite (Included - Local Storage)
- **Default**: BioMuseum uses SQLite
- **Data stored**: In `backend/database.db`
- **Limitation**: Data persists on local filesystem only
- **For production**: Upload database file or migrate to cloud database

### Option 2: PostgreSQL (Recommended for Production)

1. **Create Free PostgreSQL Database**
   - Visit https://www.elephantsql.com (free tier available)
   - Or use Render's integrated PostgreSQL

2. **Update Backend Connection**
   - **File**: `backend/server.py`
   - Find database URL configuration
   - Replace with:
     ```python
     import os
     DATABASE_URL = os.environ.get('DATABASE_URL')
     # Update SQLAlchemy configuration if using SQLAlchemy
     ```

3. **Add to Environment Variables**
   - In Render/Railway dashboard
   - Add: `DATABASE_URL=postgresql://user:password@host:5432/dbname`

### Option 3: MongoDB (Cloud-based)

1. **Create MongoDB Atlas Account**
   - Visit https://www.mongodb.com/cloud/atlas
   - Sign up (free tier: 512 MB)

2. **Create Cluster**
   - Create M0 cluster (free)
   - Add connection string to environment variables

---

## Environment Variables

### Frontend (.env file)

**File**: `frontend/.env` (create this file)

```
REACT_APP_BACKEND_URL=https://your-backend-url.com
```

### Backend (.env file)

**File**: `backend/.env` (create this file)

```
FLASK_ENV=production
FLASK_APP=server.py
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key-here
```

### How to Set in Render/Railway

1. **Go to Dashboard**
2. **Settings** or **Variables**
3. **Add** environment variables
4. **Deploy** or **Redeploy**

---

## Connecting Frontend & Backend

### Update Frontend URL After Backend Deployment

1. **Get Backend URL** from Render/Railway dashboard
2. **Update Vercel**:
   - Go to Vercel project
   - Settings → Environment Variables
   - Change `REACT_APP_BACKEND_URL` to your backend URL
   - Push to GitHub to redeploy

3. **Example**:
   ```
   Backend: https://biomuseum-api.onrender.com
   Frontend: https://biomuseum.vercel.app
   
   Update: REACT_APP_BACKEND_URL=https://biomuseum-api.onrender.com
   ```

### Test Connection

1. Open your Vercel frontend URL
2. Try to add an organism in admin panel
3. Check browser console (F12) for errors
4. If CORS errors appear, update CORS settings in backend

---

## Step-by-Step Deployment Summary

### Quick Deployment Checklist

- [ ] Push code to GitHub
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Render
- [ ] Get backend URL
- [ ] Update frontend environment variables
- [ ] Redeploy frontend
- [ ] Test admin login
- [ ] Test adding organism
- [ ] Check for errors in browser console

### Total Time: 15-30 minutes

---

## Free Tier Costs (Monthly)

| Service | Cost | Notes |
|---------|------|-------|
| Vercel Frontend | FREE | Up to 100 GB bandwidth |
| Render Backend | FREE | May spin down after 15 mins inactivity |
| Railway | FREE | $5 credit/month, generous free tier |
| PostgreSQL (ElephantSQL) | FREE | Limited storage |
| MongoDB Atlas | FREE | 512 MB storage |
| **Total** | **FREE** | All services combined |

---

## Advanced: Custom Domain (Optional)

### Add Custom Domain to Vercel

1. **Purchase Domain**
   - Namecheap ($0.88/year first year)
   - GoDaddy
   - Google Domains

2. **Connect to Vercel**
   - Vercel Dashboard → Settings → Domains
   - Add your domain
   - Update DNS records (Vercel provides instructions)
   - Takes 24-48 hours to propagate

### Example
- Instead of `biomuseum.vercel.app`
- Use `mymuseum.com`

---

## Monitoring & Maintenance

### Monitor Your Deployment

1. **Vercel Analytics**
   - Vercel Dashboard → Analytics
   - View traffic and performance

2. **Render Logs**
   - Render Dashboard → Logs
   - See backend errors and activity

3. **Keep Render Awake**
   - Use UptimeRobot (free)
   - Ping backend every 10 minutes
   - Prevents spin-down

### Update Your App

1. **Make Changes Locally**
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

2. **Auto-Deploy**
   - Vercel & Render auto-deploy on GitHub push
   - Takes 1-3 minutes

---

## Troubleshooting Deployment

### Frontend Not Loading

**Problem**: Blank page or 404 error

**Solutions**:
1. Check Vercel build logs: Dashboard → Deployments → Logs
2. Verify Root Directory is `frontend`
3. Clear browser cache (Ctrl+Shift+Delete)

### Backend Connection Error

**Problem**: "Cannot connect to backend" or CORS error

**Solutions**:
1. Check `REACT_APP_BACKEND_URL` is correct
2. Verify backend is running (check Render logs)
3. Update CORS settings in `backend/server.py`
4. Redeploy frontend

### Render Backend Spinning Down

**Problem**: 502 Bad Gateway or timeout errors

**Solutions**:
1. Set up UptimeRobot to keep it awake
2. Upgrade to paid plan
3. Use Railway instead (more generous)

### Environment Variables Not Working

**Problem**: Getting undefined errors

**Solutions**:
1. Verify variable names are correct
2. Redeploy after adding variables
3. Check file: `.env` should NOT be in Git
4. Use platform-specific env setup (Render/Railway/Vercel dashboard)

### Database Connection Errors

**Problem**: "Cannot connect to database"

**Solutions**:
1. Verify `DATABASE_URL` is correct
2. Check IP whitelist (if using PostgreSQL)
3. Ensure database is running
4. Check credentials in connection string

---

## Migration: Moving Between Platforms

### From Render to Railway
1. Export database
2. Create new Railway service
3. Import database
4. Update frontend URL

### Backup Your Data
```bash
# Download SQLite database
git pull origin main
# Or export from PostgreSQL
pg_dump -h host -U user -d database > backup.sql
```

---

## Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **UptimeRobot**: https://uptimerobot.com (keep backend awake)
- **ElephantSQL**: https://www.elephantsql.com (PostgreSQL)
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas

---

## Production Checklist

Before going live:

- [ ] Change admin password
- [ ] Enable HTTPS (automatic on Vercel/Render)
- [ ] Set up monitoring (UptimeRobot)
- [ ] Test all features
- [ ] Check error logs
- [ ] Set up backups
- [ ] Add custom domain (optional)
- [ ] Monitor costs (free tier)

---

**Last Updated**: November 26, 2025
**Version**: 1.0
