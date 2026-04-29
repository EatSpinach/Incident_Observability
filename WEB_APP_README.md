# 🌐 Incident Observability - Web Application

A modern, cloud-ready web application for evaluating incident documentation quality. Access from anywhere via URL!

## ✨ Features

- 🌍 **Web-Based**: Access from any device with a browser
- 📤 **Easy Upload**: Drag and drop Excel files
- ⚡ **Fast Evaluation**: Instant analysis of incident documentation
- 📊 **Visual Dashboard**: Beautiful statistics and metrics
- 📥 **Export Results**: Download evaluation results as Excel
- 🔒 **Secure**: Session-based data handling
- 📱 **Responsive**: Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Option 1: Use Deployed Version (Recommended)
If the application is already deployed, simply:
1. Open the URL in your browser
2. Upload your Excel file
3. Click "Evaluate Incidents"
4. View results and export if needed

### Option 2: Run Locally

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Open browser: `http://localhost:5000`

## 📖 How to Use

### Step 1: Prepare Your Excel File
Your Excel file should contain:
- **Incident ID/Number** column
- **Worknotes** column (with incident investigation details)
- **Closing Comments** column (with resolution details)
- Optional: **Application Group**, **Resolved By** columns

### Step 2: Upload File
1. Click "Choose File" button
2. Select your Excel file (.xlsx or .xls)
3. File name will appear below the button

### Step 3: Evaluate
1. Click "Evaluate Incidents" button
2. Wait for processing (usually 5-30 seconds)
3. Results will appear automatically

### Step 4: Review Results

#### Executive Summary
- **Total Incidents**: Number of records processed
- **Average Scores**: Worknotes, Closing Comments, and Overall
- **Quality Distribution**: Good, Average, Poor counts

#### Detailed Results
Switch between tabs:
- **All Results**: Complete evaluation data
- **Good**: Incidents scoring >74%
- **Average**: Incidents scoring 50-74%
- **Poor**: Incidents scoring <50%

### Step 5: Export (Optional)
1. Click "Export Results to Excel"
2. File downloads automatically
3. Open in Excel for further analysis

## 📊 Understanding Scores

### Scoring System
- **100% Keyword-Based**: Score = (Keywords Found / Total Required) × 100%
- **No Length Penalties**: Only keyword presence matters
- **Synonym Support**: Multiple variations of keywords accepted

### Quality Ratings
- **Good (>74%)**: Excellent documentation with most keywords present
- **Average (50-74%)**: Adequate documentation with some gaps
- **Poor (<50%)**: Insufficient documentation, major gaps

### Required Keywords

#### Worknotes (5 keywords)
1. **Detection**: How the issue was identified
2. **Analysis**: Investigation performed
3. **Impact**: Severity assessment
4. **Log**: Evidence in logs
5. **Monitoring**: Ongoing observation

#### Closing Comments (3 keywords)
1. **Resolution**: How it was fixed
2. **Verification**: Confirmation of fix
3. **Root Cause**: Why it happened

## 🎨 User Interface

### Color Coding
- **Mint Green**: Good quality (>74%)
- **Sky Blue**: Average quality (50-74%)
- **Peach**: Poor quality (<50%)

### Interactive Elements
- **Tabs**: Switch between different result views
- **Tables**: Sortable columns (click headers)
- **Buttons**: Hover effects for better UX

## 🔧 Configuration

The application uses `config.json` for evaluation parameters:

```json
{
  "worknotes": {
    "required_keywords": ["detection", "analysis", "impact", "log", "monitoring"]
  },
  "closing_comments": {
    "required_keywords": ["resolution", "verification", "rootcause"]
  },
  "evaluation_criteria": {
    "good_threshold": 74,
    "average_threshold": 50
  }
}
```

To modify:
1. Edit `config.json`
2. Restart the application
3. New evaluations will use updated criteria

## 📱 Browser Compatibility

### Supported Browsers
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

### Minimum Requirements
- Modern browser (released within last 2 years)
- JavaScript enabled
- Cookies enabled (for session management)

## 🔒 Security & Privacy

### Data Handling
- **Temporary Storage**: Files processed in memory
- **Session-Based**: Results stored in browser session
- **Auto-Cleanup**: Uploaded files deleted after processing
- **No Persistence**: Data not saved to database

### Best Practices
1. **Don't share URLs with sensitive data**
2. **Export results before closing browser**
3. **Use HTTPS in production** (automatic on Render/Railway)
4. **Clear browser cache** after sensitive operations

## 📊 File Size Limits

- **Maximum File Size**: 16 MB
- **Recommended**: Under 10 MB for best performance
- **Large Files**: May take longer to process

### Tips for Large Files
1. Split into smaller batches
2. Remove unnecessary columns
3. Process during off-peak hours

## 🐛 Troubleshooting

### Upload Issues
**Problem**: File won't upload
- Check file format (.xlsx or .xls only)
- Verify file size (<16 MB)
- Try different browser
- Check internet connection

### Evaluation Errors
**Problem**: Evaluation fails
- Ensure Excel has required columns
- Check for corrupted file
- Verify column names contain keywords
- Try with sample data first

### Results Not Showing
**Problem**: No results after evaluation
- Check browser console (F12) for errors
- Refresh page and try again
- Clear browser cache
- Try different browser

### Export Issues
**Problem**: Can't download results
- Check browser download settings
- Disable popup blockers
- Try different browser
- Ensure sufficient disk space

## 💡 Tips & Tricks

### For Best Results
1. **Consistent Column Names**: Use standard names like "Worknotes", "Closing Comments"
2. **Clean Data**: Remove empty rows before upload
3. **Complete Information**: Ensure all required columns present
4. **Regular Exports**: Download results frequently

### Performance Optimization
1. **Smaller Batches**: Process 100-500 records at a time
2. **Close Other Tabs**: Free up browser memory
3. **Stable Connection**: Use reliable internet
4. **Modern Browser**: Keep browser updated

## 🆚 Web vs Desktop Version

### Web Application Advantages
- ✅ Access from anywhere
- ✅ No installation required
- ✅ Always up-to-date
- ✅ Share via URL
- ✅ Cross-platform (Windows, Mac, Linux)
- ✅ Mobile-friendly

### Desktop Application Advantages
- ✅ Works offline
- ✅ Faster for very large files
- ✅ More advanced features
- ✅ Local data storage

## 📞 Support

### Getting Help
1. Check this README
2. Review DEPLOYMENT_GUIDE.md
3. Check browser console for errors
4. Verify Excel file format

### Common Questions

**Q: Can I use this offline?**
A: No, web version requires internet. Use desktop version for offline use.

**Q: Is my data secure?**
A: Yes, data is processed in memory and not stored permanently.

**Q: Can multiple users access simultaneously?**
A: Yes, each user has their own session.

**Q: How long are results stored?**
A: Until you close the browser or session expires.

**Q: Can I customize evaluation criteria?**
A: Yes, edit config.json and restart the application.

## 🎯 Use Cases

### Team Collaboration
- Share URL with team members
- Everyone can evaluate their incidents
- Consistent evaluation criteria

### Quality Audits
- Regular documentation reviews
- Track improvement over time
- Generate compliance reports

### Training
- Demonstrate good documentation practices
- Show real-time evaluation
- Interactive learning tool

## 🔄 Updates & Maintenance

### Checking for Updates
- Web version: Automatically updated on deployment
- Desktop version: Check GitHub for new releases

### Backup & Recovery
- Export results regularly
- Keep local copies of important data
- No automatic backups in web version

## 📈 Future Enhancements

Potential features in development:
- 📊 Advanced analytics and trends
- 💾 Database integration for history
- 👥 User authentication and roles
- 📧 Email notifications
- 🔗 API integration
- 📱 Native mobile apps

## 🎉 Success Stories

Use this application to:
- ✅ Improve incident documentation quality
- ✅ Standardize evaluation process
- ✅ Train new team members
- ✅ Generate quality reports
- ✅ Track improvement metrics

## 📝 Version Information

- **Current Version**: 2.0.0 (Web Edition)
- **Release Date**: 2026-04-29
- **Based On**: Desktop Edition v2.0.0
- **Framework**: Flask + HTML/CSS/JavaScript

## 🙏 Acknowledgments

Built with:
- Flask (Python web framework)
- OpenPyXL (Excel processing)
- Modern HTML5/CSS3/JavaScript
- Love and dedication to quality! ❤️

---

**🌟 Ready to improve your incident documentation quality? Upload your first file and get started!**