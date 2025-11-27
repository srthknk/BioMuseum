# Copy-Paste Deployment Commands

## Prerequisites
- GitHub account
- Vercel account (connect with GitHub)
- Render account
- MongoDB Atlas (already set up)

---

## STEP 1: Create GitHub Repository

Go to: https://github.com/new

Fill in:
- Repository name: `BioMuseum`
- Description: `Biology Museum Database with React and FastAPI`
- Visibility: **Public**
- Click "Create repository"

Then you'll see a page with setup instructions. **Follow the section "…or push an existing repository from the command line"**

---

## STEP 2: Push Code to GitHub

**Copy and paste these commands exactly:**

```powershell
cd d:\BioMuseum
git remote add origin https://github.com/YOUR_USERNAME/BioMuseum.git
git branch -M main
git push -u origin main
```

⚠️ Replace `YOUR_USERNAME` with your actual GitHub username!

**After running these commands, verify on GitHub that your files are there.**

---

## STEP 3: Deploy Backend to Render

### 3.1 Go to Render Dashboard
https://dashboard.render.com

### 3.2 Create Web Service
- Click "New +" → "Web Service"
- Select GitHub auth
- Choose your `BioMuseum` repository
- Settings:
  ```
  Name: biomuseum-backend
  Environment: Python 3
  Region: Singapore (or closest to you)
  Branch: main
  Build Command: pip install -r backend/requirements.txt
  Start Command: cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT
  ```

### 3.3 Add Environment Variables
Before clicking Deploy, scroll down to "Environment" and add:

```
MONGO_URL = mongodb+srv://sarthaknk:adminSBES@biomuseum.m30zoo4.mongodb.net/?appName=biomuseum
DB_NAME = biomuseum
CORS_ORIGINS = http://localhost:3000,http://localhost:3001,https://biomuseum.vercel.app
FRONTEND_URL = https://biomuseum.vercel.app
```

### 3.4 Deploy
- Click "Create Web Service"
- Wait 3-5 minutes
- **Copy the URL** when it says "Your service is live"
- Example: `https://biomuseum-backend.onrender.com`

---

## STEP 4: Deploy Frontend to Vercel

### 4.1 Go to Vercel
https://vercel.com/dashboard

### 4.2 Import Project
- Click "Add New" → "Project"
- Select your `BioMuseum` repository
- **Root Directory: `frontend`** ⚠️ IMPORTANT!
- Click "Continue"

### 4.3 Environment Variables
Add this environment variable:

```
REACT_APP_BACKEND_URL = https://biomuseum-backend.onrender.com
```

(Replace with the actual URL from Step 3.4)

### 4.4 Deploy
- Click "Deploy"
- Wait 1-2 minutes
- **Copy the URL** when deployment completes
- Example: `https://biomuseum.vercel.app`

---

## STEP 5: Update Backend CORS

Now that you have Vercel URL, update backend CORS:

### 5.1 Go to Render Dashboard
https://dashboard.render.com

### 5.2 Edit Environment Variables
- Click your `biomuseum-backend` service
- Go to "Environment"
- Update `CORS_ORIGINS` to include your Vercel URL:
  ```
  CORS_ORIGINS = http://localhost:3000,http://localhost:3001,https://YOUR-VERCEL-URL.vercel.app
  ```

### 5.3 Redeploy
- Click "Manual Deploy"
- Select "Deploy latest commit"
- Wait for redeployment

---

## STEP 6: Test Everything

### Test Backend
Open in browser or terminal:
```
https://biomuseum-backend.onrender.com/api/
```
Should return:
```json
{"message":"Biology Museum API"}
```

### Test Frontend
Open in browser:
```
https://your-frontend-url.vercel.app
```

Try:
1. View organisms on home page
2. Click "Admin Login" - use `admin` / `adminSBES`
3. Add a new organism
4. Search for it
5. View organism details

---

## All Set! 🎉

Your app is now live on the internet!

### Share These URLs
- **App URL**: https://your-frontend.vercel.app
- **API URL**: https://biomuseum-backend.onrender.com

### Keep Backend Awake (Optional)
Render sleeps backend after 15 minutes. To keep it alive:

Go to: https://www.freshping.com
- Create free account
- Add monitor for: `https://biomuseum-backend.onrender.com/api/`
- Check every 14 minutes
- Backend stays alive 24/7

---

## Troubleshooting

### Push to GitHub Failed
```
Run: git log
Should see your commits
If error: Make sure you're in d:\BioMuseum folder
```

### Render Deploy Failed
1. Click service → "Logs"
2. Look for error messages
3. Check `requirements.txt` exists in backend/
4. Verify Python syntax in `server.py`

### Vercel Deploy Failed
1. Click "Deployments"
2. View build logs
3. Check imports in App.js
4. Verify `frontend/` folder exists

### API Connection Errors
1. Verify `CORS_ORIGINS` in Render includes Vercel URL
2. Test: `curl https://biomuseum-backend.onrender.com/api/organisms`
3. Check MongoDB connection in Render logs

---

## Important Reminders

✅ GitHub username (YOUR_USERNAME)
✅ Render backend URL (copy after deployment)
✅ Vercel frontend URL (copy after deployment)
✅ Update CORS after getting Vercel URL
✅ Test all features on production
✅ Keep credentials safe

---

**Questions? Check DEPLOYMENT_COMPLETE.md for detailed explanations.**

