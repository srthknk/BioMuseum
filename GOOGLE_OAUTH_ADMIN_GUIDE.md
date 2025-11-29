# Google OAuth Admin Login - Setup & Configuration Guide

## Overview
The BioMuseum admin panel now supports secure Google OAuth 2.0 authentication with email-based access control. Only authorized email addresses can access the admin panel.

---

## How to Add Authorized Emails

### **Method 1: Local Development (Environment File)**

1. **Open the backend environment file:**
   ```
   d:\BioMuseum\backend\.env
   ```

2. **Find the `AUTHORIZED_ADMIN_EMAILS` line:**
   ```env
   AUTHORIZED_ADMIN_EMAILS=sarthaknk@gmail.com,admin@biomuseum.com
   ```

3. **Add new email addresses (comma-separated, no spaces):**
   ```env
   AUTHORIZED_ADMIN_EMAILS=sarthaknk@gmail.com,admin@biomuseum.com,newemail@example.com,another@domain.com
   ```

4. **Save the file** (Ctrl+S or Cmd+S)

5. **Restart the backend server** for changes to take effect:
   ```powershell
   cd d:\BioMuseum\backend
   python -m uvicorn server:app --reload
   ```

---

### **Method 2: Production Deployment (Render)**

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Sign in with your account

2. **Select your BioMuseum backend service:**
   - Click on the backend service name

3. **Navigate to Environment Variables:**
   - Click on "Environment" tab
   - Look for "Environment Variables" section

4. **Edit `AUTHORIZED_ADMIN_EMAILS`:**
   - Click on the pencil icon next to the variable
   - Update the email list:
     ```
     sarthaknk@gmail.com,admin@biomuseum.com,newemail@example.com
     ```
   - Click "Save"

5. **Trigger a Redeployment:**
   - Changes to environment variables require a redeploy
   - Go to "Deploys" tab
   - Click "Manual Deploy" or wait for automatic deployment
   - Service will restart with new emails

---

## Email Format Requirements

✅ **Valid formats:**
- `user@gmail.com`
- `admin@company.com`
- `name.email@domain.co.uk`

❌ **Invalid formats:**
- `user@gmail.com ` (with spaces)
- `admin@biomuseum.com, user@gmail.com` (space after comma)
- `@gmail.com` (no username)

### **Important:** No spaces after commas!
```env
✅ CORRECT:   sarthaknk@gmail.com,admin@biomuseum.com,new@example.com
❌ WRONG:     sarthaknk@gmail.com, admin@biomuseum.com, new@example.com
```

---

## How Admin Login Works

### **Step 1: User Clicks "Sign in with Google"**
- Google Sign-In button appears in the admin login modal
- Button text: "Sign in with Google" (bold, modern styling)

### **Step 2: Google OAuth Flow**
- User's browser redirects to Google's login page
- User enters their Google email and password
- Google verifies the credentials
- Google returns an authentication token to BioMuseum

### **Step 3: Email Verification**
- Backend receives the Google token
- Extracts the email address from the token
- **Checks email against `AUTHORIZED_ADMIN_EMAILS` list**
- If email is authorized → Admin token granted → Access allowed ✅
- If email is NOT authorized → 403 Forbidden error → Access denied ❌

### **Step 4: Admin Access**
- Authorized user is logged in
- Admin dashboard becomes accessible
- User can manage organisms, generate images, view analytics, etc.

---

## Current Authorized Emails

These emails have access to the admin panel:

| Email | Status |
|-------|--------|
| sarthaknk@gmail.com | ✅ Authorized |
| admin@biomuseum.com | ✅ Authorized |

---

## Testing New Email Access

### **Test Locally:**
1. Start the backend (with updated `.env`):
   ```powershell
   cd d:\BioMuseum\backend
   python -m uvicorn server:app --reload
   ```

2. Start the frontend:
   ```powershell
   cd d:\BioMuseum\frontend
   npm start
   ```

3. Navigate to admin login (http://localhost:3000)

4. Click "Sign in with Google"

5. Sign in with a newly added email address

6. Verify you get access ✅ or error message ❌

### **Test on Production:**
1. Make changes on Render dashboard
2. Wait for service to redeploy (2-3 minutes)
3. Visit https://bio-museum.vercel.app
4. Click "Admin" button
5. Click "Sign in with Google"
6. Test login with new email

---

## Error Messages

### **"Email not authorized to access admin panel"**
- ❌ The email you're using is NOT in the `AUTHORIZED_ADMIN_EMAILS` list
- ✅ Solution: Add the email to the list (see "How to Add Authorized Emails")
- Wait for backend to restart or redeploy

### **"Google login failed"**
- ❌ Something went wrong with Google OAuth
- ✅ Try again or check browser console (F12 > Console tab)
- ✅ Verify Google Client ID is correct in App.js

### **"Invalid token"**
- ❌ Google token verification failed
- ✅ This usually means Google OAuth credentials are outdated
- ✅ Contact admin to update Google OAuth credentials

---

## Quick Reference

### **Add Email Quickly (Local):**
```
1. Open: d:\BioMuseum\backend\.env
2. Find: AUTHORIZED_ADMIN_EMAILS=...
3. Add: ,newemail@example.com
4. Save file
5. Restart backend
6. Done!
```

### **Add Email Quickly (Production):**
```
1. Go to: https://dashboard.render.com
2. Select: biomuseum backend service
3. Click: Environment tab
4. Edit: AUTHORIZED_ADMIN_EMAILS variable
5. Add: ,newemail@example.com
6. Click: Save
7. Manual Deploy
8. Done! (2-3 min to activate)
```

---

## FAQ

**Q: Can I use a different email service (like Outlook, Yahoo)?**
A: Yes! Any email that works with Google Sign-In will work.

**Q: Do I need to add emails to both `.env` files?**
A: No! Only add to `backend/.env`. Frontend doesn't store the whitelist.

**Q: How many emails can I add?**
A: As many as you want. Just separate them with commas.

**Q: What if I remove an email?**
A: That email will no longer be able to log in. The person will see "Email not authorized" error.

**Q: Do changes take effect immediately?**
A: 
- **Local:** After restarting the backend
- **Production (Render):** After manual deployment (2-3 minutes)

**Q: Can users change their password?**
A: No! Login is only through Google OAuth. Password login is disabled for admins.

**Q: Is the email list case-sensitive?**
A: No! Both `user@gmail.com` and `USER@gmail.com` will match.

---

## Security Notes

✅ **Best Practices:**
- Only add emails you trust
- Use Gmail or company email accounts
- Regularly review who has access
- Remove emails when people leave the team

🔒 **Protection:**
- Google OAuth tokens are verified with Google's servers
- Email whitelist is checked on every login
- Admin tokens are unique and time-limited
- All logins are logged in the backend

---

## Backend Code Reference

The Google OAuth endpoint is located in `backend/server.py` at `/api/admin/google-login`:

```python
@app.post("/admin/google-login")
async def google_login(request: GoogleLoginRequest):
    # Verify Google token
    # Check email against AUTHORIZED_ADMIN_EMAILS
    # Return admin token if authorized
    # Return 403 Forbidden if not authorized
```

Environment variable check:
```python
authorized_emails = os.getenv("AUTHORIZED_ADMIN_EMAILS", "").lower().split(",")
email_lower = payload.get("email", "").lower()
if email_lower not in authorized_emails:
    raise HTTPException(status_code=403, detail="Email not authorized to access admin panel")
```

---

## Support

If you have issues with Google OAuth admin login:
1. Check that the email is in `AUTHORIZED_ADMIN_EMAILS`
2. Verify backend/Render has been restarted/redeployed
3. Clear browser cache and cookies
4. Check browser console (F12) for error messages
5. Check backend logs for detailed error information

---

**Last Updated:** November 29, 2025
**Status:** ✅ Google OAuth Admin Login Active
