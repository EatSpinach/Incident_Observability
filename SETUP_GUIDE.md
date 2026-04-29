# Setup Guide for Incident Evaluator

## Prerequisites Installation

### Step 1: Install Python

1. **Download Python**:
   - Visit: https://www.python.org/downloads/
   - Download Python 3.14

2. **Install Python**:
   - Run the installer
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Click "Install Now"

3. **Verify Installation**:
   ```powershell
   python --version
   ```
   Should display: `Python 3.x.x`

### Step 2: Install Required Packages

Open PowerShell or Command Prompt in the `Incident_Observability` directory and run:

```powershell
python -m pip install -r requirements.txt
```

This will install:
- openpyxl (for .xlsx files)
- xlrd (for .xls files)

## Running the Application

### Method 1: Command Line

```powershell
cd Incident_Observability
python main.py
```

### Method 2: Double-click

1. Right-click on `main.py`
2. Select "Open with" → "Python"

### Method 3: Create a Shortcut

Use the included `run_app.bat` file.

Double-click `run_app.bat` to launch the application.

## Quick Start

1. **Launch the Application**
   ```powershell
   .\run_app.bat
   ```

2. **Load Your Excel File**
   - Click "Browse" button
   - Select your incident dump Excel file
   - File should contain columns for:
     - Incident ID
     - Worknotes
     - Closing Comments

3. **Evaluate**
   - Click "Evaluate" button
   - Wait for processing to complete

4. **Review Results**
   - Check "Executive Dashboard" for summary metrics
   - Check "Application Group Analysis" for group-level breakdowns
   - Check "Resolver Analysis" for resolver-wise performance
   - Check "Evaluation Results" for incident-level scores

5. **Export**
   - File → Export Results
   - Save the evaluated data

## Troubleshooting

### Python Not Found

**Error**: `Python was not found`

**Solution**:
1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add Python installation directory (e.g., `C:\Python311\`)

### Module Not Found

**Error**: `ModuleNotFoundError` for required Excel packages

**Solution**:
```powershell
python -m pip install openpyxl xlrd
```

### Permission Denied

**Error**: Permission denied when installing packages

**Solution**:
```powershell
python -m pip install --user -r requirements.txt
```

### Excel File Not Loading

**Error**: Failed to load Excel file

**Solutions**:
1. Ensure file is .xlsx or .xls format
2. Close the file if open in Excel
3. Check file is not corrupted
4. Verify file has proper column headers

## Configuration

### Customizing Evaluation Parameters

Edit `config.json` to customize:

```json
{
  "worknotes": {
    "required_keywords": ["detection", "analysis", "impact", "log", "monitoring"]
  },
  "closing_comments": {
    "required_keywords": ["resolution", "verification", "rootcause"]
  }
}
```

Update `config.json` directly, then restart the application.

## Testing the Application

### Test with Included Sample Files

1. Run the application
2. Load one of the sample files from the `Data files` folder
3. Click Evaluate
4. Review results in the Executive Dashboard, Application Group Analysis, Resolver Analysis, and Evaluation Results views

## System Requirements

- **OS**: Windows 11
- **Python**: 3.14
- **RAM**: 4GB minimum (8GB recommended for large files)
- **Disk Space**: 100MB for application and dependencies

## Performance Tips

- **Large Files**: For files with 10,000+ records, evaluation may take 1-2 minutes
- **Memory**: Close other applications when processing large files
- **Export**: Export results incrementally if working with very large datasets

## Support

### Common Issues

1. **Slow Performance**
   - Reduce file size
   - Close unnecessary applications
   - Check system resources

2. **Incorrect Scores**
   - Review config.json parameters
   - Check if keywords match your documentation style

3. **Column Detection Failed**
   - Rename columns to include keywords like "worknote", "closing"
   - Or manually specify columns in code

### Getting Help

1. Check README.md for detailed documentation
2. Review config.json for parameter settings
3. Check the Executive Dashboard, Application Group Analysis, Resolver Analysis, and Evaluation Results views for insights

## Next Steps

After successful setup:

1. ✅ Test with sample data
2. ✅ Customize config.json for your needs
3. ✅ Load your actual incident dump
4. ✅ Review and adjust parameters based on results
5. ✅ Export evaluated data for reporting

## Updates and Maintenance

### Updating Dependencies

```powershell
python -m pip install --upgrade openpyxl xlrd
```

### Backup Configuration

Before making changes, backup your `config.json`:
```powershell
copy config.json config.json.backup
```

## Additional Resources

- Python Documentation: https://docs.python.org/
- Tkinter Tutorial: https://docs.python.org/3/library/tkinter.html

---

**Version**: 2.5.2
**Last Updated**: 2026-04-24