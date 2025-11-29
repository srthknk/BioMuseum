# Adding GEMINI_API_KEY to Render Deployment

## Problem
The backend on Render is returning 503 Service Unavailable for the AI organism feature because `GEMINI_API_KEY` environment variable is not set.

## Solution
Add the GEMINI_API_KEY to Render's environment variables:

### Steps:

1. Go to your Render dashboard: https://dashboard.render.com

2. Select your backend service: **biomuseum** (or your service name)

3. Click on **Environment** in the left sidebar

4. Click **Add Environment Variable**

5. Add the following:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `AIzaSyBbk6TEFTYeBGIFx0cVPGi51zrj8t19GOI`

6. Click **Save**

7. The service will automatically redeploy with the new environment variable

### Environment Variables Needed on Render:

```
MONGO_URL=mongodb+srv://sarthaknk:adminSBES@biomuseum.m30zoo4.mongodb.net/biomuseum?retryWrites=true&w=majority
DB_NAME=biomuseum
FRONTEND_URL=https://bio-museum.vercel.app
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://bio-museum.vercel.app,https://biomuseum.onrender.com
GEMINI_API_KEY=AIzaSyBbk6TEFTYeBGIFx0cVPGi51zrj8t19GOI
```

## Verification

After adding the variable:

1. Wait for the service to redeploy (check the Render dashboard)
2. Test the AI endpoint:
   ```
   curl -X POST https://biomuseum.onrender.com/api/admin/organisms/ai-complete \
     -H "Content-Type: application/json" \
     -d '{"organism_name": "Lion"}'
   ```

3. You should now get a 200 response with AI-generated organism data instead of 503

## Notes

- The GEMINI_API_KEY is already configured in your local `.env` file
- Make sure the API key is valid and has the Generative AI API enabled
- After adding the variable, the service will redeploy automatically
- The deployment usually takes 1-2 minutes

## Troubleshooting

If you still get 503 after adding the variable:

1. Check Render logs: Dashboard → Service → Logs
2. Verify the key was added correctly (no extra spaces)
3. Wait for the deployment to fully complete
4. Try refreshing the page or making the request again
