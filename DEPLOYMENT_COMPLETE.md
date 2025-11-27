# BioMuseum - Complete Deployment Instructions

## Prerequisites
- GitHub account (free at https://github.com)
- Vercel account (free, connect with GitHub)
- Render account (free at https://render.com)
- MongoDB Atlas account (already configured)

---

## STEP 1: Push Code to GitHub

### 1.1 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `BioMuseum`
3. Description: `Biology Museum - Organism Database with React and FastAPI`
4. Select "Public" (required for free tier)
5. Click "Create repository"

### 1.2 Push Your Code
```powershell
cd d:\BioMuseum
git remote add origin https://github.com/YOUR_USERNAME/BioMuseum.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

**Expected output:**
```
Enumerating objects: 98, done.
Counting objects: 100% (98/98), done.
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## STEP 2: Deploy Backend to Render

### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (easier)
3. Authorize GitHub access

### 2.2 Create New Web Service
1. Dashboard → "New +" button
2. Select "Web Service"
3. Connect repository: Select `BioMuseum` repo
4. Fill in details:
   - **Name**: `biomuseum-backend`
   - **Environment**: `Python 3`
   - **Region**: `Singapore (closest to Asia)` or pick your region
   - **Branch**: `main`
   - **Root Directory**: `.` (root)
   - **Build Command**: 
     ```
     pip install -r backend/requirements.txt
     ```
   - **Start Command**: 
     ```
     cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT
     ```

### 2.3 Add Environment Variables
In the "Environment" section, add:

| Key | Value |
|-----|-------|
| `MONGO_URL` | `mongodb+srv://sarthaknk:adminSBES@biomuseum.m30zoo4.mongodb.net/?appName=biomuseum` |
| `DB_NAME` | `biomuseum` |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:3001,https://biomuseum.vercel.app` |
| `FRONTEND_URL` | `https://biomuseum.vercel.app` |

### 2.4 Deploy
1. Click "Create Web Service"
2. Wait 3-5 minutes for deployment
3. You'll see "Your service is live" ✓
4. **Copy the URL** - looks like: `https://biomuseum-backend.onrender.com`

---

## STEP 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub (recommended)
3. Authorize GitHub access

### 3.2 Import Project
1. Dashboard → "Add New..." → "Project"
2. Select `BioMuseum` repository
3. **Important**: Set **Root Directory** to `frontend`
4. Click "Continue"

### 3.3 Configure Build Settings
Vercel auto-detects React, but verify:
- **Framework**: React
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

### 3.4 Add Environment Variables
Before deploying, add these:

| Key | Value |
|-----|-------|
| `REACT_APP_BACKEND_URL` | `https://biomuseum-backend.onrender.com` (from Step 2.4) |

### 3.5 Deploy
1. Click "Deploy"
2. Wait for build (1-2 minutes)
3. You'll see "Congratulations" ✓
4. **Copy the URL** - looks like: `https://biomuseum.vercel.app`

---

## STEP 4: Update Backend CORS

Now that you have the Vercel URL, update backend CORS:

### 4.1 Go to Render Dashboard
1. Select your `biomuseum-backend` service
2. Go to "Environment" tab
3. Update `CORS_ORIGINS`:
   ```
   http://localhost:3000,http://localhost:3001,https://YOUR-VERCEL-URL.vercel.app
   ```
4. Click "Save"

### 4.2 Redeploy Backend
1. Click "Manual Deploy" → "Deploy latest commit"
2. Wait for redeployment

---

## STEP 5: Test the Deployment

### 5.1 Test Backend API
```
curl https://biomuseum-backend.onrender.com/api/
```
Expected response:
```json
{"message": "Biology Museum API"}
```

### 5.2 Test Frontend
1. Open https://your-frontend-url.vercel.app
2. You should see the BioMuseum homepage
3. Test admin login: username `admin`, password `adminSBES`
4. Try adding a new organism

---

## STEP 6: Keep Backend Awake (Optional)

Render's free tier puts services to sleep after 15 minutes of inactivity.

### Solution: Use Uptime Monitor
1. Go to https://www.freshping.com (free)
2. Create account
3. Add monitor:
   - URL: `https://biomuseum-backend.onrender.com/api/`
   - Check every 14 minutes
4. This keeps your backend running 24/7

---

## Useful URLs After Deployment

| Service | URL |
|---------|-----|
| Frontend | https://biomuseum.vercel.app |
| Backend | https://biomuseum-backend.onrender.com |
| Backend API | https://biomuseum-backend.onrender.com/api/ |
| GitHub | https://github.com/YOUR_USERNAME/BioMuseum |
| Vercel Dashboard | https://vercel.com/dashboard |
| Render Dashboard | https://dashboard.render.com |
| MongoDB Atlas | https://cloud.mongodb.com |

---

## Troubleshooting

### Backend Deploy Failed
**Issue**: Build failed or deployment error
**Solution**:
1. Check Render logs (click service → Logs tab)
2. Verify `requirements.txt` has all dependencies
3. Check Python version compatibility
4. Ensure no syntax errors in `server.py`

### Frontend Won't Load
**Issue**: Blank page or 404
**Solution**:
1. Check Vercel build logs
2. Verify `REACT_APP_BACKEND_URL` is set correctly
3. Clear browser cache (Ctrl+Shift+Del)
4. Check browser console for errors (F12)

### API Errors (CORS, Connection)
**Issue**: Backend requests fail
**Solution**:
1. Verify `CORS_ORIGINS` includes your Vercel domain
2. Test: `curl https://biomuseum-backend.onrender.com/api/organisms`
3. Check MongoDB connection in Render logs
4. Verify MongoDB credentials are correct

### MongoDB Connection Error
**Issue**: `SSL handshake failed` or connection timeout
**Solution**:
1. Go to MongoDB Atlas → Network Access
2. Add IP: `0.0.0.0/0` (allow all)
3. Verify connection string in `.env`
4. Test locally first

### Data Not Persisting
**Issue**: Data added but not saved
**Solution**:
1. Check MongoDB is connected (see Render logs)
2. Verify `organisms` collection exists
3. Check write permissions in MongoDB
4. Look for database errors in backend logs

---

## Performance Tips

1. **Optimize Images**: Compress before upload
2. **Enable Caching**: Already configured in `vercel.json`
3. **Database Indexes**: Already set up in MongoDB
4. **API Rate Limiting**: Consider adding later

---

## Cost Breakdown

| Service | Cost | Limit |
|---------|------|-------|
| Vercel | FREE | 100 GB bandwidth/month |
| Render | FREE | 0.5 GB RAM, sleep after 15 min |
| MongoDB Atlas | FREE | 512 MB storage |
| **Total** | **$0/month** | **Unlimited users** |

---

## Next Steps

1. ✅ Test all features on production
2. ✅ Share your app URL
3. ✅ Monitor error logs regularly
4. ✅ Plan for scaling (upgrade services if needed)

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **MongoDB**: https://www.mongodb.com/docs

---

**Your BioMuseum is now live on the internet! 🚀**

