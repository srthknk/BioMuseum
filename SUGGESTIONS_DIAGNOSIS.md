# 🔍 Biotube Suggestions - Diagnosis Checklist

## Problem Summary
✅ Dashboard SHOWS pending suggestions count  
❌ Suggestions tab shows EMPTY (no suggestions to display)

This means:
- ✅ Database connection is working (dashboard queries it successfully)
- ✅ Data is in the database (dashboard found the count)
- ❌ Something is wrong with GET suggestions endpoint or frontend

---

## Quick Diagnosis

### Step 1: Check Browser Console (F12)
```
Expected to see:
✅ Suggestions API Response: Array(...)
Number of suggestions: [count]

If instead you see:
❌ Error fetching suggestions: AxiosError
Error status: 500
```

---

### Step 2: Check Backend Logs

Look at the terminal where `python backend/server.py` is running.

**When you click Suggestions tab, you should see:**
```
[Biotube] Found X suggestions in database
[Biotube] Returning Y processed suggestions
```

**If you see errors like:**
```
[Biotube] Error fetching video suggestions: ...
[Biotube] Traceback: ...
```

Then the backend is failing to return the data. **Screenshot this error!**

---

### Step 3: Check Network Tab (F12)

1. Go to Admin → Biotube → Suggestions
2. Open DevTools → Network tab
3. Look for request to `/api/admin/biotube/suggestions`
4. Check Status Code:
   - **200**: Success (but frontend not showing data)
   - **401**: Auth failed
   - **403**: Permission denied
   - **500**: Server error
   - **Other**: Connection issue

5. Click on the request and check **Response** tab
   - Should see JSON array `[]` or `[{...}, {...}]`
   - Should NOT see HTML error page

---

## Possible Issues & Solutions

### Issue 1: Dashboard Shows Count But Tab Shows Empty

**Cause**: API returns 200 but with empty array

**Check**:
1. Network tab → Response should show `[]` (empty) or `[{...}]` (has data)
2. If response is `[]` → No suggestions in database
3. If response has data but not showing → Frontend bug

**Solution**:
- Submit a new suggestion from `/biotube` page
- Or check MongoDB directly:
  ```
  mongosh
  use biomuseum
  db.video_suggestions.find()
  ```

---

### Issue 2: API Returns Error (500)

**Cause**: Backend is throwing an exception

**Check**:
1. Backend logs for error message
2. Network tab → Response should show error details

**Solution**:
- Look for error in backend logs
- Common errors:
  - Missing fields in document
  - Database connection lost
  - Type validation error

---

### Issue 3: API Returns 401/403

**Cause**: Authentication or authorization failed

**Check**:
1. Are you logged in? (Check navbar)
2. Is your account admin? (Check in database)

**Solution**:
- Logout and login again
- Check user role in database

---

### Issue 4: Network Request Fails

**Cause**: Backend not responding or connection error

**Check**:
1. Is backend running? (Check for `Uvicorn running` message)
2. Is URL correct? Should be `http://localhost:8000/api/admin/biotube/suggestions`

**Solution**:
- Start backend: `python backend/server.py`
- Hard refresh browser: Ctrl+Shift+R

---

## Step-by-Step Diagnosis Flow

```
1. Dashboard shows count?
   ├─ YES → Database has data, server is responding
   └─ NO → Database is empty
   
2. Click Suggestions tab
   ├─ See error in console?
   │  ├─ YES → Check backend logs for detailed error
   │  └─ NO → Network request succeeded
   │
   └─ Network request status?
      ├─ 200 → Response is successful
      │  ├─ Response has data → Frontend issue
      │  └─ Response is empty → Database has no suggestions
      │
      ├─ 401 → Login again
      ├─ 403 → Check user role
      └─ 500 → Backend error, check logs
```

---

## Testing Commands

### Test 1: Check Database Directly
```bash
mongosh
use biomuseum
db.video_suggestions.find().pretty()
```

Expected: See documents with `user_name`, `video_title`, etc.

### Test 2: Check Backend Response
```bash
# Make sure you have a valid token first
TOKEN="your_token_here"
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/admin/biotube/suggestions
```

Expected: JSON array of suggestions

### Test 3: Run Diagnostic
```bash
python diagnose_biotube_db.py
```

This will show:
- Database connection status
- Collection existence
- Document count
- Sample data

### Test 4: Run API Test
```bash
python test_biotube_api.py
```

This will test all endpoints and show detailed status

---

## Key Indicators

| Indicator | Status | Meaning |
|-----------|--------|---------|
| Dashboard shows "Pending Suggestions: 5" | ✅ | Database is working, has data |
| Suggestions tab shows "No suggestions yet" | ⚠️ | Either empty DB or fetch failed |
| Browser console shows error | ❌ | Frontend or API issue |
| Backend logs show error | ❌ | Backend is failing |
| Network shows 500 status | ❌ | Server error |
| Network shows 200 with empty array | ⚠️ | No data in database |

---

## What NOT to Do

❌ Don't just hard refresh (data might still not exist)
❌ Don't restart everything at once (can't see error messages)
❌ Don't assume it's the frontend (backend might be failing silently)
❌ Don't submit suggestions multiple times (clogs the database)

---

## What TO Do

✅ Check console errors first (F12)
✅ Check backend logs for error details
✅ Verify database has documents (mongosh)
✅ Use Network tab to inspect API response
✅ Check that you're logged in as admin
✅ Hard refresh if you change backend code

---

## Expected Working Flow

```
1. User submits suggestion from /biotube
   ↓
2. POST /api/biotube/suggest-video succeeds (200)
   ↓
3. Suggestion saved to database (biomuseum → video_suggestions)
   ↓
4. Admin goes to Admin → Biotube → Suggestions
   ↓
5. Frontend fetches: GET /api/admin/biotube/suggestions
   ↓
6. Backend queries database and returns documents
   ↓
7. Frontend receives array and displays each suggestion
   ↓
8. Admin sees list with video titles, user names, status
```

If any step fails, the chain breaks and suggestions don't show.

---

## Common Reasons Suggestions Don't Show

1. **No suggestions submitted**
   - Fix: Go to /biotube and submit one

2. **Submitted to wrong collection**
   - Fix: Check database name and collection name
   - Should be: `biomuseum` → `video_suggestions`

3. **API is silently failing**
   - Fix: Check backend logs for errors
   - Check Network tab for response

4. **Frontend not showing data**
   - Fix: Check console.log in browser
   - Should see: `✅ Suggestions API Response: Array(...)`

5. **Wrong database name**
   - Fix: Check DB_NAME environment variable
   - Default: `biomuseum`

6. **Token expired**
   - Fix: Logout and login again

7. **Not admin user**
   - Fix: Verify account role in database

---

## Quick Fixes (In Order)

1. **Hard refresh**: Ctrl+Shift+R
2. **Clear cache**: Ctrl+Shift+Delete
3. **Check console**: F12 → Console
4. **Check network**: F12 → Network → Look for errors
5. **Check backend logs**: Look for [Biotube] error messages
6. **Check database**: `db.video_suggestions.find()`
7. **Restart backend**: Stop and start `python server.py`
8. **Restart MongoDB**: Check it's running
9. **Logout/Login**: Get fresh token
10. **Submit new suggestion**: Ensure data exists

---

## Debug Information to Collect

If submitting a bug report, include:

1. **Browser console output**
   ```
   Screenshot of F12 → Console
   Including any red error messages
   ```

2. **Network response**
   ```
   F12 → Network → /suggestions request → Response tab
   Copy the JSON response
   ```

3. **Backend logs**
   ```
   Last 20 lines from terminal where python server.py runs
   Look for [Biotube] entries
   ```

4. **Database count**
   ```
   mongosh command:
   use biomuseum
   db.video_suggestions.countDocuments({})
   ```

5. **System info**
   ```
   python --version
   node --version
   MongoDB version (if available)
   ```

---

## Success Indicators

Once working, you should see:

✅ Dashboard shows "Pending Suggestions: X" (not 0)
✅ Suggestions tab loads without errors
✅ List shows suggestions with titles and user names
✅ Status badges visible (yellow, green, etc.)
✅ Action buttons (Reviewed, Added, Dismissed) clickable
✅ User History tab shows grouped suggestions
✅ Delete buttons work on user history
✅ No red errors in browser console
✅ Backend logs show "[Biotube] Found X suggestions"

Once ALL of these pass, the system is working correctly!

---

## Need More Help?

1. Run diagnostic: `python diagnose_biotube_db.py`
2. Run API test: `python test_biotube_api.py`
3. Check logs: Look at backend terminal output
4. Verify data: Use MongoDB to check collections
5. Check frontend: Use browser DevTools extensively

The issue is almost always one of:
- Database connection
- Missing data
- Backend error (check logs!)
- Frontend not displaying

Start with the diagnostics above to narrow it down!
