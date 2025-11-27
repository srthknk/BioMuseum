# Quick GitHub Setup - Copy & Paste Commands

## Step 1: Create Repository on GitHub
Go to: https://github.com/new
- Name: `BioMuseum`
- Description: `Biology Museum Database`
- Choose "Public"
- Click "Create repository"

## Step 2: Copy & Paste These Commands

```powershell
cd d:\BioMuseum

# Configure Git
git config user.email "your-email@gmail.com"
git config user.name "Your Name"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/BioMuseum.git

# Rename branch to main if desired (optional)
git branch -M main

# Push to GitHub (use your token as password if prompted)
git push -u origin master
```

## Step 3: Create GitHub Personal Access Token (if needed)

If Git asks for password:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `BioMuseum-Deployment`
4. Select scopes: `repo` (all)
5. Generate and copy token
6. Use token as password when Git prompts

## Step 4: Verify Push
Run: `git log --oneline -5`
You should see your commits.

---

**After push is successful:**
1. Go to your GitHub repo URL
2. You should see all project files
3. Proceed with Vercel and Render deployment (see DEPLOYMENT_COMPLETE.md)

