# Incident Observability

A desktop GUI application for evaluating incident worknotes and closing comments based on predefined parameters.

## Features

- **Excel File Processing**: Load and process incident dumps from Excel files (.xlsx, .xls)
- **Automated Evaluation**: Evaluate worknotes and closing comments based on configurable criteria
- **Quality Scoring**: Score incidents based on:
  - Presence of required keywords (100% weight)
- **Visual Results**: Color-coded results display (Good, Average, Poor)
- **Executive Dashboard**: Summary metrics and analysis views
- **Export Functionality**: Export evaluation results back to Excel
- **Configurable Parameters**: Easily customize evaluation criteria via config.json

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Navigate to the project directory**:
   ```bash
   cd "Incident_Observability"
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Step-by-Step Guide

1. **Launch the Application**
   - Run `python main.py`
   - The GUI window will open

2. **Load Excel File**
   - Click "Browse" button or use File → Load Excel
   - Select your incident dump Excel file
   - The application will automatically detect columns containing worknotes and closing comments

3. **Evaluate Incidents**
   - Click the "Evaluate" button
   - The application will process all incidents based on configured parameters
   - Progress will be shown in the status bar

4. **View Dashboard**
   - Navigate to "📊 Dashboard" tab to see:
     - Executive Summary with all key metrics
     - Application Group Analysis with detailed breakdowns
   - Results are color-coded:
     - **Mint Green**: Good (Score > 74%)
     - **Sky Blue**: Average (Score >=50% and <75%)
     - **Peach**: Poor (Score < 50%)

5. **View Detailed Results**
   - Switch to "Evaluation Results" tab for incident-by-incident details
   - Color-coded rows for easy identification

6. **Export Results**
   - Use File → Export Results
   - Save the combined data (original + evaluation results) to a new Excel file

## Configuration

### config.json Structure

The application uses `config.json` to define evaluation parameters:

```json
{
  "worknotes": {
    "required_keywords": ["detection", "analysis", "impact", "log",
                         "monitoring"]
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

### Evaluation Parameters

#### Worknotes Evaluation
The application checks for these required keywords:
1. **Detection**: Identification of the issue
2. **Analysis**: Investigation performed
3. **Impact**: Assessment of severity
4. **Log**: Evidence captured in logs
5. **Monitoring**: Ongoing observation

#### Closing Comments Evaluation
Focuses on these required keywords:
- **Resolution**: Clear resolution statement
- **Verification**: Confirmation of fix
- **Rootcause**: Root cause summary

### Customizing Parameters

1. **Edit config.json** directly
2. Restart the application to apply updated parameters

### Scoring System

The scoring is based 100% on keyword presence:
- `keywords_weight`: 1.0 (100%)
- Score = (Keywords Found / Total Keywords) × 100%

## Excel File Format

### Expected Columns

The application automatically detects columns containing:
- **Incident ID**: Any column with "incident", "id", "number", or "ticket"
- **Worknotes**: Columns with "worknote", "work note", "notes", or "comments"
- **Closing Comments**: Columns with "closing", "close comment", or "resolution"

### Sample Excel Structure

| Incident ID | Worknotes | Closing Comments | Status |
|-------------|-----------|------------------|--------|
| INC001 | Alert received... | Resolved by... | Closed |
| INC002 | Detection of... | Validated and... | Closed |

## Evaluation Scoring

### Score Calculation

Each incident receives three scores:
1. **Worknotes Score** (0-100)
2. **Closing Comments Score** (0-100)
3. **Overall Score** (average of above)

### Score Calculation

**Score = (Required Keywords Found / Total Required Keywords) × 100%**

The score is based purely on the percentage of required keywords found in the text.

### Quality Ratings

Based on the percentage of required keywords found:
- **Good** (> 74%): Most key parameters documented
- **Average** (>=50% and <75%): Adequate documentation with some gaps
- **Poor** (< 50%): Insufficient documentation, major gaps

## Output

### Evaluation Results Include

- Incident ID
- Worknotes Score
- Closing Comments Score
- Overall Score
- Quality Rating
- Worknotes Issues (specific problems identified)
- Closing Issues (specific problems identified)

### Statistics Provided

- Total incidents evaluated
- Average, median, min, max scores
- Quality distribution (count and percentage)
- Top issues identified
- Common problems across incidents

## Troubleshooting

### Common Issues

1. **"Could not detect required columns"**
   - Ensure your Excel file has columns for worknotes or closing comments
   - Column names should contain keywords like "worknote", "closing", etc.

2. **"Failed to load file"**
   - Check file format (.xlsx or .xls)
   - Ensure file is not corrupted
   - Close file if open in Excel

3. **Low Scores**
   - Review the "Issues" columns in results
   - Check if required keywords are present
   - Ensure all key parameters are documented

### Tips for Better Scores

1. **Include All Required Keywords**: Ensure worknotes cover all 5 required keywords
2. **Use Keywords Naturally**: Include required keywords in your documentation
3. **Be Specific**: Provide clear detection, analysis, impact, log, and monitoring details

## Advanced Features

### Batch Processing
- Load large Excel files (tested with 10,000+ records)
- Efficient processing with progress indication

### Customization
- Modify evaluation criteria without code changes
- Add/remove keywords as needed
- Adjust scoring weights to match your requirements

### Export Options
- Combined data (original + evaluation results)
- Preserves all original columns
- Adds evaluation columns for analysis

## Support

For issues or questions:
1. Check the configuration in config.json
2. Review the Statistics tab for insights
3. Examine specific incident issues in the results

## Version History

- **v2.0.0** (2026-04-21)
  - Simplified scoring to 100% keyword-based evaluation
  - Removed length, quality, and format scoring components
  - Updated quality ratings: Good (>74%), Average (>=50% and <75%), Poor (<50%)
  - Removed "closure" keyword from evaluation
  - Streamlined configuration and settings UI

- **v1.0.0** (2026-04-21)
  - Initial release
  - Core evaluation functionality
  - GUI interface
  - Configurable parameters
  - Export functionality
  - Statistics dashboard

## License

This application is provided as-is for incident management and quality evaluation purposes.