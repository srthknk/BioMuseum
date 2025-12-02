# 🔍 Troubleshooting Guide - Biotube Suggestions Not Showing

## Problem
Suggestions are not appearing in the Admin Panel → Biotube → Suggestions tab after submitting them.

---

## Step-by-Step Diagnosis

### 1. Check if Suggestions are Being Submitted ✅

**What to do:**
- Go to `http://localhost:3000/biotube` (Biotube home page)
- Click **💡 Suggest Video** button
- Fill in the form:
  - Name: `Test User`
  - Class: `12th`
  - Video Title: `Lion Hunting`
  - Description: `Test description`
- Click **Submit**
- Look for **✅ success message** (green notification)

**Expected Result:**
- Form clears after submission
- Success message appears: "Thank you! Your suggestion has been submitted successfully."

**If you don't see success message:**
- Check browser console (F12) for errors
- Check that backend is running
- Make sure MongoDB is accessible

---

### 2. Check Backend is Running ✅

**What to do:**
- Open a terminal
- Run: `cd d:\BioMuseum\backend`
- Run: `python server.py`
- Look for message: `[INFO] Server running at http://0.0.0.0:8000`

**Expected:**
```
INFO:     Application startup complete
Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**If you see an error:**
- Check that port 8000 is not in use
- Check that all dependencies are installed
- Check backend logs for detailed errors

---

### 3. Verify MongoDB Connection ✅

**What to do:**
- Check that MongoDB is running
- Open a terminal
- Run: `py manage_mongodb.py` (if available) or use MongoDB Compass
- Navigate to database: `BioMuseumDB` → `video_suggestions`

**Expected:**
- Collection `video_suggestions` should exist
- Should see documents after submitting suggestions
- Each document should have fields:
  - `_id` (MongoDB ID)
  - `id` (UUID)
  - `user_name`
  - `user_class`
  - `video_title`
  - `video_description`
  - `status` (should be "pending")
  - `created_at`
  - `updated_at`

**If collection is empty:**
- Try submitting a suggestion again
- Check that submission succeeded

---

### 4. Check API Response in Browser ✅

**What to do:**
1. Open browser Developer Tools (F12)
2. Go to Admin Panel (http://localhost:3000/admin)
3. Login if needed
4. Click **🎬 Biotube** tab
5. Click **💡 Suggestions** tab
6. Open DevTools **Network** tab
7. Look for request to `/api/admin/biotube/suggestions`

**Expected Request:**
```
URL: http://localhost:8000/api/admin/biotube/suggestions
Method: GET
Status: 200 OK
Headers: Authorization: Bearer <your_token>
```

**Expected Response:**
```json
[
  {
    "id": "uuid-here",
    "user_name": "Test User",
    "user_class": "12th",
    "video_title": "Lion Hunting",
    "video_description": "Test description",
    "status": "pending",
    "created_at": "2025-12-02T...",
    "updated_at": "2025-12-02T..."
  }
]
```

**If status is not 200:**
- **401**: Authentication failed - Login again
- **403**: Permission denied - Make sure you're admin user
- **500**: Server error - Check backend logs
- **404**: Endpoint not found - Backend might not be running

---

### 5. Check Browser Console for Errors ✅

**What to do:**
1. Press F12 to open DevTools
2. Click **Console** tab
3. Look for any red error messages
4. Look for warning messages starting with "Error fetching data"

**Common Errors:**

**Error 1: Network Error**
```
Error: Network Error
Error details: Error: connect ECONNREFUSED 127.0.0.1:8000
```
**Fix:** Backend is not running. Start it with `python backend/server.py`

**Error 2: 401 Unauthorized**
```
Error fetching data: AxiosError: {status: 401}
Error details: {detail: "Not authenticated"}
```
**Fix:** Login again. Token might have expired.

**Error 3: 403 Forbidden**
```
Error fetching data: AxiosError: {status: 403}
Error details: {detail: "Not authorized"}
```
**Fix:** Make sure your account is admin. Check user role in database.

**Error 4: Data is undefined**
```
Uncaught TypeError: Cannot read property 'map' of undefined
```
**Fix:** API returned null/undefined. Check backend response.

---

### 6. Full Request-Response Flow ✅

**What happens when you submit a suggestion:**

1. **User fills form** on `/biotube` page
   ```
   Name: "Test User"
   Class: "12th"
   Video: "Test Video"
   ```

2. **Frontend sends POST request**
   ```
   POST /api/biotube/suggest-video
   {
     "user_name": "Test User",
     "user_class": "12th",
     "video_title": "Test Video",
     "video_description": ""
   }
   ```

3. **Backend creates document**
   - Generates UUID for `id`
   - Sets `status` to "pending"
   - Saves to MongoDB

4. **MongoDB stores document**
   ```
   db.video_suggestions.insertOne({
     _id: ObjectId(...),
     id: "uuid-string",
     user_name: "Test User",
     user_class: "12th",
     video_title: "Test Video",
     status: "pending",
     created_at: "2025-12-02T...",
     updated_at: "2025-12-02T..."
   })
   ```

5. **Backend returns success**
   ```
   {
     "message": "Video suggestion submitted successfully",
     "id": "uuid-string"
   }
   ```

6. **Frontend shows success message**
   - Green notification appears
   - Form resets
   - User sees "Thank you!" message

7. **Admin views suggestions**
   - Go to Admin → Biotube → Suggestions
   - Frontend fetches with GET request
   - Shows all pending suggestions in list

---

## Quick Checks

Run this checklist to find the issue:

- [ ] **MongoDB running?**
  - Windows: Check MongoDB is in system services or running
  - Verify connection string: `mongodb://localhost:27017`
  
- [ ] **Backend running?**
  - Check terminal shows `Uvicorn running`
  - Visit http://localhost:8000/health
  
- [ ] **Frontend running?**
  - Check http://localhost:3000 loads
  - Page doesn't show "connection refused"
  
- [ ] **Suggestions submitted?**
  - Go to `/biotube` page
  - Click "Suggest Video" button
  - Fill form and click Submit
  - See green success message
  
- [ ] **Admin logged in?**
  - Go to `/admin` page
  - Make sure you can see admin content
  - Check token in local storage
  
- [ ] **Biotube tab visible?**
  - In admin panel, do you see "🎬 Biotube" tab?
  - Can you click it?
  
- [ ] **Suggestions tab visible?**
  - In Biotube admin, click "💡 Suggestions" tab
  - Does it load?
  - Shows "No suggestions yet" or list?

---

## Solutions by Error Type

### "No suggestions yet" message
**Means:** No documents in `video_suggestions` collection OR fetch failed silently

**Check:**
1. Did you submit a suggestion? (Go to /biotube, try again)
2. Is MongoDB running? (Check connection)
3. Check browser console for errors
4. Check backend server logs

### "Connection refused" error
**Means:** Backend not running

**Fix:**
```bash
cd d:\BioMuseum
python backend/server.py
```

### "Not authenticated" error (401)
**Means:** Auth token invalid or missing

**Fix:**
1. Logout and login again
2. Clear browser cookies
3. Check Local Storage in DevTools

### "Not authorized" error (403)
**Means:** User is not admin

**Fix:**
1. Check that your user account is admin
2. Query database to verify:
   ```
   db.users.findOne({email: "your@email.com"})
   ```
3. Make sure `is_admin: true` or `role: "admin"`

---

## Advanced Debugging

### Check Database Directly

Using MongoDB Compass or mongosh:

```javascript
// Count suggestions
db.video_suggestions.countDocuments({})

// View all suggestions
db.video_suggestions.find({}).pretty()

// View pending only
db.video_suggestions.find({status: "pending"}).pretty()

// View specific user
db.video_suggestions.find({user_name: "Test User"}).pretty()

// Check if collection exists
db.getCollectionNames()
```

### Check Backend Logs

Look at terminal where `python server.py` is running:

- Should show incoming POST requests from frontend
- Should log database operations
- Should log any errors

Example log:
```
INFO:     GET http://localhost:3000 - "POST /api/biotube/suggest-video HTTP/1.1" 200 OK
INFO:     Database: Inserted suggestion with ID: uuid-123-456
INFO:     Admin: GET /api/admin/biotube/suggestions - User: admin_user
```

### Check Network Requests

In DevTools Network tab:
1. Filter by "fetch/XHR"
2. Look for request to `/api/admin/biotube/suggestions`
3. Check:
   - **Request Headers**
     - `Authorization: Bearer <token>` should be present
     - `Content-Type: application/json`
   
   - **Response Headers**
     - `Content-Type: application/json`
   
   - **Response Body**
     - Should be an array `[...]`
     - Should contain objects with suggestion data

---

## Still Not Working?

1. **Clear cache and reload**
   - Hard refresh: Ctrl+Shift+R
   - Clear cookies
   - Close and reopen browser

2. **Check for typos**
   - API endpoint: `/admin/biotube/suggestions` (not `suggestion`)
   - Collection name: `video_suggestions`
   - Database name: `BioMuseumDB`

3. **Restart services**
   ```bash
   # Stop MongoDB (if running locally)
   # Stop backend: Press Ctrl+C in server.py terminal
   # Stop frontend: Press Ctrl+C in npm terminal
   
   # Start in correct order:
   1. MongoDB
   2. Backend: python backend/server.py
   3. Frontend: npm start
   ```

4. **Check file modifications**
   - Make sure `BiotubeAdminPanel.jsx` has suggestions rendering code
   - Make sure `server.py` has `/admin/biotube/suggestions` endpoint
   - Run `git status` to see what changed

5. **Contact support**
   - Share the full error message from browser console
   - Share server logs
   - Share network request/response
   - Share database query results

---

## Expected Working Flow

```
User Flow:
1. Visit http://localhost:3000/biotube
2. Click "💡 Suggest Video"
3. Fill form: Name, Class, Title, Description
4. Click "Submit"
5. See "✅ Thank you!" message
6. Close modal

Admin Flow:
1. Visit http://localhost:3000/admin
2. Click "🎬 Biotube" tab
3. Click "💡 Suggestions" tab
4. See list of suggestions
5. Each suggestion shows:
   - Title
   - User name and class
   - Yellow "pending" badge
   - Action buttons (Reviewed, Added, Dismissed)
```

---

## Summary

The suggestion system should work as:
1. ✅ Users can submit suggestions from Biotube home
2. ✅ Suggestions save to MongoDB
3. ✅ Admin can view suggestions in admin panel
4. ✅ Admin can update suggestion status
5. ✅ Suggestions appear in user history

If any step fails, follow the troubleshooting guide above for your specific error.
