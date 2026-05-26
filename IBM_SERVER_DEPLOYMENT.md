# IBM Internal Server Deployment Guide

## Prerequisites
- Access to an IBM internal server (Linux/Windows)
- Python 3.8 or higher installed
- Git installed
- Network access to the server

## Deployment Steps

### Step 1: Connect to IBM Server
```bash
# SSH to your IBM server
ssh your-username@ibm-server-hostname

# Or use PuTTY on Windows
```

### Step 2: Clone the Repository
```bash
cd /opt/apps  # or your preferred directory
git clone https://github.ibm.com/subhash-seelam/Incident_Observability.git
cd Incident_Observability
```

### Step 3: Set Up Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure the Application

#### Option A: Run with Flask Development Server (Testing)
```bash
python app.py
```
Access at: `http://<server-ip>:5000`

#### Option B: Run with Gunicorn (Production - Linux)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option C: Run with Waitress (Production - Windows)
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### Step 6: Run as Background Service

#### On Linux (using systemd):

Create service file:
```bash
sudo nano /etc/systemd/system/incident-observability.service
```

Add content:
```ini
[Unit]
Description=Incident Observability Web Application
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/opt/apps/Incident_Observability
Environment="PATH=/opt/apps/Incident_Observability/venv/bin"
ExecStart=/opt/apps/Incident_Observability/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable incident-observability
sudo systemctl start incident-observability
sudo systemctl status incident-observability
```

#### On Windows (using NSSM):

1. Download NSSM: https://nssm.cc/download
2. Install as service:
```cmd
nssm install IncidentObservability "C:\Path\To\venv\Scripts\python.exe" "C:\Path\To\Incident_Observability\app.py"
nssm start IncidentObservability
```

### Step 7: Configure Firewall (if needed)
```bash
# On Linux (firewalld):
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload

# On Linux (ufw):
sudo ufw allow 5000/tcp
```

### Step 8: Set Up Reverse Proxy (Optional - for production)

#### Using Nginx:
```bash
sudo nano /etc/nginx/sites-available/incident-observability
```

Add:
```nginx
server {
    listen 80;
    server_name your-server-hostname;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/incident-observability /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Access the Application

### Internal Network:
```
http://<server-ip>:5000
```

### With Nginx (port 80):
```
http://<server-hostname>
```

### With Custom Domain:
```
http://incident-observability.your-company.com
```

## Maintenance Commands

### View Logs:
```bash
# Systemd service logs
sudo journalctl -u incident-observability -f

# Application logs
tail -f /var/log/incident-observability.log
```

### Restart Service:
```bash
sudo systemctl restart incident-observability
```

### Update Application:
```bash
cd /opt/apps/Incident_Observability
git pull
sudo systemctl restart incident-observability
```

### Stop Service:
```bash
sudo systemctl stop incident-observability
```

## Troubleshooting

### Port Already in Use:
```bash
# Find process using port 5000
sudo lsof -i :5000
# Or
sudo netstat -tulpn | grep 5000

# Kill the process
sudo kill -9 <PID>
```

### Permission Issues:
```bash
# Fix ownership
sudo chown -R your-username:your-username /opt/apps/Incident_Observability

# Fix permissions
chmod +x app.py
```

### Dependencies Issues:
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## Security Considerations

1. **Change Secret Key:**
   ```bash
   export SECRET_KEY='your-secure-random-key-here'
   ```

2. **Use HTTPS:**
   - Configure SSL certificate in Nginx
   - Use Let's Encrypt for free SSL

3. **Restrict Access:**
   - Configure firewall rules
   - Use VPN or internal network only
   - Add authentication if needed

## Performance Tuning

### Gunicorn Workers:
```bash
# Formula: (2 x CPU cores) + 1
gunicorn -w 9 -b 0.0.0.0:5000 app:app  # For 4 CPU cores
```

### Increase Upload Limit:
Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

## Monitoring

### Check Application Status:
```bash
curl http://localhost:5000
```

### Monitor Resource Usage:
```bash
htop
# Or
top
```

## Contact

For issues or questions, contact: subhash.seelam@in.ibm.com