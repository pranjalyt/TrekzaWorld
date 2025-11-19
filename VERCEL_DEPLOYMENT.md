# Vercel Deployment Guide

## Issues Fixed

### 1. Images Not Loading
- Ensure all images are in the `img/` folder
- Image paths are already configured correctly (`img/filename.jpg`)
- Make sure all image files are committed to your repository

### 2. OpenRouter API Key Configuration

## Step-by-Step Deployment

### 1. Set Environment Variables in Vercel (CRITICAL!)

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Click **Add New**
4. Add the following environment variable:
   - **Name**: `OPENROUTER_API_KEY`
   - **Value**: Your OpenRouter API key (get it from https://openrouter.ai/)
   - **Environment**: Select **Production**, **Preview**, and **Development** (all three)
5. Click **Save**
6. **IMPORTANT**: After adding the environment variable, you MUST redeploy your project for it to take effect!

### 2. Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production
vercel --prod
```

#### Option B: Using GitHub Integration
1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Vercel will automatically deploy on every push

### 3. File Structure for Vercel

Make sure your project has:
```
Travel website/
├── api/
│   └── generate_trip.py
├── css/
│   ├── style.css
│   └── responsive.css
├── js/
│   ├── script.js
│   └── swiper.js
├── img/
│   └── (all your images)
├── index.html
├── login.html
├── app.py
├── vercel.json
├── requirements.txt
└── README_SETUP.md
```

### 4. Important Notes

1. **API Routes**: The API is configured in `api/generate_trip.py` for Vercel serverless functions
2. **Static Files**: HTML, CSS, JS, and images are served as static files
3. **Environment Variables**: Must be set in Vercel dashboard
4. **Image Paths**: All images should use relative paths like `img/filename.jpg`

### 5. Verify Deployment

After deployment:
1. Check that images load: Visit your site and check browser console for 404 errors
2. Test API: Try the trip planner form
3. Check logs: Go to Vercel dashboard → Functions → View logs

### 6. Troubleshooting

#### Images Still Not Loading
- **Check browser console** for 404 errors to see which images are missing
- **Verify image file names** match exactly (case-sensitive - `image 1.jpg` vs `Image 1.jpg`)
- **Ensure all images are committed** to git repository (check with `git status`)
- **Check that `img/` folder** is in the root directory
- **Verify image paths** in HTML are correct: `img/filename.jpg` (not `./img/` or `/img/`)
- **Common issue**: Spaces in filenames like `image 1(1).jpg` - make sure they're committed
- **Solution**: If images are missing, add them to git:
  ```bash
  git add img/
  git commit -m "Add images"
  git push
  ```
- **After pushing**, Vercel will automatically redeploy with images

#### API Key Error
- Verify environment variable is set in Vercel
- Make sure variable name is exactly `OPENROUTER_API_KEY`
- Redeploy after adding environment variable
- Check Vercel function logs for errors

#### API Not Working
- Check Vercel function logs
- Verify `api/generate_trip.py` exists
- Ensure `vercel.json` is configured correctly
- Test the `/api/test` endpoint first

### 7. Update API Endpoint in Frontend (if needed)

If your Vercel domain is different, update the API calls in `index.html`:
```javascript
// Change from:
const response = await fetch('/api/generate_trip', {...});

// To (if needed):
const response = await fetch('https://your-domain.vercel.app/api/generate_trip', {...});
```

However, using relative paths (`/api/generate_trip`) should work fine.

## Quick Checklist

- [ ] All images are in `img/` folder
- [ ] `vercel.json` is in root directory
- [ ] `api/generate_trip.py` exists
- [ ] `OPENROUTER_API_KEY` is set in Vercel environment variables
- [ ] All files are committed to git
- [ ] Deployed to Vercel
- [ ] Tested image loading
- [ ] Tested API endpoint

