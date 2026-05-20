# Changelog - Incident Observability Dashboard

## Version 2.5.2 (2026-04-24)

### 🎨 UI Synchronization & Criteria Updates

#### Worknotes Criteria Simplification
- **Removed worknotes-only keywords**: `rootcause`, `resolution`, and `verification`
  - Worknotes evaluation now uses: detection, analysis, impact, log, monitoring
  - Closing comments evaluation remains: resolution, verification, rootcause
  - Updated default config and project documentation to match

#### Results & Analysis Table Improvements
- **Fixed Evaluation Results visibility**:
  - Resolved issue where rows were inserted into an unrendered Treeview
  - Evaluation Results tab now displays data correctly with working scrollbars

- **Synchronized analysis tab layouts**:
  - Application Group Analysis, Resolver Analysis, and Evaluation Results now use aligned full-window table layouts
  - Standardized column sizing behavior and row styling patterns
  - Improved fit-to-window behavior for analysis tables

- **Scrollbar behavior updates**:
  - Evaluation Results retains vertical and horizontal scrollbars for detailed incident-level data
  - Application Group Analysis uses vertical scrolling only
  - Resolver Analysis uses vertical scrolling only
  - Fixed bottom scrollbar placement issue in Resolver Analysis by switching the table area to a grid-based layout

#### Documentation Sync
- Updated README.md, SETUP_GUIDE.md, DASHBOARD_FEATURES.md, EXECUTIVE_SUMMARY.md, and KEYWORD_MANAGEMENT_GUIDE.md to reflect current:
  - Worknotes keyword criteria
  - Tab structure
  - Analysis views
  - Scrolling/layout behavior

---

## Version 2.5.1 (2026-04-24)

### 🐛 Bug Fixes

#### RCA Tab - Keyword Highlighting Fix
- **Fixed Root Cause and Validation Keywords Not Displaying**: Enhanced keyword matching in RCA tab
  - Issue: Required keywords like "rootcause" and "verification" were not highlighting their variations
  - Root cause variations now properly highlighted: "root cause", "rootcause", "root-cause", "cause", "rca", etc.
  - Verification variations now properly highlighted: "verification", "verified", "validated", "checked", etc.
  - Resolution variations continue to work correctly
  
- **Technical Implementation**:
  - Modified `highlight_keywords_in_text()` method in main.py
  - Built comprehensive set of required keyword variations by matching phase names
  - All variations of required keywords now highlighted with 'required' tag (yellow background, bold)
  - Phase-specific colors only applied to non-required keyword variations
  
- **Impact**: Closing comments now properly display all root cause and validation keyword matches with correct highlighting

---

## Version 2.5.0 (2026-04-22)

### 🎨 Major UI/UX Enhancements

#### New Tab Structure
- **Added Application Group Analysis Tab**: Dedicated tab for group-level analysis
  - Positioned between Executive Dashboard and Resolver Analysis
  - Clean table view without header frames
  - Matches Resolver Analysis styling for consistency
  - Export menu updated to "Export Application Group Analysis"

#### Executive Dashboard Reorganization
- **Moved Application Group Summary**: From separate tab to Executive Dashboard
  - Now displays as compact summary cards below Executive Summary
  - Two-row layout matching Executive Summary structure
  - Shows group-level quality distribution (Good/Average/Poor/Blank)

#### Enhanced Professional Styling
- **Modern Card Design**:
  - Layered frame design with subtle shadow effect
  - Outer gray frame (#E0E0E0) for depth
  - Inner white card for clean appearance
  - Professional Segoe UI font family throughout

- **Category Cards** (Worknotes Avg, Closing Comments Avg):
  - Two-tone gradient-like design
  - Colored top section with white icon
  - Bold white text on colored background
  - Fixed height for visual consistency

- **Metric Cards** (Good, Average, Poor, Blank):
  - Clean white background with subtle borders
  - Colored icons using Segoe UI Emoji
  - Bold colored values for emphasis
  - Subtle gray titles (#666) for hierarchy

#### Compact Layout Optimization
- **Reduced Spacing**:
  - LabelFrame padding: 8px → 5px
  - Section spacing: 15px/10px → 5px/3px
  - Card padding: 5px → 3px (horizontal), 5px → 2px (vertical)
  - Border width: 2px → 1px

- **Optimized Fonts**:
  - Icon size: 18pt → 14pt (24pt → 16pt for categories)
  - Value font: 16pt → 14pt (bold)
  - Title font: 10pt → 9pt
  - Category title: 14pt → 10pt

- **Result**: All sections fit within window without scrolling

#### Header Enhancements
- **Date Range Display**: Smart date detection from "Resolved" field
  - Supports 14+ date formats
  - Shows oldest to newest date range
  - Graceful fallback for parsing errors

- **Two-Column Layout**:
  - Left: Total Records + Date Range
  - Right: Evaluation Criteria
  - Professional formatting with icons

### 🗑️ Removed Features
- **Removed Category Highlighters**: Cleaner metric card appearance
  - Removed "Worknotes" and "Closing Comments" colored category columns
  - Simplified to icon + title format
  - More professional, less cluttered look

### 📊 Tab Structure (Current)
1. **Executive Dashboard**: Summary metrics + Application Group Summary
2. **Application Group Analysis**: Detailed group-level table
3. **Resolver Analysis**: Individual resolver performance (with filter)
4. **Evaluation Results**: Incident-by-incident details (with filter)

### 🎯 Quality Metrics
- **Blank Records Handling**: Properly excluded from "Poor" counts
  - Separate "Blank" category for transparency
  - Accurate quality distribution
  - Both incident-level and group-level tracking

### 💡 Benefits
1. **Better Organization**: Dedicated tab for application group analysis
2. **Professional Appearance**: Modern card design with depth and hierarchy
3. **Compact Display**: All content fits on screen without scrolling
4. **Enhanced Readability**: Segoe UI fonts and proper spacing
5. **Visual Clarity**: Color-coded metrics with professional palette
6. **Consistent Design**: Unified styling across all sections

---

## Version 2.4.0 (2026-04-21)

### 🗑️ Removed Features
- **Removed Weekly Trends Tab**: Completely removed weekly trends functionality
  - Removed `create_trends_tab()` method
  - Removed `update_weekly_trends()` method
  - Removed `detect_date_column()` method
  - Removed `parse_date()` method
  - Removed `get_week_number()` method
  - Removed `get_week_year()` method
  - Removed `group_by_week()` method
  - Removed weekly trends tab from UI
  - Removed weekly trends update call from evaluation process
- Interface now has 2 tabs only:
  - Dashboard tab (Executive Summary + Application Group Analysis)
  - Evaluation Results tab (Detailed incident breakdown)

---

## Version 2.3.0 (2026-04-21)

### 🗑️ UI Simplification
- **Removed Data Preview Tab**: Streamlined interface to 2 tabs only
  - Dashboard tab (Executive Summary + Application Group Analysis)
  - Evaluation Results tab (Detailed incident breakdown)
- Simplified workflow: Load → Evaluate → View Results
- Reduced navigation complexity

### 🐛 Bug Fixes
- **Fixed Dashboard Display Issue**: Updated field references
  - Changed `'Closing Score'` → `'Closing Comments Score'`
  - Changed `'Quality Rating'` → `'Overall Rating'`
  - Dashboard now displays correctly after evaluation

---

## Version 2.2.0 (2026-04-21)

### 📋 Column Formatting & Structure Updates

#### Data Preview Tab
- **Renamed**: "Number" → "Incident Reference"
- **Center-aligned**: Incident Reference, Resolved By, Resolved
- **Left-aligned**: Assignment Group, Worknotes, Closing Comments
- Improved column widths for better readability

#### Evaluation Results Tab - Complete Restructure
**New Column Structure:**
- S.No.
- Number
- Group
- Resolved by
- Resolved
- Worknotes Score
- Worknotes Rating (NEW - separate column)
- Closing Comments Score
- Closing Comments Rating (NEW - separate column)
- Total Score
- Total Rating (NEW - separate column)
- Worknotes Issues
- Closing Comments Issues

**Alignment:**
- Center-aligned: All columns except Issues
- Left-aligned: Group and Issues columns
- Optimized widths: 60px (S.No.), 120px (Number/Resolved), 100px (Scores/Ratings)

#### Application Group Analysis
- **Left-aligned**: Group column for better readability
- Width increased to 200px
- All other columns remain center-aligned

### 🎨 Color Coding Update
- Row colors now based on "Overall Rating" instead of "Quality Rating"
- Maintains professional color scheme (Mint Green, Sky Blue, Peach)

---

## Version 2.1.0 (2026-04-21)

### 🎨 UI/UX Improvements

#### Dashboard Optimization
- **Compact Layout**: Reduced padding and margins throughout dashboard
  - Title padding: 20px → 10px
  - Frame padding: 15px → 8px
  - Vertical spacing: 10px → 5px
- **Metric Cards**: Optimized for better screen fit
  - Icon size: 24pt → 18pt
  - Value font: 20pt → 16pt
  - Title font: 10pt → 9pt
  - Card padding: 10px → 5px
  - Border width: 2px → 1px
- **Dashboard fits on screen** without excessive scrolling

#### Professional Color Scheme
Replaced bright colors with softer, professional tones:

**Metric Card Values:**
- Good: Medium Sea Green (#52BE80)
- Average: Sky Blue (#5DADE2)
- Poor: Orange (#F39C12)
- Worknotes Average: Sky Blue (#5DADE2)
- Closing Comments Average: Purple (#AF7AC5)
- Total Incidents: Teal (#45B39D)

**Table Row Backgrounds:**
- Good: Mint Green (#A8E6CF)
- Average: Sky Blue (#B3D9FF)
- Poor: Peach (#FFE5B4)

### 📊 Feature Enhancements

#### Application Group Analysis
Added two new columns for detailed group-level insights:
- **Worknotes Avg**: Average worknotes score per group
- **Closing Avg**: Average closing comments score per group

Updated column structure:
- S.No.
- Group
- Count
- **Worknotes Avg** (NEW)
- **Closing Avg** (NEW)
- Good
- Average
- Poor

### 🗑️ Removed Features
- **Statistics Tab**: Removed for cleaner interface
  - All key metrics consolidated in Dashboard tab
  - Simplified navigation with 3 tabs instead of 4

### 📝 Documentation Updates
- Updated README.md with new color scheme and workflow
- Enhanced EXECUTIVE_SUMMARY.md with:
  - New column descriptions
  - Professional color codes
  - Compact layout notes
  - Phase keyword scoring clarification
- Created CHANGELOG.md for version tracking

### 🔧 Technical Details

#### Scoring System
- Phase keywords (synonyms) are treated equally with required keywords
- Any synonym match counts as keyword found
- Score = (Keywords Found / Total Required Keywords) × 100%

#### Configuration
All colors and keywords configurable via config.json:
- `phase_keywords`: Synonym definitions for each required keyword
- `evaluation_criteria`: Score thresholds for quality ratings
- `required_keywords`: Keywords to check in worknotes and closing comments

### 📋 Current Features

#### Executive Summary Dashboard
- Total incidents count
- Worknotes: Average score + Good/Average/Poor counts
- Closing Comments: Average score + Good/Average/Poor counts
- Overall: Good/Average/Poor distribution
- 12 metric cards in 3×4 grid layout

#### Application Group Analysis
- Sortable table with 8 columns
- Group-wise performance breakdown
- Color-coded rows based on average score
- Includes worknotes and closing comments averages

#### Evaluation Results
- Incident-by-incident detailed view
- Color-coded quality ratings
- Sortable columns
- Issues and scores for each incident


### 🎯 Quality Thresholds
- **Good**: Score > 74%
- **Average**: Score >=50% and <75%
- **Poor**: Score < 50%

### 💡 Benefits
1. **Better Screen Utilization**: Compact layout fits more information
2. **Professional Appearance**: Softer colors easier on eyes
3. **Enhanced Insights**: Group-level worknotes and closing averages
4. **Simplified Navigation**: 2 tabs for streamlined workflow
5. **Consistent Scoring**: Phase keywords treated equally

---

## Version 2.0.0 (2026-04-21)
- Initial release with keyword-based evaluation
- Dashboard with executive summary
- Application group analysis
- Configurable parameters
- Export functionality

---

**Note**: All changes maintain backward compatibility with existing Excel files and configuration.