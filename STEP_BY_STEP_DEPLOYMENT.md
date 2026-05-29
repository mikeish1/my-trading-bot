# 🚀 STEP-BY-STEP DEPLOYMENT GUIDE
## Railway Deployment - Complete Walkthrough

---

## PART 1: Prepare Your Files (5 minutes)

### Step 1: Download This Package

You should have received a folder called `DEPLOYMENT_PACKAGE` containing:
- `main.py`
- `requirements.txt`
- `Procfile`
- `runtime.txt`

### Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. **Repository name:** `my-trading-bot`
3. **Description:** My AI Trading System
4. Make it **Public** (or Private if you prefer)
5. **DO NOT** check "Add a README file"
6. Click **"Create repository"**

### Step 3: Upload Your Files

1. On your new repository page, click **"uploading an existing file"**
2. Drag and drop ALL files from the `DEPLOYMENT_PACKAGE` folder:
   - `main.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
3. **IMPORTANT:** Also upload your `scripts` folder with `advanced_portfolio_analyzer.py`
4. Type a commit message: "Initial deployment"
5. Click **"Commit changes"**

---

## PART 2: Deploy on Railway (3 minutes)

### Step 4: Create Railway Account

1. Go to: https://railway.app
2. Click **"Login"**
3. Click **"Continue with GitHub"**
4. Authorize Railway to access your GitHub

### Step 5: Create New Project

1. Click **"New Project"**
2. Click **"Deploy from GitHub repo"**
3. Select your repository: `my-trading-bot`
4. Click **"Deploy Now"**

### Step 6: Wait for Deployment

You'll see:
```
🔨 Building...
📦 Installing dependencies...
🚀 Deploying...
✅ Deployment successful!
```

This takes 2-5 minutes.

### Step 7: Check Your Deployment

1. Click on your project
2. Click **"Deployments"**
3. Click the latest deployment
4. You should see logs showing:
   ```
   🚀 Running Trading System for NVDA
   📊 RECOMMENDATION:
   Ticker: NVDA
   Score: 7.7/10
   Recommendation: Buy - Good multi-factor alignment
   ```

---

## PART 3: Set Up Daily Automation (Optional)

### Step 8: Add Environment Variables (Optional)

If you want to customize:
1. Go to your Railway project
2. Click **"Variables"**
3. Add:
   - `DEFAULT_TICKER` = `NVDA` (or your preferred stock)

### Step 9: Set Up Cron Job (For Daily Runs)

Railway doesn't have built-in cron, so use **GitHub Actions** instead:

1. In your GitHub repository, create folder: `.github/workflows`
2. Create file: `daily-trading.yml`
3. Add this content:
```yaml
name: Daily Trading Recommendation

on:
  schedule:
    - cron: '30 13 * * 1-5'  # 9:30 AM ET, Monday-Friday
  workflow_dispatch:  # Allow manual trigger

jobs:
  recommend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run Trading System
        run: |
          python main.py
```

4. Commit and push this file
5. Go to GitHub → Actions → Your workflow
6. Click **"Run workflow"** to test

---

## ✅ SUCCESS CHECKLIST

- [ ] GitHub repository created
- [ ] All files uploaded (main.py, requirements.txt, Procfile, runtime.txt)
- [ ] Railway project created
- [ ] Deployment successful
- [ ] Logs show trading recommendation
- [ ] (Optional) GitHub Actions workflow added for daily runs

---

## 🆘 TROUBLESHOOTING

### Error: "No Python app detected"
**Solution:** Make sure you uploaded `requirements.txt` and `runtime.txt`

### Error: "Application failed to respond"
**Solution:** Check the logs in Railway → Deployments → Latest deployment

### Error: "Module not found"
**Solution:** Make sure `scripts/advanced_portfolio_analyzer.py` is in your repository

---

## 📞 NEED HELP?

If you get stuck:
1. Check Railway logs (they show exactly what went wrong)
2. Make sure all files are uploaded to GitHub
3. Verify the file structure matches this guide

**You're doing great!** This is easier than it looks. 🚀
