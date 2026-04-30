# 🚀 Deploy to PythonAnywhere Using Git

## ✅ Connect Your IBM GitHub to PythonAnywhere

This guide shows how to deploy your app from IBM GitHub Enterprise directly to PythonAnywhere.

---

## 📋 Prerequisites

- PythonAnywhere account (FREE): https://www.pythonanywhere.com
- Your IBM GitHub repository: `https://github.ibm.com/subhash-seelam/Incident_Observability.git`
- IBM GitHub credentials

---

## 🎯 Step-by-Step Deployment

### Step 1: Sign Up for PythonAnywhere

1. Go to: https://www.pythonanywhere.com
2. Click "Start running Python online in less than a minute!"
3. Create a **FREE Beginner account**
4. Verify your email
5. Log in

---

### Step 2: Clone Your Repository

1. **Open a Bash Console**
   - Go to "Consoles" tab
   - Click "Bash" to start a new console

2. **Clone Your Repository**
   ```bash
   git clone https://github.ibm.com/subhash-seelam/Incident_Observability.git
   ```

3. **Enter IBM GitHub Credentials**
   - Username: Your IBM email or username
   - Password: Your IBM GitHub password or personal access token

4. **Verify Files**
   ```bash
   cd Incident_Observability
   ls -la
   ```
   You should see: app.py, config.json, requirements.txt, templates/, etc.

---

### Step 3: Install Dependencies

In the same Bash console:

```bash
# Make sure you're in the project directory
cd ~/Incident_Observability

# Install required packages
pip3.10 install --user -r requirements.txt
```

Wait for installation to complete (1-2 minutes).

---

### Step 4: Create Web App

1. **Go to "Web" Tab**
   - Click on "Web" in the top menu

2. **Add New Web App**
   - Click "Add a new web app"
   - Click "Next" (accept the domain name)

3. **Select Framework**
   - Choose "Manual configuration"
   - Select **Python 3.10**
   - Click "Next"

4. **Complete Setup**
   - Click "Next" through remaining screens

---

### Step 5: Configure WSGI File

1. **Find WSGI Configuration**
   - In the "Web" tab, scroll to "Code" section
   - Click on the WSGI configuration file link (e.g., `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`)

2. **Replace ALL Content** with this:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/Incident_Observability'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['SECRET_KEY'] = 'pythonanywhere-secret-key-change-this-random-12345'

# Import Flask app
from app import app as application
```

3. **IMPORTANT**: Replace `YOUR_USERNAME` with your actual PythonAnywhere username!
   - Example: If your username is `john123`, use `/home/john123/Incident_Observability`

4. **Click "Save"** (top right)

---

### Step 6: Configure Directories

Still in the "Web" tab, scroll to "Code" section:

1. **Source code**
   - Set to: `/home/YOUR_USERNAME/Incident_Observability`

2. **Working directory**
   - Set to: `/home/YOUR_USERNAME/Incident_Observability`

3. **Click the checkmark** to save each setting

---

### Step 7: Create Uploads Directory

1. **Go to "Files" Tab**
2. Navigate to: `Incident_Observability`
3. Click "New directory"
4. Name it: `uploads`
5. Click "Create"

---

### Step 8: Set Permissions (Important!)

Go back to Bash console and run:

```bash
cd ~/Incident_Observability
chmod 755 uploads
```

---

### Step 9: Reload and Launch! 🚀

1. **Go to "Web" Tab**
2. Scroll to the top
3. Click the big green **"Reload YOUR_USERNAME.pythonanywhere.com"** button
4. Wait 5-10 seconds

---

### Step 10: Access Your App! 🎉

Your app is now live at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

**Example**: If your username is `john123`, your URL is:
```
https://john123.pythonanywhere.com
```

---

## 🔄 Updating Your App

When you make changes to your code:

### Option 1: Pull from Git (Recommended)

1. **Open Bash Console**
2. **Pull latest changes**:
   ```bash
   cd ~/Incident_Observability
   git pull origin master
   ```

3. **Reload Web App**
   - Go to "Web" tab
   - Click green "Reload" button

### Option 2: Edit Files Directly

1. Go to "Files" tab
2. Navigate to your file
3. Click to edit
4. Save changes
5. Reload web app

---

## 🔧 Troubleshooting

### Issue: "Could not clone repository"

**Solution**: Use Personal Access Token instead of password

1. **Create Token on IBM GitHub**
   - Go to: https://github.ibm.com/settings/tokens
   - Click "Generate new token"
   - Select scopes: `repo` (all)
   - Copy the token

2. **Clone with Token**:
   ```bash
   git clone https://YOUR_TOKEN@github.ibm.com/subhash-seelam/Incident_Observability.git
   ```

### Issue: "Module not found" Error

**Solution**: Reinstall dependencies
```bash
cd ~/Incident_Observability
pip3.10 install --user -r requirements.txt --force-reinstall
```

### Issue: "502 Bad Gateway"

**Solutions**:
1. Check WSGI file configuration
2. Verify paths are correct (use YOUR actual username)
3. Check error log in "Web" tab → "Error log"

### Issue: "Permission denied" for uploads

**Solution**:
```bash
cd ~/Incident_Observability
chmod 755 uploads
chmod 755 .
```

### Issue: App shows old version

**Solution**:
1. Pull latest changes: `git pull origin master`
2. Clear browser cache (Ctrl+Shift+Delete)
3. Reload web app in PythonAnywhere

---

## 📊 Checking Logs

### Error Log
1. Go to "Web" tab
2. Click "Error log" link
3. View recent errors

### Server Log
1. Go to "Web" tab
2. Click "Server log" link
3. View access logs

---

## 🔐 Security Best Practices

### 1. Use Personal Access Token
Instead of password, use a token for Git operations.

### 2. Change SECRET_KEY
In WSGI file, use a strong random key:
```python
os.environ['SECRET_KEY'] = 'use-a-long-random-string-here-at-least-32-characters'
```

Generate one:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Keep Dependencies Updated
```bash
cd ~/Incident_Observability
pip3.10 install --user -r requirements.txt --upgrade
```

---

## 💡 Pro Tips

### 1. Auto-Pull Updates
Create a script to pull and reload:

```bash
# In Bash console
cd ~/Incident_Observability
cat > update.sh << 'EOF'
#!/bin/bash
cd ~/Incident_Observability
git pull origin master
touch /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py
echo "Updated successfully!"
EOF

chmod +x update.sh
```

Run anytime: `./update.sh`

### 2. Monitor Your App
- Check "Web" tab regularly
- Review error logs
- Monitor CPU usage (shown in dashboard)

### 3. Backup Configuration
Save your WSGI configuration locally in case you need to recreate it.

---

## 📞 Support

### PythonAnywhere Help
- Help Pages: https://help.pythonanywhere.com
- Forums: https://www.pythonanywhere.com/forums/
- Wiki: https://help.pythonanywhere.com/pages/

### Common Help Topics
- Git on PythonAnywhere: https://help.pythonanywhere.com/pages/ExternalVCS
- Flask apps: https://help.pythonanywhere.com/pages/Flask
- Debugging: https://help.pythonanywhere.com/pages/DebuggingImportError

---

## ✅ Deployment Checklist

- [ ] Signed up for PythonAnywhere (FREE)
- [ ] Opened Bash console
- [ ] Cloned Git repository
- [ ] Installed dependencies (pip install)
- [ ] Created web app (Manual, Python 3.10)
- [ ] Configured WSGI file (replaced all content)
- [ ] Set source code directory
- [ ] Set working directory
- [ ] Created uploads folder
- [ ] Set permissions (chmod 755)
- [ ] Reloaded web app
- [ ] Tested URL - IT WORKS! 🎉
- [ ] Shared URL with team

---

## 🎊 Success!

Your app is now live at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

**Share this URL with anyone who needs to evaluate incident documentation!**

### What You Can Do Now:
- ✅ Access from anywhere in the world
- ✅ Share with unlimited users
- ✅ Upload Excel files and evaluate incidents
- ✅ Export results
- ✅ Update code via Git pull
- ✅ Monitor via PythonAnywhere dashboard

---

## 🔄 Quick Reference Commands

```bash
# Navigate to project
cd ~/Incident_Observability

# Pull latest changes
git pull origin master

# Reinstall dependencies
pip3.10 install --user -r requirements.txt

# Check files
ls -la

# View logs
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

---

**🎉 Congratulations! Your Incident Observability app is now accessible worldwide via URL!**

**Made with ❤️ - Deploy once, use forever!**