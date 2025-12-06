# Unsplash API Key Setup - Quick Walkthrough

## 🔑 Getting Your Unsplash API Key (5 minutes)

### Step 1: Create Unsplash Account (if you don't have one)
- Go to: https://unsplash.com
- Click "Sign In" → "Create account"
- Verify email

### Step 2: Access Developer Console
- Go to: https://unsplash.com/developers
- Click "Your Apps" (top right after signing in)

### Step 3: Create Application
- Click "New Application" button
- Accept Terms and Conditions
- Fill in:
  - **Application Name:** BioMuseum (or any name)
  - **Description:** Image generation for biology museum app
  - **Website:** http://localhost:3000 (or your domain)
  - **Intended use:** I want to use this for an application

### Step 4: Get Access Key
- After creating, you'll see your application
- Under "Keys" section, find "Access Key"
- **Copy the Access Key** (looks like: `abc123def456ghi789jkl...`)

### Step 5: Update Backend Config
Edit file: `c:\BioMuseum\backend\.env`

Find this line:
```
UNSPLASH_ACCESS_KEY=your_unsplash_api_key_here
```

Replace with your actual key:
```
UNSPLASH_ACCESS_KEY=abc123def456ghi789jkl...
```

**Example (FAKE KEY - don't use this):**
```
UNSPLASH_ACCESS_KEY=rK1234567890abcdefghijklmnopqrstuvwxyz
```

### Step 6: Restart Backend
```powershell
# Kill old backend
taskkill /F /IM python.exe

# Start new backend
cd c:\BioMuseum\backend
c:\BioMuseum\.venv\Scripts\python.exe -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Wait 10-15 seconds for it to start.

### Step 7: Test It Works
1. Go to http://localhost:3000
2. Click Admin button → Login
3. Go to "Add Organism" tab
4. Type "Dog" in the name field
5. Click "AI Images" button
6. **You should see 5 dog images load!** ✅

---

## 🚨 If Images Still Don't Load

**Check these in order:**

1. **Is the key in .env?**
   ```powershell
   Get-Content c:\BioMuseum\backend\.env | Select-String "UNSPLASH"
   ```
   Should show: `UNSPLASH_ACCESS_KEY=rK...`

2. **Did you restart backend?**
   - Check the terminal - should show:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.
   ```

3. **Check backend logs for errors:**
   - Look for: `WARNING: Unsplash API error`
   - Or: `INFO: Generated 5 images from Unsplash`

4. **Test the API directly:**
   - Go to: http://localhost:8000/docs
   - Find: `POST /admin/organisms/ai-generate-images`
   - Click "Try it out"
   - Enter: `{"organism_name": "Lion"}`
   - Click "Execute"
   - Should return image URLs

---

## 📊 Rate Limits

- **Free tier:** 50 requests per hour per API key
- **Testing:** This is plenty for development

If you see `429 error`, just wait an hour for the limit to reset.

---

## ✅ Success Indicators

**Backend logs should show:**
```
INFO: Generated 5 images from Unsplash for term 'Lion'
```

**Frontend should display:**
- 5 real animal photos
- From Unsplash (you can click to see source)

---

That's it! You're all set. Let me know if you run into any issues! 🎉
