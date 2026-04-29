# Keyword Management Guide

## Overview
The Keyword Management screen is a new feature in the Incident Observability application that allows you to view, add, edit, and manage keywords used for incident evaluation.

## Accessing the Feature
1. Launch the Incident Observability application
2. Click on the **"🔑 Keyword Management"** tab in the main interface

## Features

### 1. Required Keywords Tab
This tab manages keywords that are required for evaluating incident worknotes and closing comments.

#### Worknotes Required Keywords
- **Purpose**: Keywords that must be present in incident worknotes for proper evaluation
- **Current Keywords**: detection, analysis, impact, log, monitoring
- **Actions**:
  - View all current keywords in the text area
  - Add new keywords using the "➕ Add Keyword" button
  - Clear all keywords using the "🗑️ Clear All" button
  - Edit keywords directly in the text area (comma-separated)

#### Closing Comments Required Keywords
- **Purpose**: Keywords that must be present in closing comments for proper evaluation
- **Current Keywords**: resolution, verification, rootcause
- **Actions**:
  - View all current keywords in the text area
  - Add new keywords using the "➕ Add Keyword" button
  - Clear all keywords using the "🗑️ Clear All" button
  - Edit keywords directly in the text area (comma-separated)

### 2. Phase Keywords Tab
This tab manages keywords associated with different incident resolution phases.

#### Available Phases:
1. **Detection Phase**
   - Keywords: detection, detected, identified, discovered, found, alarm, alert, detect, identify, discover

2. **Analysis Phase**
   - Keywords: analysis, analyzed, investigated, examined, reviewed, analyze, investigate, examine, review, troubleshoot, check

3. **Impact Phase**
   - Keywords: impact, affected, severity, priority, affect, severe, urgent, urgency, critical, complex

4. **Log Phase**
   - Keywords: log, logs, logged, logging

5. **Root Cause Phase**
   - Keywords: root cause, rootcause, root-cause, cause identified, reason, rca, cause, problem, issue

6. **Resolution Phase**
   - Keywords: resolution, resolved, fixed, corrected, remediated, fix, solution, correction

7. **Verification Phase**
   - Keywords: verification, verified, tested, confirmed, validated, checked

8. **Monitoring Phase**
   - Keywords: monitoring, monitor, monitored, tracking, observing, watching

#### Actions for Each Phase:
- View all keywords for the phase
- Add new keywords using the "➕ Add Keyword" button
- Clear all keywords using the "🗑️ Clear All" button
- Edit keywords directly in the text area (comma-separated)

## How to Use

### Adding a New Keyword
1. Navigate to the appropriate section (Required Keywords or Phase Keywords)
2. Click the "➕ Add Keyword" button
3. Enter the keyword in the dialog box
4. Click "Add" or press Enter
5. The keyword will be appended to the existing list

### Editing Keywords
1. Click directly in the text area
2. Modify the keywords (ensure they are comma-separated)
3. Click "💾 Save All Changes" to persist your changes

### Saving Changes
1. After making any modifications, click the "💾 Save All Changes" button at the bottom
2. Changes will be saved to the `config.json` file
3. A success message will confirm the save operation
4. The updated keywords will be used for all future evaluations

### Reloading Keywords
1. If you want to discard unsaved changes and reload from the config file
2. Click the "🔄 Reload from Config" button
3. All text areas will be refreshed with the current config.json values

## Important Notes

### Keyword Format
- Keywords should be separated by commas
- Leading and trailing spaces are automatically trimmed
- Empty keywords are ignored
- Keywords are case-insensitive during evaluation

### Best Practices
1. **Be Specific**: Use clear, unambiguous keywords
2. **Include Variations**: Add different forms of the same word (e.g., "analyze", "analyzed", "analysis")
3. **Test After Changes**: After modifying keywords, test with sample data to ensure proper evaluation
4. **Backup Config**: Keep a backup of your config.json file before making major changes
5. **Document Changes**: Keep track of why certain keywords were added or removed

### Impact on Evaluation
- Changes to required keywords affect the scoring algorithm
- More keywords = more comprehensive evaluation but potentially lower scores
- Fewer keywords = simpler evaluation but may miss important aspects
- Worknotes currently evaluate detection, analysis, impact, log, and monitoring only
- Phase keywords help categorize and analyze incident resolution patterns

## Troubleshooting

### Changes Not Saving
- Ensure you clicked "💾 Save All Changes" button
- Check file permissions on config.json
- Verify the application has write access to the directory

### Keywords Not Appearing
- Click "🔄 Reload from Config" to refresh from the file
- Check that config.json is properly formatted
- Restart the application if needed

### Evaluation Not Using New Keywords
- Save your changes first
- Re-evaluate your incidents after saving
- The new keywords will only apply to new evaluations

## Technical Details

### Configuration File
- Location: `config.json` in the application directory
- Format: JSON
- Encoding: UTF-8
- Structure:
  ```json
  {
    "worknotes": {
      "required_keywords": ["keyword1", "keyword2", ...]
    },
    "closing_comments": {
      "required_keywords": ["keyword1", "keyword2", ...]
    },
    "phase_keywords": {
      "phase_name": ["keyword1", "keyword2", ...]
    }
  }
  ```

### Real-time Updates
- Changes are reflected immediately in the UI
- Config file is updated only when "Save All Changes" is clicked
- Evaluations use the in-memory config until the application is restarted

## Examples

### Adding a New Detection Keyword
1. Go to "Phase Keywords" tab
2. Scroll to "Detection Phase Keywords"
3. Click "➕ Add Keyword"
4. Enter "spotted" or "noticed"
5. Click "Add"
6. Click "💾 Save All Changes"

### Modifying Worknotes Keywords
1. Go to "Required Keywords" tab
2. In the "Worknotes Required Keywords" section
3. Edit the text directly: `detection, analysis, impact, log, monitoring, documentation`
4. Click "💾 Save All Changes"

### Removing a Keyword
1. Navigate to the appropriate section
2. Edit the text area and remove the keyword (and its comma)
3. Click "💾 Save All Changes"

## Support
For issues or questions about keyword management, please refer to the main application documentation or contact your system administrator.