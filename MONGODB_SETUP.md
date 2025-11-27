# MongoDB Atlas Setup Guide - Render Deployment

## Problem: MongoDB Connection Timeouts on Render

If you're seeing `[WARN] MongoDB connection timeout` errors, this is typically due to **IP whitelist restrictions** on MongoDB Atlas.

## Solution: Configure MongoDB Atlas IP Whitelist

### Step 1: Access MongoDB Atlas
1. Go to [MongoDB Atlas Dashboard](https://cloud.mongodb.com)
2. Log in with your account
3. Select your "biomuseum" cluster

### Step 2: Configure Network Access
1. Click **"Network Access"** in the left sidebar
2. Click **"ADD IP ADDRESS"** button
3. Choose one of these options:

#### Option A: Allow All IPs (Easy - for development)
- Click **"ALLOW ACCESS FROM ANYWHERE"**
- Enter `0.0.0.0/0` 
- Click **"Confirm"**
- ⚠️ This allows any IP to connect, only use for non-sensitive data

#### Option B: Add Render's IP (Recommended - more secure)
1. Go to your Render deployment logs
2. Look for the log message showing `[OK] ✓ Successfully connected to MongoDB!` OR any error message that shows your IP
3. Copy that IP address
4. In MongoDB Atlas, click **"ADD IP ADDRESS"**
5. Paste the Render IP
6. Click **"Confirm"**

### Step 3: Verify Connection String
Ensure your MONGO_URL in `render.yaml` or environment variables is:
```
mongodb+srv://sarthaknk:adminSBES@biomuseum.m30zoo4.mongodb.net/biomuseum?retryWrites=true&w=majority
```

### Step 4: Deploy and Monitor
1. Redeploy your application on Render
2. Check logs for:
   - ✓ `[OK] DNS resolved successfully`
   - ✓ `[OK] ✓ Successfully connected to MongoDB!`

## Troubleshooting

### If DNS Resolution Fails
- Check your system's internet connection
- Verify the MongoDB cluster is still active in Atlas

### If Connection Still Times Out After IP Whitelisting
1. Check that the IP address is correctly whitelisted (exact match)
2. Wait 5-10 minutes for MongoDB Atlas to apply the rule
3. Redeploy your application

### If You See "Using local JSON storage as fallback"
- The app will use local JSON file storage instead of MongoDB
- **Warning**: Data will NOT persist across restarts
- All changes will be lost when the app restarts
- This is NOT recommended for production

## Database Credentials
- **Username**: sarthaknk
- **Password**: adminSBES
- **Database**: biomuseum
- **Cluster**: biomuseum.m30zoo4

## Connection Details
- **Host**: ac-ojscwyo-shard-00-00.m30zoo4.mongodb.net
- **Port**: 27017
- **Protocol**: MongoDB+SRV (SRV record lookup)
- **SSL/TLS**: Required

## Support
If problems persist:
1. Check MongoDB Atlas cluster status is "Running"
2. Verify no active alerts in MongoDB Atlas dashboard
3. Check Render deployment region and MongoDB cluster region match if possible
4. Review recent changes to network access rules

