# 🚀 Deployment Guide - Incident Observability Web Application

This guide will help you deploy the Incident Observability application to the cloud so it can be accessed via URL from anywhere.

## 📋 Table of Contents

1. [Quick Start - Local Testing](#quick-start---local-testing)
2. [Deploy to Render (Recommended - FREE)](#deploy-to-render-recommended---free)
3. [Deploy to Railway (Alternative - FREE)](#deploy-to-railway-alternative---free)
4. [Deploy to Heroku](#deploy-to-heroku)
5. [Deploy to Azure App Service](#deploy-to-azure-app-service)
6. [Troubleshooting](#troubleshooting)

---

## 🏠 Quick Start - Local Testing

Before deploying to the cloud, test the application locally:

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Open your browser and go to: `http://localhost:5000`
   - Upload an Excel file and test the evaluation

4. **Stop the Application**
   - Press `Ctrl+C` in the terminal

---

## 🌐 Deploy to Render (Recommended - FREE)

Render offers free hosting with automatic deployments from GitHub.

### Why Render?
- ✅ **FREE** tier available
- ✅ Automatic HTTPS
- ✅ Easy deployment from GitHub
- ✅ Auto-deploy on code changes
- ✅ No credit card required for free tier

### Prerequisites
- GitHub account
- Git installed on your computer

### Step-by-Step Deployment

#### 1. Prepare Your Code

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit - Web application ready for deployment"
```

#### 2. Push to GitHub

```bash
# Create a new repository on GitHub (https://github.com/new)
# Then link it to your local repository:

git remote add origin https://github.com/YOUR_USERNAME/incident-observability.git
git branch -M main
git push -u origin main
```

#### 3. Deploy on Render

1. **Sign up/Login to Render**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: `incident-observability` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Select "Free"

4. **Add Environment Variable**
   - Click "Advanced"
   - Add environment variable:
     - Key: `SECRET_KEY`
     - Value: Generate a random string (e.g., use https://randomkeygen.com/)

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - Your app will be live at: `https://incident-observability-XXXX.onrender.com`

#### 4. Access Your Application
- Click the URL provided by Render
- Share this URL with anyone who needs access!

### Auto-Deploy Updates
- Any changes you push to GitHub will automatically deploy to Render
- Just commit and push:
  ```bash
  git add .
  git commit -m "Update description"
  git push
  ```

---

## 🚂 Deploy to Railway (Alternative - FREE)

Railway is another excellent free hosting option.

### Why Railway?
- ✅ **FREE** $5 credit per month (enough for small apps)
- ✅ Very fast deployment
- ✅ Automatic HTTPS
- ✅ Simple interface

### Step-by-Step Deployment

#### 1. Prepare GitHub Repository
Follow the same steps as Render (Step 1-2 above)

#### 2. Deploy on Railway

1. **Sign up/Login to Railway**
   - Go to https://railway.app
   - Sign up with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Deployment**
   - Railway will auto-detect Python
   - It will automatically use the `Procfile`

4. **Add Environment Variable**
   - Go to "Variables" tab
   - Add:
     - `SECRET_KEY`: Generate a random string

5. **Generate Domain**
   - Go to "Settings" tab
   - Click "Generate Domain"
   - Your app will be live at: `https://incident-observability-production-XXXX.up.railway.app`

#### 3. Access Your Application
- Use the generated domain
- Share with your team!

---

## 🔷 Deploy to Heroku

Heroku is a popular platform but requires credit card verification (even for free tier).

### Prerequisites
- Heroku account (https://heroku.com)
- Heroku CLI installed (https://devcenter.heroku.com/articles/heroku-cli)

### Step-by-Step Deployment

#### 1. Login to Heroku
```bash
heroku login
```

#### 2. Create Heroku App
```bash
heroku create incident-observability-app
```

#### 3. Set Environment Variables
```bash
heroku config:set SECRET_KEY=your-random-secret-key-here
```

#### 4. Deploy
```bash
git push heroku main
```

#### 5. Open Application
```bash
heroku open
```

Your app will be at: `https://incident-observability-app.herokuapp.com`

---

## ☁️ Deploy to Azure App Service

For enterprise deployments with Microsoft Azure.

### Prerequisites
- Azure account (https://azure.microsoft.com)
- Azure CLI installed

### Step-by-Step Deployment

#### 1. Login to Azure
```bash
az login
```

#### 2. Create Resource Group
```bash
az group create --name incident-observability-rg --location eastus
```

#### 3. Create App Service Plan
```bash
az appservice plan create --name incident-observability-plan --resource-group incident-observability-rg --sku F1 --is-linux
```

#### 4. Create Web App
```bash
az webapp create --resource-group incident-observability-rg --plan incident-observability-plan --name incident-observability-app --runtime "PYTHON:3.11"
```

#### 5. Configure Deployment
```bash
az webapp config appsettings set --resource-group incident-observability-rg --name incident-observability-app --settings SECRET_KEY=your-random-secret-key
```

#### 6. Deploy Code
```bash
az webapp up --name incident-observability-app --resource-group incident-observability-rg
```

Your app will be at: `https://incident-observability-app.azurewebsites.net`

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Application Not Starting
**Problem**: App crashes on startup

**Solutions**:
- Check logs: `heroku logs --tail` (Heroku) or view logs in Render/Railway dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version matches `runtime.txt`

#### 2. File Upload Fails
**Problem**: Cannot upload Excel files

**Solutions**:
- Check file size (max 16MB by default)
- Ensure `uploads/` directory exists (created automatically)
- Verify file format (.xlsx or .xls)

#### 3. "Module Not Found" Error
**Problem**: Import errors on deployment

**Solutions**:
```bash
# Regenerate requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update requirements"
git push
```

#### 4. Slow Performance
**Problem**: App is slow or times out

**Solutions**:
- Free tiers have limited resources
- Consider upgrading to paid tier for production use
- Optimize large Excel file processing

#### 5. Session Data Lost
**Problem**: Results disappear after refresh

**Solutions**:
- This is expected behavior (sessions are temporary)
- Export results to Excel before closing
- For persistent storage, consider adding a database

---

## 🎯 Best Practices

### Security
1. **Never commit sensitive data**
   - Use environment variables for secrets
   - Add `.env` to `.gitignore`

2. **Use strong SECRET_KEY**
   - Generate random string: `python -c "import secrets; print(secrets.token_hex(32))"`

3. **Limit file uploads**
   - Current limit: 16MB
   - Adjust in `app.py` if needed

### Performance
1. **Monitor usage**
   - Check platform dashboards regularly
   - Watch for memory/CPU limits

2. **Optimize for free tier**
   - Free tiers may sleep after inactivity
   - First request after sleep may be slow

### Maintenance
1. **Keep dependencies updated**
   ```bash
   pip install --upgrade -r requirements.txt
   pip freeze > requirements.txt
   ```

2. **Regular backups**
   - Export important results
   - Keep local copies of data

---

## 📞 Support

### Platform-Specific Help
- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app
- **Heroku**: https://devcenter.heroku.com
- **Azure**: https://docs.microsoft.com/azure

### Application Issues
- Check application logs on your hosting platform
- Review error messages in browser console (F12)
- Ensure Excel files follow expected format

---

## 🎉 Success!

Once deployed, your application will be accessible via URL from anywhere in the world!

**Share your URL with:**
- Team members
- Stakeholders
- Anyone who needs to evaluate incident documentation

**Example URLs:**
- Render: `https://incident-observability-xxxx.onrender.com`
- Railway: `https://incident-observability-production-xxxx.up.railway.app`
- Heroku: `https://incident-observability-app.herokuapp.com`
- Azure: `https://incident-observability-app.azurewebsites.net`

---

## 📝 Quick Reference Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Access at http://localhost:5000
```

### Git Commands
```bash
# Add changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push origin main
```

### Render/Railway
- Push to GitHub → Auto-deploys
- No additional commands needed!

### Heroku
```bash
# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

---

**🎊 Congratulations! Your application is now accessible worldwide via URL!**