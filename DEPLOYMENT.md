# Deployment Guide: GCP Cloud Run + Vercel

## Architecture
- **Backend (GCP Cloud Run)**: Flask API with EasyOCR
- **Frontend (Vercel)**: Static files or Next.js app

---

## Part 1: Deploy Backend to GCP Cloud Run

### Prerequisites
1. Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
2. Create a GCP project
3. Enable Cloud Run API

### Steps

1. **Login to GCP**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Build and Deploy**
```bash
# Build the container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/easyocr-api

# Deploy to Cloud Run
gcloud run deploy easyocr-api \
  --image gcr.io/YOUR_PROJECT_ID/easyocr-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300 \
  --max-instances 3
```

3. **Get the backend URL**
After deployment, you'll get a URL like:
`https://easyocr-api-xxxxx-uc.a.run.app`

---

## Part 2: Deploy Frontend to Vercel

### Option A: Current HTML Frontend

1. **Update the frontend to use your Cloud Run URL**
   - Edit `templates/index.html` 
   - Change form action to your Cloud Run URL

2. **Deploy static files to Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd templates
vercel
```

### Option B: Keep Everything on Cloud Run (Simpler)

Just deploy as-is to Cloud Run. Your HTML templates will be served from the same backend.

---

## Environment Variables

Add these to Cloud Run if needed:
```bash
gcloud run services update easyocr-api \
  --set-env-vars "UPLOAD_FOLDER=/tmp/uploads"
```

---

## Costs Estimate

**GCP Cloud Run (Free tier includes):**
- 2 million requests/month
- 360,000 GB-seconds memory
- After that: ~$0.40 per 1M requests

**Vercel (Free tier includes):**
- Unlimited static deployments
- 100 GB bandwidth/month

---

## Quick Deploy Commands

```bash
# 1. Set your project
gcloud config set project YOUR_PROJECT_ID

# 2. Deploy in one command
gcloud run deploy easyocr-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

That's it! The `--source .` flag will automatically build and deploy.
