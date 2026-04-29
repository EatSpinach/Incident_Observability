# Incident Observability

A comprehensive solution for evaluating incident worknotes and closing comments with both desktop and web interfaces.

## 🎯 Overview

Incident Observability provides automated evaluation of incident documentation quality based on configurable criteria. Available in two versions:

- **Desktop Application** (`main.py`) - Full-featured GUI with advanced analytics
- **Web Application** (`app.py`) - Browser-based interface accessible via URL

## ✨ Features

- **Excel File Processing**: Load and process incident dumps (.xlsx, .xls)
- **Automated Evaluation**: Score incidents based on required keywords
- **Quality Scoring**: Rate incidents as Good (>74%), Average (50-74%), or Poor (<50%)
- **Visual Results**: Color-coded displays for easy identification
- **Executive Dashboard**: Summary metrics and group analysis
- **Application Group Analysis**: Team/application-level performance tracking
- **Resolver Analysis**: Individual resolver performance metrics
- **Export Functionality**: Save evaluation results to Excel
- **Configurable Parameters**: Customize evaluation criteria via config.json
- **Keyword Management**: Built-in interface to manage evaluation keywords

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Desktop Application](#desktop-application)
- [Web Application](#web-application)
- [Configuration](#configuration)
- [Evaluation Criteria](#evaluation-criteria)
- [Dashboard Features](#dashboard-features)
- [Keyword Management](#keyword-management)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Navigate to project directory**:
   ```bash
   cd Incident_Observability
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Quick Start

### Desktop Application
```bash
# Windows
.\run_app.bat

# Or directly
python main.py
```

### Web Application
```bash
# Run locally
python app.py

# Access at http://localhost:5000
```

## 🖥️ Desktop Application

### Features
- Modern GUI with professional design
- 4-tab interface: Dashboard, Application Group Analysis, Resolver Analysis, Evaluation Results
- Real-time evaluation progress
- Advanced filtering and sorting
- Comprehensive export options

### Usage

1. **Launch**: Run `run_app.bat` or `python main.py`
2. **Load Data**: Click "Browse" or File → Load Excel
3. **Evaluate**: Click "Evaluate" button
4. **Review**: Check Dashboard for summary, other tabs for details
5. **Export**: File → Export Results

### Required Excel Columns
- Incident ID/Number
- Work Notes
- Closing Comments
- Resolved (optional, for date range)
- Application/Group/Team (optional, for group analysis)
- Resolver/Resolved By (optional, for resolver analysis)

## 🌐 Web Application

### Features
- Browser-based interface
- No installation required for users
- Mobile-friendly responsive design
- Cloud deployment ready
- Real-time processing with progress indicators

### Local Testing
```bash
python app.py
# Open http://localhost:5000 in browser
```

### Deployment Options
- **Render.com** (Recommended - Free)
- **Railway.app** (Free alternative)
- **Heroku** (Requires credit card)
- **Azure/AWS** (Enterprise)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## ⚙️ Configuration

### config.json Structure

```json
{
  "worknotes": {
    "required_keywords": ["detection", "analysis", "impact", "log", "monitoring"]
  },
  "closing_comments": {
    "required_keywords": ["resolution", "verification", "rootcause"]
  },
  "scoring": {
    "keywords_weight": 1.0
  },
  "evaluation_criteria": {
    "good_threshold": 74,
    "average_threshold": 50,
    "poor_threshold": 0
  }
}
```

### Customizing Parameters

1. Edit `config.json` directly, or
2. Use the Keyword Management tab in the desktop application
3. Restart application to apply changes

## 📊 Evaluation Criteria

### Scoring System

**Score = (Keywords Found / Total Required Keywords) × 100%**

### Worknotes Evaluation (5 keywords)
1. **Detection**: Identification of the issue
2. **Analysis**: Investigation performed
3. **Impact**: Assessment of severity
4. **Log**: Evidence captured in logs
5. **Monitoring**: Ongoing observation

### Closing Comments Evaluation (3 keywords)
1. **Resolution**: Clear resolution statement
2. **Verification**: Confirmation of fix
3. **Rootcause**: Root cause summary

### Quality Ratings
- **Good** (>74%): Most key parameters documented
- **Average** (50-74%): Adequate documentation with gaps
- **Poor** (<50%): Insufficient documentation

## 📈 Dashboard Features

### Executive Dashboard
- **Header**: Total records, date range, evaluation criteria
- **Executive Summary**: Worknotes and Closing Comments metrics
  - Average scores
  - Good/Average/Poor/Blank counts
- **Application Group Summary**: Group-level quality distribution

### Application Group Analysis
- Detailed group performance table
- Sortable columns
- Color-coded rows
- Average scores per group

### Resolver Analysis
- Individual resolver performance
- Filterable by application group
- Sortable metrics
- Performance tracking

### Evaluation Results
- Incident-by-incident details
- Filterable by application group
- Complete scoring breakdown
- Issues identification

## 🔑 Keyword Management

### Desktop Application Feature
Access via "🔑 Keyword Management" tab:

#### Required Keywords Tab
- Manage worknotes required keywords
- Manage closing comments required keywords
- Add, edit, or remove keywords
- Real-time updates

#### Phase Keywords Tab
Manage keywords for 8 phases:
- Detection, Analysis, Impact, Log
- Root Cause, Resolution, Verification, Monitoring

### Actions Available
- ➕ Add Keyword: Add new keywords
- 🗑️ Clear All: Remove all keywords
- 💾 Save All Changes: Persist to config.json
- 🔄 Reload from Config: Discard changes

## 🔧 Troubleshooting

### Common Issues

**"Could not detect required columns"**
- Ensure Excel has columns for worknotes/closing comments
- Column names should contain keywords like "worknote", "closing"

**"Failed to load file"**
- Check file format (.xlsx or .xls)
- Close file if open in Excel
- Verify file is not corrupted

**Low Scores**
- Review "Issues" columns in results
- Check if required keywords are present
- Adjust keywords in config.json if needed

**Python Not Found**
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to system PATH

**Module Not Found**
```bash
pip install -r requirements.txt
```

### Performance Tips
- Large files (10,000+ records) may take 1-2 minutes
- Close other applications when processing large files
- Export results incrementally for very large datasets

## 🚀 Deployment

### Web Application Deployment

#### Render.com (Recommended)
1. Push code to GitHub
2. Sign up at https://render.com
3. Create new Web Service
4. Connect repository
5. Deploy automatically

#### Railway.app
1. Push code to GitHub
2. Sign up at https://railway.app
3. Create new project from GitHub
4. Generate domain
5. Access via provided URL

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete instructions.

## 📁 Project Structure

```
Incident_Observability/
├── main.py                      # Desktop application
├── app.py                       # Web application
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
├── run_app.bat                  # Windows launcher
├── templates/
│   └── index.html              # Web interface
├── Procfile                     # Deployment config
├── runtime.txt                  # Python version
├── render.yaml                  # Render.com config
├── .gitignore                   # Git ignore rules
├── CHANGELOG.md                 # Version history
├── DEPLOYMENT_GUIDE.md          # Deployment instructions
├── WEB_APP_README.md            # Web app documentation
├── RENDER_DEPLOYMENT_STEPS.md   # Render-specific steps
└── IBM_GITHUB_UPLOAD_GUIDE.md   # IBM GitHub guide
```

## 📊 Output

### Evaluation Results Include
- Incident ID
- Worknotes Score (0-100)
- Closing Comments Score (0-100)
- Overall Score (average)
- Quality Rating (Good/Average/Poor)
- Worknotes Issues (specific problems)
- Closing Issues (specific problems)

### Statistics Provided
- Total incidents evaluated
- Average, median, min, max scores
- Quality distribution (count and percentage)
- Group-level analysis
- Resolver-level analysis

## 🎯 Use Cases

### For Management
- Quick overview of incident handling quality
- Identify teams/applications needing improvement
- Track overall performance metrics
- Data-driven decision making

### For Team Leads
- Monitor team-specific performance
- Compare against other teams
- Identify training needs
- Track progress over time

### For Quality Assurance
- Assess documentation completeness
- Track improvement trends
- Identify common gaps
- Ensure compliance with standards

## 📝 Version History

### v2.5.2 (2026-04-29)
- Consolidated documentation
- Removed redundant files
- Improved project structure

### v2.0.0 (2026-04-21)
- Simplified scoring to 100% keyword-based
- Updated quality ratings
- Streamlined configuration
- Added web application

### v1.0.0 (2026-04-21)
- Initial release
- Core evaluation functionality
- GUI interface
- Configurable parameters

## 🤝 Support

For issues or questions:
1. Check this README for common solutions
2. Review config.json settings
3. Examine Statistics tab for insights
4. Check platform-specific documentation

## 📄 License

This application is provided as-is for incident management and quality evaluation purposes.

---

**Made with ❤️ for better incident management**