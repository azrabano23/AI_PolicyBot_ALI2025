# 🚀 Deploy Ali 2025 Campaign Bot

## Quick Deployment to Vercel (Frontend) + Railway (Backend)

### Step 1: Deploy Backend to Railway
1. Go to [railway.app](https://railway.app) and sign up
2. Click "Deploy from GitHub repo"
3. Connect your GitHub account and select `AI_PolicyBot_ALI2025`
4. Add environment variables in Railway:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PORT`: 8080 (Railway default)
   - `ALI_WEBSITE_URL`: https://www.ali2025.com/
5. Railway will auto-deploy and give you a backend URL like: `https://your-app.railway.app`

### Step 2: Deploy Frontend to Vercel
1. Go to [vercel.com](https://vercel.com) and sign up
2. Click "Import Git Repository"
3. Select your `AI_PolicyBot_ALI2025` repo
4. In build settings:
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/build`
   - Install Command: `cd frontend && npm install`
5. Add environment variable in Vercel:
   - `REACT_APP_API_URL`: `https://your-backend-url.railway.app/api/chat`

### Step 3: Update Frontend Configuration
Replace the URL in the frontend code with your Railway backend URL.

## That's it! 🎉

Your bot will be live at: `https://your-project.vercel.app`

## Alternative: All-in-One Vercel Deployment

If you want everything on Vercel, we can convert to a Next.js app. Let me know!
