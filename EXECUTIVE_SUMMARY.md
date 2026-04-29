# Executive Dashboard

## Overview
The Incident Observability application features a modern Executive Dashboard that provides comprehensive metrics and insights about incident evaluation results in a compact, professional layout.

## Tab Structure

The application now has 4 tabs:
1. **📊 Executive Dashboard**: Executive Summary + Application Group Summary cards
2. **📱 Application Group Analysis**: Detailed group-level analysis table
3. **👤 Resolver Analysis**: Resolver-wise performance table with application group filter
4. **📋 Evaluation Results**: Incident-by-incident detailed results with application group filter

## Executive Dashboard Components

### Header Section
- **Total Records**: Count of evaluated incidents
- **Date Range**: Automatically detected from "Resolved" field (supports 14+ date formats)
- **Evaluation Criteria**: Quality thresholds (Good/Average/Poor)

### 1. Executive Summary Section

Professional metric cards displaying key performance indicators:

#### Row 1: Worknotes Metrics
- **Worknotes Avg**: Average score percentage (with icon 📊)
- **Good**: Count of incidents with worknotes score > 74% (✅)
- **Average**: Count of incidents with worknotes score 50-74% (📈)
- **Poor**: Count of incidents with worknotes score < 50% (⚠️)
- **Blank**: Count of incidents with empty worknotes (📄)

#### Row 2: Closing Comments Metrics
- **Closing Comments Avg**: Average score percentage (with icon 📊)
- **Good**: Count of incidents with closing comments score > 74% (✅)
- **Average**: Count of incidents with closing comments score 50-74% (📈)
- **Poor**: Count of incidents with closing comments score < 50% (⚠️)
- **Blank**: Count of incidents with empty closing comments (📄)

### 2. Application Group Summary Section

Group-level quality distribution displayed as metric cards:

#### Row 1: Worknotes Group Metrics
- **Worknotes Total**: Total number of application groups (📝)
- **Good**: Groups with worknotes average > 74% (✅)
- **Average**: Groups with worknotes average 50-74% (📈)
- **Poor**: Groups with worknotes average < 50% (⚠️)
- **Blank**: Groups with blank worknotes records (📄)

#### Row 2: Closing Comments Group Metrics
- **Closing Comments Total**: Total number of application groups (💬)
- **Good**: Groups with closing comments average > 74% (✅)
- **Average**: Groups with closing comments average 50-74% (📈)
- **Poor**: Groups with closing comments average < 50% (⚠️)
- **Blank**: Groups with blank closing comments records (📄)

## Dashboard Group Analysis

The Dashboard includes application group summary metrics for group-level quality visibility.

## Quality Rating Criteria

### Score Thresholds
- **Good**: Score > 74% (Light Green background)
- **Average**: Score >=50% and <75% (Light Blue background)
- **Poor**: Score < 50% (Light Orange background)

### Scoring Methodology
Scores are calculated based on the percentage of required keywords found:
- **Score = (Keywords Found / Total Required Keywords) × 100%**

#### Worknotes Required Keywords (5 total):
1. Detection
2. Analysis
3. Impact
4. Log
5. Monitoring

#### Closing Comments Required Keywords (3 total):
1. Resolution
2. Verification
3. Rootcause

## Visual Design

### Modern Metric Cards
Each metric card features professional styling:
- **Layered Design**: Outer gray frame with inner white card for depth
- **Shadow Effect**: Subtle shadow using frame layering
- **Clean Layout**: Icon at top, value in middle, title at bottom
- **Professional Fonts**: Segoe UI family throughout

### Category Cards (Averages)
Special styling for Worknotes Avg and Closing Comments Avg:
- **Two-Tone Design**: Colored top section with white icon
- **Gradient Effect**: Professional color transitions
- **Bold Text**: White text on colored background
- **Fixed Height**: Consistent visual appearance

### Professional Color Scheme

**Metric Card Colors:**
- **Good Quality**: Medium Sea Green (#52BE80)
- **Average Quality**: Sky Blue (#5DADE2)
- **Poor Quality**: Orange (#F39C12)
- **Blank Records**: Coral Red (#FF6B6B)
- **Worknotes Average**: Sky Blue (#5DADE2)
- **Closing Comments Average**: Purple (#AF7AC5)

**Table Row Backgrounds (Application Group Analysis):**
- **Good**: Mint Green (#A8E6CF)
- **Average**: Sky Blue (#B3D9FF)
- **Poor**: Peach (#FFE5B4)

**Card Design:**
- **Outer Frame**: Light Gray (#E0E0E0) for shadow
- **Inner Card**: White (#FFFFFF) for content
- **Text Colors**: Colored values, gray (#666) titles

### Interactive Features
- Sortable columns in Application Group Analysis, Resolver Analysis, and Evaluation Results
- Vertical scrolling in all detailed analysis/result tables
- Horizontal scrolling in Evaluation Results for wide incident-level detail
- Color-coded rows based on performance

## How to Access

1. Load an Excel file with incident data
2. Click the "Evaluate" button
3. View summary results in the "Executive Dashboard" tab
4. Navigate to "Application Group Analysis", "Resolver Analysis", and "Evaluation Results" for detailed analysis

**Key Features**:
- **4-Tab Structure**: Dashboard, Application Group Analysis, Resolver Analysis, and Evaluation Results
- **Synchronized Layouts**: Analysis tables use consistent full-window styling and sizing behavior
- **Professional Design**: Modern card-based interface with depth and hierarchy
- **Smart Date Detection**: Automatic date range from "Resolved" field
- **Blank Tracking**: Separate category for empty records

## Use Cases

### For Management
- Quick overview of incident handling quality
- Identify teams/applications needing improvement
- Track overall performance metrics

### For Team Leads
- Monitor team-specific performance
- Compare against other teams
- Identify training needs

### For Quality Assurance
- Assess documentation completeness
- Track improvement trends
- Identify common gaps

## Export Capabilities

The dashboard data can be exported along with detailed results:
- Use File → Export Results
- Saves to Excel format
- Includes all original data plus evaluation scores

## Key Metrics Available

The Executive Dashboard provides comprehensive metrics:
- **Header**: Total records, date range, evaluation criteria
- **Executive Summary**: Worknotes and Closing Comments with 5 metrics each (Avg, Good, Average, Poor, Blank)
- **Application Group Summary**: Group-level quality distribution (10 metrics total)
- **Application Group Analysis**: Detailed sortable group performance table
- **Resolver Analysis**: Detailed sortable resolver performance table with filter
- **Evaluation Results**: Detailed sortable incident-level results with filter
- **Professional Design**: Modern card layout with shadow effects
- **Smart Features**: Automatic date detection, blank record tracking

## Benefits

1. **Professional Appearance**: Modern card design with depth and shadows
2. **At-a-Glance Insights**: Quickly understand overall incident quality
3. **Comprehensive Metrics**: Incident-level, group-level, and resolver-level analysis
4. **Visual Hierarchy**: Clear distinction between categories and metrics
5. **Consistent Layouts**: Synchronized styling across detailed analysis tabs
6. **Blank Tracking**: Separate category for transparency
7. **Smart Date Range**: Automatic detection from resolved dates
8. **Organized Structure**: Dedicated tabs for different analysis views

## Technical Details

### Layout Optimization
- **Reduced Padding**: 5px frame padding, 3px card spacing
- **Compact Fonts**: 14pt icons, 14pt values, 9pt titles
- **Minimal Borders**: 1px borders for clean appearance
- **Efficient Spacing**: 2-5px vertical padding

### Design Elements
- **Segoe UI Font**: Professional Windows font family
- **Layered Frames**: Outer gray + inner white for depth
- **Color Coding**: Consistent color scheme across all sections
- **Icon Integration**: Emoji icons for visual appeal

## Notes

- Dashboard updates automatically after evaluation
- All metrics are calculated in real-time
- Group summary shown only if application group data is available
- Metrics based on current evaluation configuration (config.json)
- **Phase keywords (synonyms) treated equally with required keywords** for scoring
- **Blank records excluded from Poor counts** for accurate quality assessment
- Professional design suitable for executive presentations