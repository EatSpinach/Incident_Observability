"""
Incident Evaluator Application
A desktop GUI application to evaluate incident worknotes and closing comments
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import os
import json
from collections import Counter

import openpyxl
import xlrd


class IncidentEvaluator:
    def __init__(self, root):
        self.root = root
        self.root.title("Incident Observability - Professional Edition")
        self.root.geometry("1200x800")
        
        # Modern color scheme
        self.colors = {
            'primary': '#2C3E50',      # Dark blue-gray
            'secondary': '#3498DB',    # Bright blue
            'accent': '#E74C3C',       # Red accent
            'success': '#27AE60',      # Green
            'warning': '#F39C12',      # Orange
            'bg_light': '#ECF0F1',     # Light gray
            'bg_dark': '#34495E',      # Dark gray
            'text_dark': '#2C3E50',    # Dark text
            'text_light': '#7F8C8D',   # Light text
            'card_bg': '#FFFFFF',      # White cards
            'border': '#BDC3C7'        # Border gray
        }
        
        # Configure root window background
        self.root.configure(bg=self.colors['bg_light'])
        
        # Data storage
        self.df = []
        self.evaluation_results = []
        self.config = self.load_default_config()
        self.worknotes_req_kw = None
        self.closing_comments_req_kw = None
        self.selected_group = tk.StringVar(value="All Groups")
        
        # Configure modern ttk style
        self.setup_styles()
        
        # Create UI
        self.create_menu()
        self.group_analysis_tree = None
        self.individual_analysis_tree = None
        self.create_main_ui()
    def setup_styles(self):
        """Configure modern ttk styles for professional appearance"""
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        
        # Configure Notebook (tabs)
        style.configure('TNotebook', background=self.colors['bg_light'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background=self.colors['bg_dark'],
                       foreground='white',
                       padding=[20, 10],
                       font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['secondary'])],
                 foreground=[('selected', 'white')])
        
        # Configure Frames
        style.configure('TFrame', background=self.colors['bg_light'])
        style.configure('Card.TFrame', background=self.colors['card_bg'], 
                       relief='raised', borderwidth=1)
        
        # Configure Labels
        style.configure('TLabel', background=self.colors['bg_light'], 
                       foreground=self.colors['text_dark'])
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'),
                       foreground=self.colors['primary'])
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'),
                       foreground=self.colors['secondary'])
        
        # Configure Buttons with modern look
        style.configure('TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=[15, 8],
                       font=('Arial', 9, 'bold'))
        style.map('TButton',
                 background=[('active', self.colors['primary']),
                           ('pressed', self.colors['primary'])])
        
        # Configure LabelFrame
        style.configure('TLabelframe', background=self.colors['bg_light'],
                       borderwidth=2, relief='solid')
        style.configure('TLabelframe.Label',
                       background=self.colors['bg_light'],
                       foreground=self.colors['primary'],
                       font=('Arial', 11, 'bold'))
        
        # Configure Entry and Combobox
        style.configure('TEntry', fieldbackground='white', 
                       borderwidth=1, relief='solid')
        style.configure('TCombobox', fieldbackground='white',
                       borderwidth=1, relief='solid')
        
        # Configure Treeview with modern colors
        style.configure('Treeview',
                       background='white',
                       foreground=self.colors['text_dark'],
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid')
        style.configure('Treeview.Heading',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=1,
                       relief='raised',
                       font=('Arial', 9, 'bold'))
        style.map('Treeview.Heading',
                 background=[('active', self.colors['secondary'])])
    
        
    def load_default_config(self):
        """Load evaluation parameters from config file or use defaults"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Fallback to default config
        return {
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
                "fair_threshold": 54,
                "poor_threshold": 50
            },
            "phase_keywords": {
                "detection": ["detection", "detected", "identified", "discovered", "found", "alarm", "alert", "detect", "identify", "discover"],
                "analysis": ["analysis", "analyzed", "investigated", "examined", "reviewed", "analyze", "investigate", "examine", "review", "troubleshoot", "check"],
                "impact": ["impact", "affected", "severity", "priority", "affect", "severe", "urgent", "urgency", "critical", "complex"],
                "log": ["log", "logs", "logged", "logging"],
                "rootcause": ["root cause", "rootcause", "cause identified", "reason", "rca", "cause", "problem", "issue"],
                "resolution": ["resolution", "resolved", "fixed", "corrected", "remediated", "fix", "solution", "correction"],
                "verification": ["verification", "verified", "tested", "confirmed", "validated", "checked"],
                "monitoring": ["monitoring", "monitor", "monitored", "tracking", "observing", "watching"]
            }
        }
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Excel", command=self.load_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Export Complete Dataset", command=self.export_complete_dataset)
        file_menu.add_command(label="Export Application Group Analysis", command=self.export_group_analysis)
        file_menu.add_command(label="Export Resolver Analysis", command=self.export_resolver_analysis)
        file_menu.add_command(label="Export Evaluation Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Manage Keywords", command=self.open_keyword_management)
        settings_menu.add_command(label="Reset to Defaults", command=self.reset_config)
    
    def create_main_ui(self):
        """Create main user interface"""
        # Top frame - File selection
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Excel File:").pack(side=tk.LEFT, padx=5)
        self.file_path_var = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.file_path_var, width=60).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Browse", command=self.load_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Evaluate", command=self.evaluate_incidents).pack(side=tk.LEFT, padx=5)
        
        # Middle frame - Notebook with tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 0: Executive Dashboard
        self.dashboard_frame = ttk.Frame(notebook)
        notebook.add(self.dashboard_frame, text="📊 Executive Dashboard")
        self.create_dashboard_tab()
        
        # Tab 1: Application Group Analysis
        self.group_analysis_frame = ttk.Frame(notebook)
        notebook.add(self.group_analysis_frame, text="📱 Application Group Analysis")
        self.create_group_analysis_tab()
        
        # Tab 2: Resolver Analysis
        self.individual_frame = ttk.Frame(notebook)
        notebook.add(self.individual_frame, text="👤 Resolver Analysis")
        self.create_individual_tab()
        
        # Tab 3: Evaluation Results
        self.results_frame = ttk.Frame(notebook)
        notebook.add(self.results_frame, text="📋 Evaluation Results")
        self.create_results_tab()
        
        # Tab 4: RCA (Root Cause Analysis)
        self.rca_frame = ttk.Frame(notebook)
        notebook.add(self.rca_frame, text="🔍 RCA")
        self.create_rca_tab()
        
        # Tab 5: Monthly Trend Analysis
        self.trend_frame = ttk.Frame(notebook)
        notebook.add(self.trend_frame, text="📈 Monthly Trends")
        self.create_trend_tab()
        
        # Bottom frame - Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_results_tab(self):
        """Create evaluation results tab"""
        # Filter and Actions frame
        actions_frame = ttk.Frame(self.results_frame)
        actions_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        # Application Group Filter on the left
        filter_frame = ttk.Frame(actions_frame)
        filter_frame.pack(side=tk.LEFT)
        
        ttk.Label(filter_frame, text="Filter by Application Group:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        
        # Dropdown will be populated when data is loaded
        self.results_filter_var = tk.StringVar(value='All')
        self.results_filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.results_filter_var,
                                                     values=['All'], state='readonly', width=50)
        self.results_filter_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        self.results_filter_dropdown.bind('<<ComboboxSelected>>', lambda e: self.display_results(self.results_filter_var.get()))
        
        # Export button on the right
        ttk.Button(actions_frame, text="Export Evaluation Results", command=self.export_results).pack(side=tk.RIGHT)
        
        # Treeview for results
        tree_frame = ttk.Frame(self.results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.results_tree = ttk.Treeview(tree_frame,
                                         yscrollcommand=vsb.set,
                                         xscrollcommand=hsb.set)
        vsb.config(command=self.results_tree.yview)
        hsb.config(command=self.results_tree.xview)

        self.results_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
    
    def create_rca_tab(self):
        """Create RCA tab with incident filtering and keyword highlighting"""
        # Main container
        main_container = ttk.Frame(self.rca_frame, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_container, text="Root Cause Analysis - Keyword Highlighting", 
                               font=('Segoe UI', 14, 'bold'),
                               foreground=self.colors['primary'])
        title_label.pack(pady=(0, 10))
        
        # Filter frame
        filter_frame = ttk.Frame(main_container)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter by Incident Number:", 
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.rca_incident_var = tk.StringVar()
        self.rca_incident_dropdown = ttk.Combobox(filter_frame,
                                                  textvariable=self.rca_incident_var,
                                                  values=['Select an incident...'],
                                                  state='normal',
                                                  width=50)
        self.rca_incident_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        self.rca_incident_dropdown.current(0)
        self.rca_incident_dropdown.bind('<<ComboboxSelected>>', self.display_rca_analysis)
        self.rca_incident_dropdown.bind('<Return>', self.display_rca_analysis)
        
        ttk.Button(filter_frame, text="Clear", 
                  command=self.clear_rca_filter).pack(side=tk.LEFT)
        
        # Content frame with two sections
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Worknotes section
        worknotes_frame = ttk.LabelFrame(content_frame, text="Work Notes", padding="10")
        worknotes_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.rca_worknotes_text = tk.Text(worknotes_frame, wrap=tk.WORD, 
                                         font=('Consolas', 10), height=15)
        worknotes_scroll = ttk.Scrollbar(worknotes_frame, command=self.rca_worknotes_text.yview)
        self.rca_worknotes_text.configure(yscrollcommand=worknotes_scroll.set)
        
        self.rca_worknotes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        worknotes_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Closing comments section
        closing_frame = ttk.LabelFrame(content_frame, text="Closing Comments", padding="10")
        closing_frame.pack(fill=tk.BOTH, expand=True)
        
        self.rca_closing_text = tk.Text(closing_frame, wrap=tk.WORD, 
                                       font=('Consolas', 10), height=15)
        closing_scroll = ttk.Scrollbar(closing_frame, command=self.rca_closing_text.yview)
        self.rca_closing_text.configure(yscrollcommand=closing_scroll.set)
        
        self.rca_closing_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        closing_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure tags for highlighting
        self.configure_rca_tags()
        
        # Initial message
        self.rca_worknotes_text.insert(1.0, "Load and evaluate data, then select an incident to view keyword analysis.")
        self.rca_closing_text.insert(1.0, "Load and evaluate data, then select an incident to view keyword analysis.")
        self.rca_worknotes_text.config(state=tk.DISABLED)
        self.rca_closing_text.config(state=tk.DISABLED)
    
    def configure_rca_tags(self):
        """Configure text tags for keyword highlighting"""
        # Required keywords - bold and colored
        self.rca_worknotes_text.tag_configure('required', 
                                             background='#ffeb3b', 
                                             foreground='#000000',
                                             font=('Consolas', 10, 'bold'))
        self.rca_closing_text.tag_configure('required', 
                                           background='#ffeb3b', 
                                           foreground='#000000',
                                           font=('Consolas', 10, 'bold'))
        
        # Phase keywords - different colors for each phase
        phase_colors = {
            'detection': '#e3f2fd',
            'analysis': '#e1f5fe',
            'impact': '#e0f7fa',
            'log': '#e0f2f1',
            'rootcause': '#f1f8e9',
            'resolution': '#fff9c4',
            'verification': '#fff3e0',
            'monitoring': '#fce4ec'
        }
        
        for phase, color in phase_colors.items():
            self.rca_worknotes_text.tag_configure(phase, 
                                                 background=color, 
                                                 foreground='#000000')
            self.rca_closing_text.tag_configure(phase, 
                                               background=color, 
                                               foreground='#000000')
    
    def update_rca_dropdown(self):
        """Update RCA dropdown with incident numbers"""
        if not self.df or not self.evaluation_results:
            return
        
        cols = self.detect_columns()
        if not cols:
            return
        
        incident_col = cols.get('incident')
        if not incident_col:
            return
        
        # Get incident numbers
        incidents = []
        for row in self.df:
            incident_num = self.safe_cell_text(row.get(incident_col, ''))
            if incident_num:
                incidents.append(incident_num)
        
        if incidents:
            self.rca_incident_dropdown['values'] = ['Select an incident...'] + incidents
            self.rca_incident_dropdown.current(0)
    
    def clear_rca_filter(self):
        """Clear RCA filter"""
        self.rca_incident_dropdown.current(0)
        self.rca_worknotes_text.config(state=tk.NORMAL)
        self.rca_closing_text.config(state=tk.NORMAL)
        self.rca_worknotes_text.delete(1.0, tk.END)
        self.rca_closing_text.delete(1.0, tk.END)
        self.rca_worknotes_text.insert(1.0, "Select an incident to view keyword analysis.")
        self.rca_closing_text.insert(1.0, "Select an incident to view keyword analysis.")
        self.rca_worknotes_text.config(state=tk.DISABLED)
        self.rca_closing_text.config(state=tk.DISABLED)
    def create_trend_tab(self):
        """Create monthly trend analysis tab"""
        # Actions frame with export button
        actions_frame = ttk.Frame(self.trend_frame)
        actions_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        ttk.Button(actions_frame, text="Export Monthly Trends",
                  command=self.export_trend_results).pack(side=tk.RIGHT)
        
        # Treeview for monthly breakdown
        tree_frame = ttk.Frame(self.trend_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.trend_tree = ttk.Treeview(tree_frame,
                                       yscrollcommand=vsb.set,
                                       xscrollcommand=hsb.set)
        vsb.config(command=self.trend_tree.yview)
        hsb.config(command=self.trend_tree.xview)
        
        self.trend_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
    
    def update_trend_analysis(self):
        """Update monthly trend analysis - show breakdown by group and month"""
        # Clear existing data
        for item in self.trend_tree.get_children():
            self.trend_tree.delete(item)
        
        if not self.evaluation_results:
            return
        
        # Parse dates and group by month and application group
        from datetime import datetime
        from collections import defaultdict
        
        # Structure: monthly_data[month_key][group] = {scores}
        monthly_group_data = {}
        
        for result in self.evaluation_results:
            resolved_date = result.get('Resolved', '')
            app_group = result.get('Group', 'Ungrouped')
            
            if not resolved_date or str(resolved_date).strip().lower() in ['', 'none', 'null', 'n/a']:
                continue
            
            try:
                # Parse date
                date_str = str(resolved_date).strip()
                date_part = date_str.split()[0] if ' ' in date_str else date_str
                
                parsed_date = None
                formats = [
                    '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y',
                    '%Y/%m/%d', '%d-%b-%Y', '%d-%B-%Y', '%b-%d-%Y',
                    '%Y-%m-%d %H:%M:%S', '%d-%m-%Y %H:%M:%S'
                ]
                
                for fmt in formats:
                    try:
                        parsed_date = datetime.strptime(date_str if '%H:%M:%S' in fmt else date_part, fmt)
                        break
                    except:
                        continue
                
                if parsed_date:
                    month_key = parsed_date.strftime('%Y-%m')  # Format: 2024-01
                    month_display = parsed_date.strftime('%B %Y')  # Format: January 2024
                    
                    # Create key for month-group combination
                    key = (month_key, month_display, app_group)
                    
                    if key not in monthly_group_data:
                        monthly_group_data[key] = {
                            'count': 0,
                            'total_score': 0,
                            'worknotes_total': 0,
                            'closing_total': 0
                        }
                    
                    monthly_group_data[key]['count'] += 1
                    monthly_group_data[key]['total_score'] += result.get('Total Score', 0)
                    monthly_group_data[key]['worknotes_total'] += result.get('Worknotes Score', 0)
                    monthly_group_data[key]['closing_total'] += result.get('Closing Comments Score', 0)
                    
            except Exception as e:
                continue
        
        if not monthly_group_data:
            return
        
        # Configure columns
        columns = ('Month', 'Application Group', 'Avg Score', 'Avg Worknotes', 'Avg Closing')
        self.trend_tree['columns'] = columns
        self.trend_tree['show'] = 'headings'
        
        # Set column headings and widths
        self.trend_tree.heading('Month', text='Month')
        self.trend_tree.heading('Application Group', text='Application Group')
        self.trend_tree.heading('Avg Score', text='Avg Score')
        self.trend_tree.heading('Avg Worknotes', text='Avg Worknotes')
        self.trend_tree.heading('Avg Closing', text='Avg Closing')
        
        self.trend_tree.column('Month', width=150, anchor=tk.W)
        self.trend_tree.column('Application Group', width=200, anchor=tk.W)
        self.trend_tree.column('Avg Score', width=120, anchor=tk.CENTER)
        self.trend_tree.column('Avg Worknotes', width=130, anchor=tk.CENTER)
        self.trend_tree.column('Avg Closing', width=130, anchor=tk.CENTER)
        
        # Sort by month and group
        sorted_keys = sorted(monthly_group_data.keys(), key=lambda x: (x[0], x[2]))
        
        # Populate data with color coding
        for key in sorted_keys:
            month_key, month_display, app_group = key
            data = monthly_group_data[key]
            count = data['count']
            
            avg_total = data['total_score'] / count if count > 0 else 0
            avg_worknotes = data['worknotes_total'] / count if count > 0 else 0
            avg_closing = data['closing_total'] / count if count > 0 else 0
            
            # Determine color based on avg score (Good > 74, Average 50-74, Poor < 50)
            if avg_total > 74:
                tag = 'good'
            elif avg_total >= 50:
                tag = 'average'
            else:
                tag = 'poor'
            
            self.trend_tree.insert('', tk.END, values=(
                month_display,
                app_group,
                f"{avg_total:.2f}",
                f"{avg_worknotes:.2f}",
                f"{avg_closing:.2f}"
            ), tags=(tag,))
        
        # Configure tags for color coding
        self.trend_tree.tag_configure('good', background='#d4edda', foreground='#155724')
        self.trend_tree.tag_configure('average', background='#fff3cd', foreground='#856404')
        self.trend_tree.tag_configure('poor', background='#f8d7da', foreground='#721c24')
    
    def export_trend_results(self):
        """Export monthly trend results to Excel"""
        if not self.evaluation_results:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment
            from datetime import datetime
            
            # Get data from tree
            if not self.trend_tree.get_children():
                messagebox.showwarning("Warning", "No trend data to export!")
                return
            
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"Monthly_Trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if not filename:
                return
            
            # Create workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Monthly Trends"
            
            # Write headers
            headers = ['Month', 'Application Group', 'Avg Score', 'Avg Worknotes', 'Avg Closing']
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.font = Font(bold=True, color="FFFFFF")
                cell.alignment = Alignment(horizontal='center')
            
            # Write data
            row_num = 2
            for item in self.trend_tree.get_children():
                values = self.trend_tree.item(item)['values']
                tags = self.trend_tree.item(item)['tags']
                
                for col_num, value in enumerate(values, 1):
                    cell = ws.cell(row=row_num, column=col_num, value=value)
                    
                    # Apply color based on tag
                    if tags:
                        tag = tags[0]
                        if tag == 'good':
                            cell.fill = PatternFill(start_color="d4edda", end_color="d4edda", fill_type="solid")
                        elif tag == 'average':
                            cell.fill = PatternFill(start_color="fff3cd", end_color="fff3cd", fill_type="solid")
                        elif tag == 'poor':
                            cell.fill = PatternFill(start_color="f8d7da", end_color="f8d7da", fill_type="solid")
                
                row_num += 1
            
            # Adjust column widths
            ws.column_dimensions['A'].width = 20
            ws.column_dimensions['B'].width = 30
            ws.column_dimensions['C'].width = 15
            ws.column_dimensions['D'].width = 18
            ws.column_dimensions['E'].width = 18
            
            # Save workbook
            wb.save(filename)
            messagebox.showinfo("Success", f"Monthly trends exported successfully to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    
    def display_rca_analysis(self, event=None):
        """Display RCA analysis for selected incident"""
        selected = self.rca_incident_var.get()
        if not selected or selected == 'Select an incident...':
            return
        
        if not self.df or not self.evaluation_results:
            messagebox.showwarning("Warning", "Please load and evaluate data first!")
            return
        
        cols = self.detect_columns()
        if not cols:
            return
        
        # Find the incident
        incident_col = cols.get('incident')
        incident_idx = None
        
        for idx, row in enumerate(self.df):
            incident_num = self.safe_cell_text(row.get(incident_col, ''))
            if incident_num == selected:
                incident_idx = idx
                break
        
        if incident_idx is None:
            messagebox.showerror("Error", "Incident not found!")
            return
        
        # Get worknotes and closing comments
        worknotes = self.safe_cell_text(self.df[incident_idx].get(cols['worknotes'], ''))
        closing = self.safe_cell_text(self.df[incident_idx].get(cols['closing'], ''))
        
        # Display with highlighting
        self.highlight_keywords_in_text(self.rca_worknotes_text, worknotes, 'worknotes')
        self.highlight_keywords_in_text(self.rca_closing_text, closing, 'closing')
    
    def highlight_keywords_in_text(self, text_widget, content, section_type):
        """Highlight keywords in text widget"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, content)
        
        if not content:
            text_widget.config(state=tk.DISABLED)
            return
        
        content_lower = content.lower()
        
        # Get required keywords for this section
        if section_type == 'worknotes':
            required_kw = self.config['worknotes']['required_keywords']
        else:
            required_kw = self.config['closing_comments']['required_keywords']
        
        # Build a set of all required keyword variations to highlight as required
        required_variations = set()
        phases = self.config.get('phase_keywords', {})
        
        for req_kw in required_kw:
            req_kw_lower = req_kw.lower()
            # Add the required keyword itself
            required_variations.add(req_kw_lower)
            
            # If this required keyword matches a phase name, add all phase keywords as required
            if req_kw_lower in phases:
                for phase_keyword in phases[req_kw_lower]:
                    required_variations.add(phase_keyword.lower())
        
        # Highlight all required keyword variations with 'required' tag
        for keyword in required_kw:
            self.highlight_keyword(text_widget, content, content_lower, keyword, 'required')
        
        # Also highlight phase keywords that match required keywords
        for phase_name, keywords in phases.items():
            if phase_name.lower() in [kw.lower() for kw in required_kw]:
                # This phase is a required keyword, highlight all its variations as required
                for keyword in keywords:
                    self.highlight_keyword(text_widget, content, content_lower, keyword, 'required')
            else:
                # This phase is not required, highlight with phase color
                for keyword in keywords:
                    if keyword.lower() not in required_variations:
                        self.highlight_keyword(text_widget, content, content_lower, keyword, phase_name)
        
        text_widget.config(state=tk.DISABLED)
    
    def highlight_keyword(self, text_widget, content, content_lower, keyword, tag):
        """Highlight a specific keyword in text widget"""
        keyword_lower = keyword.lower()
        start_idx = 0
        
        while True:
            # Find next occurrence
            pos = content_lower.find(keyword_lower, start_idx)
            if pos == -1:
                break
            
            # Check if it's a whole word (not part of another word)
            if pos > 0 and content_lower[pos-1].isalnum():
                start_idx = pos + 1
                continue
            if pos + len(keyword) < len(content) and content_lower[pos + len(keyword)].isalnum():
                start_idx = pos + 1
                continue
            
            # Calculate text widget indices
            start_index = f"1.0 + {pos} chars"
            end_index = f"1.0 + {pos + len(keyword)} chars"
            
            # Apply tag
            text_widget.tag_add(tag, start_index, end_index)
            
            start_idx = pos + len(keyword)
    
    
    def create_dashboard_tab(self):
        """Create dashboard tab with executive summary and group-wise results - Full stretch"""
        # Store reference to dashboard frame for updates
        self.dashboard_content = self.dashboard_frame
        
        # Initial message
        initial_label = ttk.Label(self.dashboard_frame,
                                 text="Load and evaluate data to see the dashboard",
                                 font=('Arial', 14))
        initial_label.pack(pady=50)
    
    def create_group_analysis_tab(self):
        """Create application group analysis tab"""
        self.group_analysis_content = self.group_analysis_frame
        
        initial_label = ttk.Label(self.group_analysis_frame,
                                 text="Load and evaluate data to see application group analysis",
                                 font=('Arial', 14))
        initial_label.pack(pady=50)
    
    def create_individual_tab(self):
        """Create resolver analysis tab"""
        self.individual_content = self.individual_frame
    
    def open_keyword_management(self):
        """Open keyword management window - Display only"""
        # Create new window
        keyword_window = tk.Toplevel(self.root)
        keyword_window.title("Keywords and Phase Keywords - Reference")
        
        # Get screen dimensions and set window to fit
        screen_width = keyword_window.winfo_screenwidth()
        screen_height = keyword_window.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        keyword_window.geometry(f"{window_width}x{window_height}")
        keyword_window.transient(self.root)
        
        # Center the window
        keyword_window.update_idletasks()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        keyword_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Main container with light background
        keyword_window.configure(bg='#f8f9fa')
        main_frame = ttk.Frame(keyword_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with modern styling
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="Keywords and Phase Keywords Reference",
                               font=('Segoe UI', 18, 'bold'),
                               foreground='#2c3e50')
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(title_frame,
                                   text="View all keywords used for incident evaluation",
                                   font=('Segoe UI', 10),
                                   foreground='#7f8c8d')
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Create Treeview without scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview with 2 columns - no scrollbars
        columns = ('Required_Keywords', 'Phase_Keywords')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=14)
        
        # Configure columns with proper widths and left indent
        tree.heading('Required_Keywords', text='  Required Keywords', anchor=tk.W)
        tree.heading('Phase_Keywords', text='  Phase Keywords', anchor=tk.W)
        
        tree.column('Required_Keywords', width=300, anchor=tk.W, stretch=False)
        tree.column('Phase_Keywords', width=int(window_width - 400), anchor=tk.W, stretch=True)
        
        # Pack treeview without scrollbars
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Store tree reference
        self.keyword_tree = tree
        
        # Populate matrix with data
        self.populate_keyword_matrix(tree)
        
        # Close button only
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        close_btn = ttk.Button(button_frame, text="Close",
                              command=keyword_window.destroy)
        close_btn.pack(side=tk.RIGHT)
    
    def populate_keyword_matrix(self, tree):
        """Populate the keyword matrix treeview with cool light professional styling"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Configure style for increased header height
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)  # Default row height
        
        phases = self.config.get('phase_keywords', {})
        
        # WORKNOTES SECTION HEADER - aligned with data (add indent)
        tree.insert('', 'end', values=('  WORKNOTES', ''), tags=('section_header',))
        
        # Worknotes phase keywords - each on separate row
        for idx, phase_name in enumerate(['detection', 'analysis', 'impact', 'log', 'monitoring']):
            if phase_name in phases:
                keywords = phases[phase_name]
                kw_str = ', '.join(keywords)
                tree.insert('', 'end', values=(f'  {phase_name.title()}', kw_str),
                           tags=(f'worknotes_{idx}',))
        
        # Add separator
        tree.insert('', 'end', values=('', ''), tags=('separator',))
        
        # CLOSING COMMENTS SECTION HEADER - aligned with data (add indent)
        tree.insert('', 'end', values=('  CLOSING COMMENTS', ''), tags=('section_header',))
        
        # Closing comments phase keywords - each on separate row
        for idx, phase_name in enumerate(['rootcause', 'resolution', 'verification']):
            if phase_name in phases:
                keywords = phases[phase_name]
                kw_str = ', '.join(keywords)
                tree.insert('', 'end', values=(f'  {phase_name.title()}', kw_str),
                           tags=(f'closing_{idx}',))
        
        # Configure tags with cool light professional styling
        # Reduced font size for section headers, centered vertically
        tree.tag_configure('section_header',
                          background='#4a90e2',  # Cool blue
                          foreground='white',
                          font=('Segoe UI', 12, 'bold'))  # Reduced font size
        tree.tag_configure('separator', background='#f8f9fa')
        
        # Worknotes styling - Cool light pastel colors
        worknotes_colors = [
            '#e3f2fd',  # Light blue
            '#e1f5fe',  # Cyan tint
            '#e0f7fa',  # Light cyan
            '#e0f2f1',  # Teal tint
            '#f1f8e9'   # Light lime
        ]
        
        for idx in range(5):
            tree.tag_configure(f'worknotes_{idx}',
                             background=worknotes_colors[idx],
                             foreground='#2c3e50',  # Dark text for contrast
                             font=('Segoe UI', 11))
        
        # Closing comments styling - Cool light mint/aqua colors
        closing_colors = [
            '#e8f5e9',  # Light green
            '#e0f2f1',  # Light teal
            '#e1f5fe'   # Light cyan
        ]
        
        for idx in range(3):
            tree.tag_configure(f'closing_{idx}',
                             background=closing_colors[idx],
                             foreground='#2c3e50',  # Dark text for contrast
                             font=('Segoe UI', 11))
    
    def add_row_to_matrix(self, tree):
        """Add a new row to the keyword matrix"""
        # Create dialog to get new phase name
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Phase")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Add New Phase Keyword",
                 font=('Segoe UI', 12, 'bold'),
                 foreground=self.colors['primary']).pack(pady=(0, 15))
        
        # Section selection
        ttk.Label(frame, text="Select Section:", font=('Segoe UI', 9)).pack(anchor=tk.W, pady=(0, 5))
        section_var = tk.StringVar(value='worknotes')
        ttk.Radiobutton(frame, text="Worknotes", variable=section_var, value='worknotes').pack(anchor=tk.W)
        ttk.Radiobutton(frame, text="Closing Comments", variable=section_var, value='closing').pack(anchor=tk.W)
        
        # Phase name
        ttk.Label(frame, text="Phase Name:", font=('Segoe UI', 9)).pack(anchor=tk.W, pady=(10, 5))
        phase_entry = ttk.Entry(frame, width=40)
        phase_entry.pack(pady=5)
        phase_entry.focus()
        
        # Keywords
        ttk.Label(frame, text="Keywords (comma-separated):", font=('Segoe UI', 9)).pack(anchor=tk.W, pady=(10, 5))
        keywords_entry = ttk.Entry(frame, width=40)
        keywords_entry.pack(pady=5)
        
        def add():
            phase_name = phase_entry.get().strip().lower()
            keywords_str = keywords_entry.get().strip()
            
            if not phase_name:
                messagebox.showwarning("Warning", "Please enter a phase name!")
                return
            
            # Add to config
            keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
            self.config['phase_keywords'][phase_name] = keywords
            
            # Refresh tree
            self.populate_keyword_matrix(tree)
            dialog.destroy()
            messagebox.showinfo("Success", f"Phase '{phase_name}' added! Click 'Save All Changes' to persist.")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(15, 0))
        ttk.Button(btn_frame, text="Add", command=add, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
        phase_entry.bind('<Return>', lambda e: keywords_entry.focus())
        keywords_entry.bind('<Return>', lambda e: add())
    
    def delete_row_from_matrix(self, tree):
        """Delete selected row from the keyword matrix"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a row to delete!")
            return
        
        item = selection[0]
        values = tree.item(item, 'values')
        row_name = values[0].strip()
        
        # Skip section headers and separators
        if not row_name or row_name in ['WORKNOTES', 'CLOSING COMMENTS', '']:
            messagebox.showwarning("Warning", "Cannot delete section headers!")
            return
        
        # Confirm deletion
        phase_name = row_name.strip().lower()
        if messagebox.askyesno("Confirm Delete", f"Delete phase '{row_name}'?\n\nThis will remove it from the configuration."):
            # Remove from config
            if phase_name in self.config.get('phase_keywords', {}):
                del self.config['phase_keywords'][phase_name]
            
            # Remove from required keywords if present
            if phase_name in self.config.get('worknotes', {}).get('required_keywords', []):
                self.config['worknotes']['required_keywords'].remove(phase_name)
            if phase_name in self.config.get('closing_comments', {}).get('required_keywords', []):
                self.config['closing_comments']['required_keywords'].remove(phase_name)
            
            # Refresh tree
            self.populate_keyword_matrix(tree)
            messagebox.showinfo("Success", f"Phase '{row_name}' deleted! Click 'Save All Changes' to persist.")
    
    def edit_keyword_in_matrix(self, tree):
        """Edit keywords for selected row"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a row to edit!")
            return
        
        item = selection[0]
        values = tree.item(item, 'values')
        row_name = values[0].strip()
        current_phase_keywords = values[1]
        
        # Skip section headers and separators
        if not row_name or row_name in ['WORKNOTES', 'CLOSING COMMENTS', '']:
            messagebox.showwarning("Warning", "Please select a keyword row, not a header!")
            return
        
        # Edit phase keywords
        if not current_phase_keywords:
            messagebox.showwarning("Warning", "No phase keywords to edit in this row!")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Phase Keywords - {row_name}")
        dialog.geometry("800x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(frame, text=f"Edit Phase Keywords: {row_name}",
                 font=('Segoe UI', 12, 'bold'),
                 foreground=self.colors['primary']).pack(pady=(0, 15))
        
        # Instructions
        ttk.Label(frame, text="Enter keywords separated by commas:",
                 font=('Segoe UI', 9)).pack(anchor=tk.W, pady=(0, 5))
        
        # Text editor
        text_widget = scrolledtext.ScrolledText(frame, width=85, height=14,
                                               wrap=tk.WORD, font=('Consolas', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, pady=5)
        text_widget.insert(1.0, current_phase_keywords)
        text_widget.focus()
        
        def save():
            new_keywords = text_widget.get(1.0, tk.END).strip()
            tree.item(item, values=(row_name, new_keywords))
            dialog.destroy()
            messagebox.showinfo("Success", "Keywords updated! Click 'Save All Changes' to persist to config.json.")
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(15, 0))
        ttk.Button(btn_frame, text="💾 Save", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancel", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def save_matrix_keywords(self, window):
        """Save all keywords from matrix back to config"""
        try:
            tree = self.keyword_tree
            
            # Track current section
            current_section = None
            
            # Iterate through tree items and update config
            for item in tree.get_children():
                values = tree.item(item, 'values')
                row_name = values[0].strip()
                phase_keywords_str = values[1]
                
                # Track current section
                if row_name == 'WORKNOTES':
                    current_section = 'worknotes'
                    continue
                elif row_name == 'CLOSING COMMENTS':
                    current_section = 'closing'
                    continue
                elif row_name == '':
                    current_section = None
                    continue
                
                # Extract phase name from row (remove leading spaces)
                phase_name = row_name.strip().lower()
                
                # Update phase keywords
                if phase_keywords_str:
                    keywords = [kw.strip() for kw in phase_keywords_str.split(',') if kw.strip()]
                    if phase_name not in self.config.get('phase_keywords', {}):
                        # New phase, add it
                        self.config['phase_keywords'][phase_name] = keywords
                    else:
                        # Existing phase, update it
                        self.config['phase_keywords'][phase_name] = keywords
            
            # Save to config.json file
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            messagebox.showinfo("Success", "All keywords saved successfully to config.json!")
            self.status_var.set("Keywords saved to config.json")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save keywords: {str(e)}")
            self.status_var.set("Error saving keywords")
    
    def load_excel(self):
        """Load Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.file_path_var.set(file_path)
                self.df = self.read_excel_data(file_path)
                self.status_var.set(f"Loaded {len(self.df)} records from {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Loaded {len(self.df)} records successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                self.status_var.set("Error loading file")
    
    def evaluate_incidents(self):
        """Evaluate incidents based on parameters"""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load an Excel file first!")
            return
        
        # Check for required columns
        required_cols = self.detect_columns()
        if not required_cols:
            messagebox.showerror("Error", "Could not detect required columns (Worknotes/Closing Comments)")
            return
        
        try:
            self.status_var.set("Evaluating incidents...")
            self.root.update()
            
            # Perform evaluation
            results = []
            for row in self.df:
                result = self.evaluate_row(row, required_cols)
                results.append(result)
            
            self.evaluation_results = results
            self.display_results()
            self.update_dashboard()
            self.update_group_analysis()
            self.update_individual_dashboard()
            self.update_rca_dropdown()
            self.update_trend_analysis()
            
            self.status_var.set(f"Evaluation complete! Processed {len(results)} records")
            
        except Exception as e:
            messagebox.showerror("Error", f"Evaluation failed: {str(e)}")
            self.status_var.set("Evaluation failed")
    
    def detect_columns(self):
        """Detect worknotes and closing comments columns"""
        if not self.df:
            return None
        
        worknotes_col = None
        closing_col = None
        incident_col = None
        app_group_col = None
        
        # Detect worknotes column
        for col in self.df[0].keys():
            if any(keyword in col.lower() for keyword in ['worknote', 'work note', 'notes', 'comments']):
                if 'closing' not in col.lower() and 'close' not in col.lower():
                    worknotes_col = col
                    break
        
        # Detect closing comments column
        for col in self.df[0].keys():
            if any(keyword in col.lower() for keyword in ['closing', 'close comment', 'resolution']):
                closing_col = col
                break
        
        # Detect incident ID column
        for col in self.df[0].keys():
            if any(keyword in col.lower() for keyword in ['incident', 'id', 'number', 'ticket']):
                incident_col = col
                break
        
        # Detect application group column
        for col in self.df[0].keys():
            if any(keyword in col.lower() for keyword in ['application', 'app', 'group', 'assignment', 'team', 'category']):
                app_group_col = col
                break
        
        resolved_by_col = None
        for col in self.df[0].keys():
            if 'resolved by' in col.lower():
                resolved_by_col = col
                break
        
        if not worknotes_col and not closing_col:
            return None
        
        return {
            'incident': incident_col or list(self.df[0].keys())[0],
            'worknotes': worknotes_col,
            'closing': closing_col,
            'app_group': app_group_col,
            'resolved_by': resolved_by_col
        }
    
    def get_application_groups(self):
        """Extract unique application groups from data"""
        if not self.df:
            return []
        
        cols = self.detect_columns()
        if not cols or not cols.get('app_group'):
            return ['Ungrouped']
        
        app_col = cols['app_group']
        groups = set()
        for row in self.df:
            group = self.safe_cell_text(row.get(app_col, 'Ungrouped'))
            if group and group.strip():
                groups.add(group.strip())
            else:
                groups.add('Ungrouped')
        
        return sorted(list(groups))
    
    def group_results_by_application(self):
        """Group evaluation results by application"""
        if not self.evaluation_results or not self.df:
            return {}
        
        cols = self.detect_columns()
        app_col = cols.get('app_group') if cols else None
        
        grouped = {}
        for idx, result in enumerate(self.evaluation_results):
            if idx < len(self.df):
                if app_col:
                    group = self.safe_cell_text(self.df[idx].get(app_col, 'Ungrouped'))
                    group = group.strip() if group.strip() else 'Ungrouped'
                else:
                    group = 'Ungrouped'
                
                if group not in grouped:
                    grouped[group] = []
                grouped[group].append(result)
        
        return grouped
    
    def group_results_by_individual(self):
        """Group evaluation results by resolved by individual"""
        if not self.evaluation_results or not self.df:
            return {}
        
        cols = self.detect_columns()
        individual_col = cols.get('resolved_by') if cols else None
        
        grouped = {}
        for idx, result in enumerate(self.evaluation_results):
            if idx < len(self.df):
                if individual_col:
                    person = self.safe_cell_text(self.df[idx].get(individual_col, 'Unassigned'))
                    person = person.strip() if person.strip() else 'Unassigned'
                else:
                    person = 'Unassigned'
                
                if person not in grouped:
                    grouped[person] = []
                grouped[person].append(result)
        
        return grouped
    
    def evaluate_row(self, row, cols):
        """Evaluate a single incident row"""
        incident_id = row.get(cols['incident'], 'N/A') if cols['incident'] else 'N/A'
        input_number = self.safe_cell_text(row.get('Number', ''))
        
        # Get application group
        app_group = 'Ungrouped'
        if cols.get('app_group'):
            app_group = self.safe_cell_text(row.get(cols['app_group'], 'Ungrouped'))
            app_group = app_group.strip() if app_group.strip() else 'Ungrouped'
        
        # Evaluate worknotes
        worknotes_score = 0
        worknotes_issues = []
        if cols['worknotes']:
            worknotes = self.safe_cell_text(row.get(cols['worknotes']))
            worknotes_score, worknotes_issues = self.evaluate_text(
                worknotes, 
                self.config['worknotes']
            )
        
        # Evaluate closing comments
        closing_score = 0
        closing_issues = []
        if cols['closing']:
            closing = self.safe_cell_text(row.get(cols['closing']))
            closing_score, closing_issues = self.evaluate_text(
                closing,
                self.config['closing_comments']
            )
        
        # Calculate overall score as average of worknotes and closing comments scores
        overall_score = (worknotes_score + closing_score) / 2 if cols['worknotes'] and cols['closing'] else max(worknotes_score, closing_score)
        
        # Determine overall rating based on average of worknotes and closing comments scores
        if overall_score > 74:
            overall_rating = "Good"
        elif overall_score >= 50 and overall_score < 75:
            overall_rating = "Average"
        else:
            overall_rating = "Poor"
        
        # Determine individual ratings
        if worknotes_score > 74:
            worknotes_rating = "Good"
        elif worknotes_score >= 50 and worknotes_score < 75:
            worknotes_rating = "Average"
        else:
            worknotes_rating = "Poor"
            
        if closing_score > 74:
            closing_rating = "Good"
        elif closing_score >= 50 and closing_score < 75:
            closing_rating = "Average"
        else:
            closing_rating = "Poor"
        
        return {
            'Number': input_number,
            'Group': app_group,
            'Resolved by': self.safe_cell_text(row.get('Resolved by', '')),
            'Resolved': self.safe_cell_text(row.get('Resolved', '')),
            'Worknotes Score': round(worknotes_score, 2),
            'Worknotes Rating': worknotes_rating,
            'Closing Comments Score': round(closing_score, 2),
            'Closing Comments Rating': closing_rating,
            'Total Score': round(overall_score, 2),
            'Total Rating': overall_rating,
            'Worknotes Issues': '; '.join(worknotes_issues) if worknotes_issues else 'None',
            'Closing Comments Issues': '; '.join(closing_issues) if closing_issues else 'None'
        }
    
    def evaluate_text(self, text, criteria):
        """Evaluate text based on criteria - using only keyword scoring with synonyms"""
        score = 0
        issues = []
        text_lower = text.lower()
        
        # Get phase keywords (synonyms) from config
        phase_keywords = self.config.get('phase_keywords', {})
        
        # Required keywords check - check for keyword or its synonyms
        found_required = 0
        missing_keywords = []
        
        for kw in criteria['required_keywords']:
            # Normalize keyword for lookup (remove spaces, convert to lowercase)
            kw_normalized = kw.lower().replace(' ', '_')
            
            # Get synonyms for this keyword
            synonyms = phase_keywords.get(kw_normalized, [kw.lower()])
            
            # Check if any synonym is found in text
            if any(syn.lower() in text_lower for syn in synonyms):
                found_required += 1
            else:
                missing_keywords.append(kw)
        
        keyword_score = (found_required / len(criteria['required_keywords'])) * 100
        
        if found_required == 0:
            issues.append("No required keywords found")
        elif found_required < len(criteria['required_keywords']) / 2:
            issues.append(f"Only {found_required}/{len(criteria['required_keywords'])} required keywords found")
        
        # Apply 100% weight to keyword score
        score = keyword_score * self.config['scoring']['keywords_weight']
        
        return score, issues
    
    def display_results(self, selected_group=None):
        """Display evaluation results with optional application group filter"""
        # Clear existing data
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Configure columns
        if not self.evaluation_results:
            return
        
        # Populate filter dropdown with application groups
        cols = self.detect_columns()
        app_group_col = cols.get('app_group') if cols else None
        all_groups = set()
        
        if cols and self.df and app_group_col:
            for row in self.df:
                row_group = self.safe_cell_text(row.get(app_group_col, 'Ungrouped'))
                row_group = row_group.strip() if row_group.strip() else 'Ungrouped'
                all_groups.add(row_group)
        
        # Update dropdown options
        group_options = ['All'] + sorted(all_groups)
        self.results_filter_dropdown['values'] = group_options
        if not selected_group:
            self.results_filter_var.set('All')
        
        ordered_result_columns = [
            'Number',
            'Group',
            'Resolved by',
            'Resolved',
            'Worknotes Score',
            'Worknotes Rating',
            'Closing Comments Score',
            'Closing Comments Rating',
            'Total Score',
            'Total Rating',
            'Worknotes Issues',
            'Closing Comments Issues'
        ]
        columns = ['S.No.'] + ordered_result_columns
        self.results_tree['columns'] = columns
        self.results_tree['show'] = 'headings'
        
        # Add sorting functionality and alignment to headers
        column_widths = {
            'S.No.': 45,
            'Number': 90,
            'Group': 150,
            'Resolved by': 130,
            'Resolved': 110,
            'Worknotes Score': 100,
            'Worknotes Rating': 105,
            'Closing Comments Score': 125,
            'Closing Comments Rating': 135,
            'Total Score': 90,
            'Total Rating': 95,
            'Worknotes Issues': 220,
            'Closing Comments Issues': 220
        }

        for col in columns:
            if col in ('Group', 'Worknotes Issues', 'Closing Comments Issues'):
                anchor = tk.W
            else:
                anchor = tk.CENTER
            
            # Set heading with same anchor as data
            self.results_tree.heading(col, text=col, anchor=anchor,
                                     command=lambda c=col: self.sort_results_by_column(c, False))
            self.results_tree.column(col, width=column_widths.get(col, 100), minwidth=70, anchor=anchor, stretch=True)
        
        # Get the selected filter
        filter_group = selected_group if selected_group and selected_group != 'All' else None
        
        # Insert data with color coding and filtering
        row_num = 1
        for row in self.evaluation_results:
            # Apply filter if set
            if filter_group:
                row_group = row.get('Group', 'Ungrouped')
                if row_group != filter_group:
                    continue
            
            values = [str(row_num)] + [row.get(col, "") for col in ordered_result_columns]
            item = self.results_tree.insert('', tk.END, values=values)
            
            # Color code based on total rating
            if row['Total Rating'] == 'Good':
                self.results_tree.item(item, tags=('good',))
            elif row['Total Rating'] == 'Average':
                self.results_tree.item(item, tags=('average',))
            else:
                self.results_tree.item(item, tags=('poor',))
            
            row_num += 1
        
        # Configure tags with professional colors
        self.results_tree.tag_configure('good', background='#A8E6CF')      # Mint Green
        self.results_tree.tag_configure('average', background='#B3D9FF')   # Sky Blue
        self.results_tree.tag_configure('poor', background='#FFE5B4')      # Peach
    
    def sort_tree_by_column(self, tree, col, reverse):
        """Generic method to sort any treeview by column"""
        # Get all data from treeview
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        
        # Sort data
        try:
            # Try to sort numerically if possible
            data.sort(key=lambda t: float(t[0]) if t[0] and t[0] != '' else 0, reverse=reverse)
        except (ValueError, TypeError):
            # Fall back to string sorting
            data.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        
        # Update heading to toggle sort direction on next click
        tree.heading(col, command=lambda: self.sort_tree_by_column(tree, col, not reverse))
    
    def sort_results_by_column(self, col, reverse):
        """Sort results treeview by column"""
        self.sort_tree_by_column(self.results_tree, col, reverse)
    
    
    
    def update_dashboard(self):
        """Update dashboard with executive summary and group-wise results"""
        # Clear existing content
        for widget in self.dashboard_content.winfo_children():
            widget.destroy()
        
        if not self.evaluation_results:
            ttk.Label(self.dashboard_content,
                     text="No evaluation data available",
                     font=('Arial', 14)).pack(pady=50)
            return
        
        # Date Range Header - Show data period with professional spacing
        date_range_frame = ttk.Frame(self.dashboard_content)
        date_range_frame.pack(fill=tk.X, padx=10, pady=(15, 0))
        
        # Create a container for left (records/date) and right (criteria) sections
        header_container = ttk.Frame(date_range_frame)
        header_container.pack(fill=tk.X, padx=5)
        
        # Left side: Total records and date range
        left_frame = ttk.Frame(header_container)
        left_frame.pack(side=tk.LEFT, anchor=tk.W)
        
        # Display total records loaded
        ttk.Label(left_frame, text=f"📊 Total Records Loaded: {len(self.df)}",
                 font=('Arial', 10, 'bold'), foreground='#2C3E50').pack(anchor=tk.W, pady=(0, 5))
        
        # Try to detect and display date range from Resolved field specifically (not Resolved by)
        resolved_col = None
        for col in self.df[0].keys():
            # Look for exact "Resolved" field, not "Resolved by"
            if col.lower() == 'resolved':
                resolved_col = col
                break
        
        if resolved_col:
            try:
                from datetime import datetime
                import re
                dates = []
                for row in self.df:
                    date_val = row.get(resolved_col, '')
                    if date_val:
                        try:
                            # Try to parse the date
                            date_str = str(date_val).strip()
                            if date_str and date_str.lower() not in ['', 'none', 'null', 'n/a']:
                                # Extract just the date part if there's a time component
                                date_part = date_str.split()[0] if ' ' in date_str else date_str
                                
                                # Try common date formats
                                formats = [
                                    '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%Y/%m/%d',
                                    '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S',
                                    '%d-%b-%Y', '%d-%B-%Y', '%b %d, %Y', '%B %d, %Y',
                                    '%Y%m%d', '%d.%m.%Y'
                                ]
                                
                                for fmt in formats:
                                    try:
                                        parsed_date = datetime.strptime(date_str if '%H:%M:%S' in fmt else date_part, fmt)
                                        dates.append(parsed_date)
                                        break
                                    except ValueError:
                                        continue
                        except Exception as e:
                            continue
                
                if dates:
                    oldest_date = min(dates).strftime('%d-%b-%Y')
                    newest_date = max(dates).strftime('%d-%b-%Y')
                    ttk.Label(left_frame, text=f"📅 Date Range: {oldest_date} - {newest_date}",
                             font=('Arial', 10, 'bold'), foreground='#2C3E50').pack(anchor=tk.W, pady=(0, 5))
                else:
                    # If no dates could be parsed, show a message
                    ttk.Label(left_frame, text=f"📅 Date Range: Unable to parse dates from '{resolved_col}' field",
                             font=('Arial', 10, 'bold'), foreground='#999').pack(anchor=tk.W, pady=(0, 5))
            except Exception as e:
                # Show error for debugging
                ttk.Label(left_frame, text=f"📅 Date Range: Error reading dates - {str(e)[:50]}",
                         font=('Arial', 10, 'bold'), foreground='#999').pack(anchor=tk.W, pady=(0, 5))
        else:
            # No resolved column found
            ttk.Label(left_frame, text=f"📅 Date Range: No 'Resolved' field found in data",
                     font=('Arial', 10, 'bold'), foreground='#999').pack(anchor=tk.W, pady=(0, 5))
        
        # Right side: Evaluation Criteria
        right_frame = ttk.Frame(header_container)
        right_frame.pack(side=tk.RIGHT, anchor=tk.E)
        
        # Get evaluation criteria from config
        criteria = self.config.get('evaluation_criteria', {})
        good_threshold = criteria.get('good_threshold', 74)
        average_threshold = criteria.get('average_threshold', 50)
        
        # Display evaluation criteria with bold highlighting in 2 rows
        ttk.Label(right_frame, text="📋 Evaluation Criteria:",
                 font=('Arial', 10, 'bold'), foreground='#2C3E50').pack(anchor=tk.E)
        
        # Create a frame for color-coded criteria
        criteria_frame = ttk.Frame(right_frame)
        criteria_frame.pack(anchor=tk.E, pady=(2, 5))
        
        # Good criteria in green
        ttk.Label(criteria_frame, text=f"Good: >{good_threshold}%",
                 font=('Arial', 10, 'bold'), foreground='#27AE60').pack(side=tk.LEFT)
        ttk.Label(criteria_frame, text="  |  ",
                 font=('Arial', 10, 'bold'), foreground='#2C3E50').pack(side=tk.LEFT)
        
        # Average criteria in blue
        ttk.Label(criteria_frame, text=f"Average: {average_threshold}-{good_threshold}%",
                 font=('Arial', 10, 'bold'), foreground='#3498DB').pack(side=tk.LEFT)
        ttk.Label(criteria_frame, text="  |  ",
                 font=('Arial', 10, 'bold'), foreground='#2C3E50').pack(side=tk.LEFT)
        
        # Poor criteria in orange
        ttk.Label(criteria_frame, text=f"Poor: <{average_threshold}%",
                 font=('Arial', 10, 'bold'), foreground='#E67E22').pack(side=tk.LEFT)
        
        # Executive Summary Section - Compact for window fit
        summary_frame = ttk.LabelFrame(self.dashboard_content, text="📊 Executive Summary",
                                       padding=5, relief=tk.RIDGE, borderwidth=2)
        summary_frame.pack(fill=tk.X, padx=10, pady=(5, 3))
        
        # Key metrics in a grid
        metrics_frame = ttk.Frame(summary_frame)
        metrics_frame.pack(fill=tk.X)
        
        # Configure all columns to have equal weight for uniform width
        for i in range(5):
            metrics_frame.columnconfigure(i, weight=1, uniform="dashboard_cols")
        
        total_incidents = len(self.evaluation_results)
        worknotes_avg = self.calculate_average('Worknotes Score')
        closing_avg = self.calculate_average('Closing Comments Score')
        
        # Calculate blank records count first
        cols = self.detect_columns()
        worknotes_blank = 0
        closing_blank = 0
        
        if cols and self.df:
            for row in self.df:
                # Check worknotes blank
                if cols.get('worknotes'):
                    worknotes_text = self.safe_cell_text(row.get(cols['worknotes'], ''))
                    if not worknotes_text or worknotes_text.strip() == '':
                        worknotes_blank += 1
                
                # Check closing comments blank
                if cols.get('closing'):
                    closing_text = self.safe_cell_text(row.get(cols['closing'], ''))
                    if not closing_text or closing_text.strip() == '':
                        closing_blank += 1
        
        # Calculate quality counts for worknotes (excluding blanks from poor)
        worknotes_good = sum(1 for row in self.evaluation_results if row['Worknotes Score'] > 74)
        worknotes_average = sum(1 for row in self.evaluation_results if 50 <= row['Worknotes Score'] < 75)
        worknotes_poor_total = sum(1 for row in self.evaluation_results if row['Worknotes Score'] < 50)
        worknotes_poor = max(0, worknotes_poor_total - worknotes_blank)  # Exclude blanks from poor, ensure non-negative
        
        # Calculate quality counts for closing comments (excluding blanks from poor)
        closing_good = sum(1 for row in self.evaluation_results if row['Closing Comments Score'] > 74)
        closing_average = sum(1 for row in self.evaluation_results if 50 <= row['Closing Comments Score'] < 75)
        closing_poor_total = sum(1 for row in self.evaluation_results if row['Closing Comments Score'] < 50)
        closing_poor = max(0, closing_poor_total - closing_blank)  # Exclude blanks from poor, ensure non-negative
        
        # Calculate overall quality counts
        quality_counts = Counter(row['Total Rating'] for row in self.evaluation_results)
        
        # Row 0: Work Notes metrics
        self.create_metric_card(metrics_frame, "Worknotes Avg", f"{worknotes_avg:.1f}%",
                               "📊", 0, 0, "#5DADE2", font_size=11)
        self.create_metric_card(metrics_frame, "Good", str(worknotes_good),
                               "✅", 0, 1, "#52BE80")
        self.create_metric_card(metrics_frame, "Average", str(worknotes_average),
                               "📈", 0, 2, "#5DADE2")
        self.create_metric_card(metrics_frame, "Poor", str(worknotes_poor),
                               "⚠️", 0, 3, "#F39C12")
        self.create_metric_card(metrics_frame, "Blank", str(worknotes_blank),
                               "📄", 0, 4, "#FF6B6B")  # Coral Red - More visible
        
        # Row 1: Closing Comments metrics
        self.create_metric_card(metrics_frame, "Closing Comments Avg", f"{closing_avg:.1f}%",
                               "📊", 1, 0, "#AF7AC5", font_size=11)
        self.create_metric_card(metrics_frame, "Good", str(closing_good),
                               "✅", 1, 1, "#52BE80")
        self.create_metric_card(metrics_frame, "Average", str(closing_average),
                               "📈", 1, 2, "#5DADE2")
        self.create_metric_card(metrics_frame, "Poor", str(closing_poor),
                               "⚠️", 1, 3, "#F39C12")
        self.create_metric_card(metrics_frame, "Blank", str(closing_blank),
                               "📄", 1, 4, "#FF6B6B")  # Coral Red - More visible
        
        # Application Group Executive Summary Section - Compact for window fit
        grouped_results = self.group_results_by_application()
        if grouped_results:
            group_summary_frame = ttk.LabelFrame(self.dashboard_content, text="📱 Application Group Summary",
                                                 padding=5, relief=tk.RIDGE, borderwidth=2)
            group_summary_frame.pack(fill=tk.X, padx=10, pady=(3, 5))
            
            # Calculate aggregate metrics across all groups
            total_groups = len(grouped_results)
            
            # Calculate group quality distribution based on Worknotes average
            worknotes_good_groups = 0
            worknotes_average_groups = 0
            worknotes_poor_groups = 0
            worknotes_blank_groups = 0
            
            # Calculate group quality distribution based on Closing Comments average
            closing_good_groups = 0
            closing_average_groups = 0
            closing_poor_groups = 0
            closing_blank_groups = 0
            
            for group_name, group_data in grouped_results.items():
                group_count = len(group_data)
                
                # Check if this group has any blank worknotes
                group_has_blank_worknotes = False
                group_has_blank_closing = False
                
                if cols and self.df:
                    app_col = cols.get('app_group')
                    for row in self.df:
                        # Check if this row belongs to current group
                        if app_col:
                            row_group = self.safe_cell_text(row.get(app_col, 'Ungrouped'))
                            row_group = row_group.strip() if row_group.strip() else 'Ungrouped'
                        else:
                            row_group = 'Ungrouped'
                        
                        if row_group == group_name:
                            # Check worknotes blank
                            if cols.get('worknotes'):
                                worknotes_text = self.safe_cell_text(row.get(cols['worknotes'], ''))
                                if not worknotes_text or worknotes_text.strip() == '':
                                    group_has_blank_worknotes = True
                            
                            # Check closing comments blank
                            if cols.get('closing'):
                                closing_text = self.safe_cell_text(row.get(cols['closing'], ''))
                                if not closing_text or closing_text.strip() == '':
                                    group_has_blank_closing = True
                
                # Calculate worknotes average for this group
                group_worknotes_avg = sum(r['Worknotes Score'] for r in group_data) / group_count
                if group_worknotes_avg > 74:
                    worknotes_good_groups += 1
                elif group_worknotes_avg >= 50:
                    worknotes_average_groups += 1
                else:
                    worknotes_poor_groups += 1
                
                if group_has_blank_worknotes:
                    worknotes_blank_groups += 1
                
                # Calculate closing comments average for this group
                group_closing_avg = sum(r['Closing Comments Score'] for r in group_data) / group_count
                if group_closing_avg > 74:
                    closing_good_groups += 1
                elif group_closing_avg >= 50:
                    closing_average_groups += 1
                else:
                    closing_poor_groups += 1
                
                if group_has_blank_closing:
                    closing_blank_groups += 1
            
            # Create metrics grid for application groups - mirroring Executive Summary layout
            group_metrics_frame = ttk.Frame(group_summary_frame)
            group_metrics_frame.pack(fill=tk.X)
            
            # Configure all columns to have equal weight for uniform width (same as Executive Summary)
            for i in range(5):
                group_metrics_frame.columnconfigure(i, weight=1, uniform="dashboard_cols")
            
            # Row 0: Worknotes Total - Total Groups with quality breakdown
            self.create_metric_card(group_metrics_frame, "Worknotes Total", str(total_groups),
                                   "📝", 0, 0, "#5DADE2", font_size=11)
            self.create_metric_card(group_metrics_frame, "Good", str(worknotes_good_groups),
                                   "✅", 0, 1, "#52BE80")
            self.create_metric_card(group_metrics_frame, "Average", str(worknotes_average_groups),
                                   "📈", 0, 2, "#5DADE2")
            # Subtract blank from poor for worknotes
            worknotes_poor_adjusted = max(0, worknotes_poor_groups - worknotes_blank_groups)
            self.create_metric_card(group_metrics_frame, "Poor", str(worknotes_poor_adjusted),
                                   "⚠️", 0, 3, "#F39C12")
            self.create_metric_card(group_metrics_frame, "Blank", str(worknotes_blank_groups),
                                   "📄", 0, 4, "#FF6B6B")
            
            # Row 1: Closing Comments Total - Total Groups with quality breakdown
            self.create_metric_card(group_metrics_frame, "Closing Comments Total", str(total_groups),
                                   "💬", 1, 0, "#AF7AC5", font_size=11)
            self.create_metric_card(group_metrics_frame, "Good", str(closing_good_groups),
                                   "✅", 1, 1, "#52BE80")
            self.create_metric_card(group_metrics_frame, "Average", str(closing_average_groups),
                                   "📈", 1, 2, "#5DADE2")
            # Subtract blank from poor for closing comments
            closing_poor_adjusted = max(0, closing_poor_groups - closing_blank_groups)
            self.create_metric_card(group_metrics_frame, "Poor", str(closing_poor_adjusted),
                                   "⚠️", 1, 3, "#F39C12")
            self.create_metric_card(group_metrics_frame, "Blank", str(closing_blank_groups),
                                   "📄", 1, 4, "#FF6B6B")
        
    def update_group_analysis(self):
        """Update application group analysis in its own tab"""
        # Clear existing content
        for widget in self.group_analysis_content.winfo_children():
            widget.destroy()
        
        if not self.evaluation_results:
            ttk.Label(self.group_analysis_content,
                     text="No evaluation data available",
                     font=('Arial', 14)).pack(pady=50)
            return
        
        # Application Group-wise Results
        grouped_results = self.group_results_by_application()
        
        if grouped_results:
            # Create treeview for group summary - directly without label frame
            actions_frame = ttk.Frame(self.group_analysis_content)
            actions_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
            ttk.Button(actions_frame, text="Export Application Group Analysis", command=self.export_group_analysis).pack(side=tk.RIGHT)
            
            tree_frame = ttk.Frame(self.group_analysis_content)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            columns = ('S.No.', 'Group', 'Count', 'Worknotes Avg', 'Closing Avg', 'Total Avg', 'Good', 'Average', 'Poor', 'Blank Worknotes')
            group_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
            self.group_analysis_tree = group_tree
            
            group_column_widths = {
                'S.No.': 40,
                'Group': 150,
                'Count': 65,
                'Worknotes Avg': 90,
                'Closing Avg': 85,
                'Total Avg': 80,
                'Good': 55,
                'Average': 65,
                'Poor': 55,
                'Blank Worknotes': 95
            }

            # Add sorting functionality to headers with consistent alignment
            for col in columns:
                if col == 'Group':
                    anchor = tk.W
                else:
                    anchor = tk.CENTER
                
                # Set heading with same anchor as data
                group_tree.heading(col, text=col, anchor=anchor,
                                  command=lambda c=col, t=group_tree: self.sort_tree_by_column(t, c, False))
                group_tree.column(col, width=group_column_widths.get(col, 80), minwidth=50, anchor=anchor, stretch=True)
            
            vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=group_tree.yview)
            group_tree.configure(yscrollcommand=vsb.set)
            
            group_tree.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            
            # Get column info for blank detection
            cols = self.detect_columns()
            
            # Populate group data
            for idx, group_name in enumerate(sorted(grouped_results.keys()), start=1):
                group_data = grouped_results[group_name]
                group_count = len(group_data)
                group_worknotes_avg = sum(r['Worknotes Score'] for r in group_data) / group_count
                group_closing_avg = sum(r['Closing Comments Score'] for r in group_data) / group_count
                group_quality = Counter(r['Total Rating'] for r in group_data)
                
                # Calculate blank records for this group
                group_blank = 0
                if cols and self.df:
                    app_col = cols.get('app_group')
                    for df_idx, row in enumerate(self.df):
                        # Check if this row belongs to current group
                        if app_col:
                            row_group = self.safe_cell_text(row.get(app_col, 'Ungrouped'))
                            row_group = row_group.strip() if row_group.strip() else 'Ungrouped'
                        else:
                            row_group = 'Ungrouped'
                        
                        if row_group == group_name:
                            # Check if worknotes or closing comments are blank
                            worknotes_blank = False
                            closing_blank = False
                            
                            if cols.get('worknotes'):
                                worknotes_text = self.safe_cell_text(row.get(cols['worknotes'], ''))
                                if not worknotes_text or worknotes_text.strip() == '':
                                    worknotes_blank = True
                            
                            if cols.get('closing'):
                                closing_text = self.safe_cell_text(row.get(cols['closing'], ''))
                                if not closing_text or closing_text.strip() == '':
                                    closing_blank = True
                            
                            if worknotes_blank or closing_blank:
                                group_blank += 1
                
                group_total_avg = (group_worknotes_avg + group_closing_avg) / 2
                values = (
                    idx,
                    group_name,
                    group_count,
                    f"{group_worknotes_avg:.1f}",
                    f"{group_closing_avg:.1f}",
                    f"{group_total_avg:.1f}",
                    group_quality.get('Good', 0),
                    group_quality.get('Average', 0),
                    group_quality.get('Poor', 0),
                    group_blank
                )
                
                item = group_tree.insert('', tk.END, values=values)
                
                # Color code based on average score
                group_avg = (group_worknotes_avg + group_closing_avg) / 2
                if group_avg > 74:
                    group_tree.item(item, tags=('good',))
                elif group_avg >= 54:
                    group_tree.item(item, tags=('average',))
                else:
                    group_tree.item(item, tags=('poor',))
            
            # Configure tags with professional colors
            group_tree.tag_configure('good', background='#A8E6CF')      # Mint Green
            group_tree.tag_configure('average', background='#B3D9FF')   # Sky Blue
            group_tree.tag_configure('poor', background='#FFE5B4')      # Peach
        else:
            self.group_analysis_tree = None
            ttk.Label(self.group_analysis_content,
                     text="No application group data available",
                     font=('Arial', 12)).pack(pady=20)
    
    
    def update_individual_dashboard(self, selected_group=None):
        """Update resolver analysis in its own tab with optional application group filter"""
        for widget in self.individual_content.winfo_children():
            widget.destroy()
        
        if not self.evaluation_results:
            ttk.Label(self.individual_content,
                     text="No evaluation data available",
                     font=('Arial', 14)).pack(pady=50)
            self.individual_analysis_tree = None
            return
        
        individual_results = self.group_results_by_individual()
        
        if individual_results:
            individual_frame = ttk.Frame(self.individual_content, padding=8)
            individual_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Filter and Actions frame
            actions_frame = ttk.Frame(individual_frame)
            actions_frame.pack(fill=tk.X, pady=(0, 5))
            
            # Application Group Filter on the left
            filter_frame = ttk.Frame(actions_frame)
            filter_frame.pack(side=tk.LEFT)
            
            ttk.Label(filter_frame, text="Filter by Application Group:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
            
            # Get all unique application groups
            cols = self.detect_columns()
            app_group_col = cols.get('app_group') if cols else None
            all_groups = set()
            
            if cols and self.df and app_group_col:
                for row in self.df:
                    row_group = self.safe_cell_text(row.get(app_group_col, 'Ungrouped'))
                    row_group = row_group.strip() if row_group.strip() else 'Ungrouped'
                    all_groups.add(row_group)
            
            # Create dropdown with "All" option
            group_options = ['All'] + sorted(all_groups)
            self.selected_app_group = tk.StringVar(value=selected_group if selected_group else 'All')
            
            group_dropdown = ttk.Combobox(filter_frame, textvariable=self.selected_app_group,
                                         values=group_options, state='readonly', width=50)
            group_dropdown.pack(side=tk.LEFT, padx=(0, 10))
            group_dropdown.bind('<<ComboboxSelected>>', lambda e: self.update_individual_dashboard(self.selected_app_group.get()))
            
            # Export button on the right
            ttk.Button(actions_frame, text="Export Resolver Analysis", command=self.export_resolver_analysis).pack(side=tk.RIGHT)
            
            tree_frame = ttk.Frame(individual_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            columns = ('S.No.', 'Resolved By', 'Application Group', 'Count', 'Worknotes Avg', 'Closing Avg', 'Total Avg', 'Good', 'Average', 'Poor', 'Blank Records')
            individual_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
            self.individual_analysis_tree = individual_tree
            
            resolver_column_widths = {
                'S.No.': 40,
                'Resolved By': 105,
                'Application Group': 150,
                'Count': 60,
                'Worknotes Avg': 90,
                'Closing Avg': 85,
                'Total Avg': 80,
                'Good': 55,
                'Average': 65,
                'Poor': 55,
                'Blank Records': 85
            }

            for col in columns:
                if col in ('Resolved By', 'Application Group'):
                    anchor = tk.W
                else:
                    anchor = tk.CENTER
                
                individual_tree.heading(col, text=col, anchor=anchor,
                                        command=lambda c=col, t=individual_tree: self.sort_tree_by_column(t, c, False))
                individual_tree.column(col, width=resolver_column_widths.get(col, 80), minwidth=55, anchor=anchor, stretch=True)
            
            vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=individual_tree.yview)
            individual_tree.configure(yscrollcommand=vsb.set)
            
            individual_tree.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            
            cols = self.detect_columns()
            individual_col = cols.get('resolved_by') if cols else None
            app_group_col = cols.get('app_group') if cols else None
            
            # Get the selected filter
            filter_group = selected_group if selected_group and selected_group != 'All' else None
            
            row_num = 1
            for person_name in sorted(individual_results.keys()):
                person_data = individual_results[person_name]
                
                # Get application groups for this person
                application_groups = set()
                if cols and self.df:
                    for row in self.df:
                        if individual_col:
                            row_person = self.safe_cell_text(row.get(individual_col, 'Unassigned'))
                            row_person = row_person.strip() if row_person.strip() else 'Unassigned'
                        else:
                            row_person = 'Unassigned'
                        
                        if row_person == person_name:
                            if app_group_col:
                                row_group = self.safe_cell_text(row.get(app_group_col, 'Ungrouped'))
                                row_group = row_group.strip() if row_group.strip() else 'Ungrouped'
                            else:
                                row_group = 'Ungrouped'
                            application_groups.add(row_group)
                
                # Apply filter: skip if filter is set and person doesn't belong to selected group
                if filter_group and filter_group not in application_groups:
                    continue
                
                person_count = len(person_data)
                person_worknotes_avg = sum(r['Worknotes Score'] for r in person_data) / person_count
                person_closing_avg = sum(r['Closing Comments Score'] for r in person_data) / person_count
                person_overall_avg = sum(r['Total Score'] for r in person_data) / person_count
                person_quality = Counter(r['Total Rating'] for r in person_data)
                
                person_blank = 0
                if cols and self.df:
                    for row in self.df:
                        if individual_col:
                            row_person = self.safe_cell_text(row.get(individual_col, 'Unassigned'))
                            row_person = row_person.strip() if row_person.strip() else 'Unassigned'
                        else:
                            row_person = 'Unassigned'
                        
                        if row_person == person_name:
                            worknotes_blank = False
                            closing_blank = False
                            
                            if cols.get('worknotes'):
                                worknotes_text = self.safe_cell_text(row.get(cols['worknotes'], ''))
                                if not worknotes_text or worknotes_text.strip() == '':
                                    worknotes_blank = True
                            
                            if cols.get('closing'):
                                closing_text = self.safe_cell_text(row.get(cols['closing'], ''))
                                if not closing_text or closing_text.strip() == '':
                                    closing_blank = True
                            
                            if worknotes_blank or closing_blank:
                                person_blank += 1
                
                values = (
                    row_num,
                    person_name,
                    ', '.join(sorted(application_groups)) if application_groups else 'Ungrouped',
                    person_count,
                    f"{person_worknotes_avg:.1f}",
                    f"{person_closing_avg:.1f}",
                    f"{person_overall_avg:.1f}",
                    person_quality.get('Good', 0),
                    person_quality.get('Average', 0),
                    person_quality.get('Poor', 0),
                    person_blank
                )
                
                item = individual_tree.insert('', tk.END, values=values)
                
                if person_overall_avg > 74:
                    individual_tree.item(item, tags=('good',))
                elif person_overall_avg >= 54:
                    individual_tree.item(item, tags=('average',))
                else:
                    individual_tree.item(item, tags=('poor',))
                
                row_num += 1
            
            individual_tree.tag_configure('good', background='#A8E6CF')
            individual_tree.tag_configure('average', background='#B3D9FF')
            individual_tree.tag_configure('poor', background='#FFE5B4')
        else:
            ttk.Label(self.individual_content,
                     text='No individual-level data available',
                     font=('Arial', 14)).pack(pady=50)
            self.individual_analysis_tree = None
        
    
    
    def create_metric_card(self, parent, title, value, icon, row, col, color, is_category=False, font_size=9):
        """Create a professional metric card widget - Compact with enhanced styling"""
        # Create card with subtle shadow effect using frame layering
        card = tk.Frame(parent, bg='#E0E0E0', relief=tk.FLAT)
        card.grid(row=row, column=col, padx=3, pady=2, sticky='nsew')
        parent.columnconfigure(col, weight=1)
        
        # Inner card for content with white background
        inner_card = tk.Frame(card, bg='white', relief=tk.FLAT)
        inner_card.pack(padx=1, pady=1, fill=tk.BOTH, expand=True)
        
        if is_category:
            # Professional styling for category column with gradient-like effect
            # Top section with color
            top_section = tk.Frame(inner_card, bg=color, height=35)
            top_section.pack(fill=tk.X)
            top_section.pack_propagate(False)
            
            tk.Label(top_section, text=icon, font=('Segoe UI Emoji', 16),
                    bg=color, fg='white').pack(expand=True)
            
            # Bottom section with title
            bottom_section = tk.Frame(inner_card, bg=color)
            bottom_section.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(bottom_section, text=title, font=('Segoe UI', 10, 'bold'),
                    bg=color, fg='white', wraplength=120, justify='center').pack(pady=3)
        else:
            # Professional styling for metric cards with clean layout
            # Icon at top
            tk.Label(inner_card, text=icon, font=('Segoe UI Emoji', 14),
                    bg='white', fg=color).pack(pady=(4, 0))
            
            # Value with emphasis
            tk.Label(inner_card, text=value, font=('Segoe UI', 14, 'bold'),
                    bg='white', fg=color).pack(pady=(2, 0))
            
            # Title at bottom with subtle color
            tk.Label(inner_card, text=title, font=('Segoe UI', font_size),
                    bg='white', fg='#666', wraplength=120, justify='center').pack(pady=(0, 4))
    
    def create_progress_bar(self, parent, label, count, percentage):
        """Create a progress bar for quality distribution"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        # Label
        label_text = f"{label}: {count} ({percentage:.1f}%)"
        ttk.Label(frame, text=label_text, width=25).pack(side=tk.LEFT)
        
        # Progress bar
        progress = ttk.Progressbar(frame, length=400, mode='determinate',
                                   maximum=100, value=percentage)
        progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    def export_results(self):
        """Export evaluation results to Excel"""
        if not self.evaluation_results:
            messagebox.showwarning("Warning", "No evaluation results to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.export_results_to_excel(file_path)
                messagebox.showinfo("Success", f"Results exported to {os.path.basename(file_path)}")
                self.status_var.set(f"Results exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def export_resolver_analysis(self):
        """Export resolver analysis to Excel"""
        if not self.evaluation_results:
            messagebox.showwarning("Warning", "No resolver analysis to export!")
            return
        
        resolver_rows = self.get_resolver_analysis_rows()
        if not resolver_rows:
            messagebox.showwarning("Warning", "No resolver analysis to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Resolver Analysis",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.export_resolver_analysis_to_excel(file_path, resolver_rows)
                messagebox.showinfo("Success", f"Resolver analysis exported to {os.path.basename(file_path)}")
                self.status_var.set("Resolver analysis exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export resolver analysis: {str(e)}")
    
    def export_group_analysis(self):
        """Export application group analysis to Excel"""
        if not self.evaluation_results:
            messagebox.showwarning("Warning", "No application group analysis to export!")
            return
        
        grouped_rows = self.get_group_analysis_rows()
        if not grouped_rows:
            messagebox.showwarning("Warning", "No application group analysis to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Group Analysis",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.export_group_analysis_to_excel(file_path, grouped_rows)
                messagebox.showinfo("Success", f"Group analysis exported to {os.path.basename(file_path)}")
                self.status_var.set("Application group analysis exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export group analysis: {str(e)}")
    
    def export_complete_dataset(self):
        """Export complete dataset with all three analyses in separate sheets"""
        if not self.evaluation_results:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        # Get all three datasets
        group_rows = self.get_group_analysis_rows()
        resolver_rows = self.get_resolver_analysis_rows()
        
        if not group_rows and not resolver_rows:
            messagebox.showwarning("Warning", "No analysis data available to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Complete Dataset",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.export_complete_dataset_to_excel(file_path, group_rows, resolver_rows)
                messagebox.showinfo("Success", f"Complete dataset exported to {os.path.basename(file_path)}")
                self.status_var.set("Complete dataset exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export complete dataset: {str(e)}")
    
    def export_complete_dataset_to_excel(self, file_path, group_rows, resolver_rows):
        """Export all three analyses to a single Excel file with multiple sheets"""
        from openpyxl.styles import PatternFill
        
        workbook = openpyxl.Workbook()
        
        # Remove default sheet
        if workbook.active:
            workbook.remove(workbook.active)
        
        # Define color fills based on evaluation criteria
        good_fill = PatternFill(start_color="A8E6CF", end_color="A8E6CF", fill_type="solid")
        average_fill = PatternFill(start_color="B3D9FF", end_color="B3D9FF", fill_type="solid")
        poor_fill = PatternFill(start_color="FFE5B4", end_color="FFE5B4", fill_type="solid")
        
        # Get thresholds from config
        criteria = self.config.get('evaluation_criteria', {})
        good_threshold = criteria.get('good_threshold', 74)
        average_threshold = criteria.get('average_threshold', 50)
        
        # Sheet 1: Application Group Analysis
        if group_rows:
            group_sheet = workbook.create_sheet("Application Group Analysis")
            headers = list(group_rows[0].keys())
            group_sheet.append(headers)
            
            for row_idx, row in enumerate(group_rows, start=2):
                group_sheet.append([row.get(header, "") for header in headers])
                
                # Apply color based on Total Avg
                total_avg = row.get('Total Avg', 0)
                if isinstance(total_avg, (int, float)):
                    if total_avg > good_threshold:
                        fill = good_fill
                    elif total_avg >= average_threshold:
                        fill = average_fill
                    else:
                        fill = poor_fill
                    
                    # Apply fill to entire row
                    for col_idx in range(1, len(headers) + 1):
                        group_sheet.cell(row=row_idx, column=col_idx).fill = fill
        
        # Sheet 2: Resolver Analysis
        if resolver_rows:
            resolver_sheet = workbook.create_sheet("Resolver Analysis")
            headers = list(resolver_rows[0].keys())
            resolver_sheet.append(headers)
            
            for row_idx, row in enumerate(resolver_rows, start=2):
                resolver_sheet.append([row.get(header, "") for header in headers])
                
                # Apply color based on Total Avg
                total_avg = row.get('Total Avg', 0)
                if isinstance(total_avg, (int, float)):
                    if total_avg > good_threshold:
                        fill = good_fill
                    elif total_avg >= average_threshold:
                        fill = average_fill
                    else:
                        fill = poor_fill
                    
                    # Apply fill to entire row
                    for col_idx in range(1, len(headers) + 1):
                        resolver_sheet.cell(row=row_idx, column=col_idx).fill = fill
        
        # Sheet 3: Evaluation Results
        if self.evaluation_results and self.df:
            results_sheet = workbook.create_sheet("Evaluation Results")
            original_columns = list(self.df[0].keys()) if self.df else []
            cols = self.detect_columns() or {}
            excluded_original_columns = {
                col_name for col_name in [
                    cols.get('incident'),
                    cols.get('worknotes'),
                    cols.get('closing'),
                    cols.get('app_group')
                ] if col_name
            }
            export_original_columns = [col for col in original_columns if col not in excluded_original_columns]
            result_columns = [
                'Number',
                'Group',
                'Resolved by',
                'Resolved',
                'Worknotes Score',
                'Worknotes Rating',
                'Closing Comments Score',
                'Closing Comments Rating',
                'Total Score',
                'Total Rating',
                'Worknotes Issues',
                'Closing Comments Issues'
            ]
            headers = ['S.No.'] + result_columns
            results_sheet.append(headers)
            
            max_rows = len(self.evaluation_results or [])
            for idx in range(max_rows):
                result_row = self.evaluation_results[idx] if idx < len(self.evaluation_results or []) else {}
                row_values = [idx + 1] + [result_row.get(col, "") for col in result_columns]
                results_sheet.append(row_values)
                
                # Apply color based on Total Score
                total_score = result_row.get('Total Score', 0)
                if isinstance(total_score, (int, float)):
                    if total_score > good_threshold:
                        fill = good_fill
                    elif total_score >= average_threshold:
                        fill = average_fill
                    else:
                        fill = poor_fill
                    
                    # Apply fill to entire row
                    row_idx = idx + 2  # +2 because of header row and 1-based indexing
                    for col_idx in range(1, len(headers) + 1):
                        results_sheet.cell(row=row_idx, column=col_idx).fill = fill
        
        workbook.save(file_path)
    
    def get_resolver_analysis_rows(self):
        """Build resolver analysis rows for display/export"""
        individual_results = self.group_results_by_individual()
        if not individual_results:
            return []
        
        cols = self.detect_columns()
        individual_col = cols.get('resolved_by') if cols else None
        app_group_col = cols.get('app_group') if cols else None
        rows = []
        
        for idx, person_name in enumerate(sorted(individual_results.keys()), start=1):
            person_data = individual_results[person_name]
            person_count = len(person_data)
            person_worknotes_avg = sum(r['Worknotes Score'] for r in person_data) / person_count
            person_closing_avg = sum(r['Closing Comments Score'] for r in person_data) / person_count
            person_overall_avg = sum(r['Total Score'] for r in person_data) / person_count
            person_quality = Counter(r['Total Rating'] for r in person_data)
            
            person_blank = 0
            if cols and self.df:
                for row in self.df:
                    if individual_col:
                        row_person = self.safe_cell_text(row.get(individual_col, 'Unassigned'))
                        row_person = row_person.strip() if row_person.strip() else 'Unassigned'
                    else:
                        row_person = 'Unassigned'
                    
                    if row_person == person_name:
                        worknotes_blank = False
                        closing_blank = False
                        
                        if cols.get('worknotes'):
                            worknotes_text = self.safe_cell_text(row.get(cols['worknotes'], ''))
                            if not worknotes_text or worknotes_text.strip() == '':
                                worknotes_blank = True
                        
                        if cols.get('closing'):
                            closing_text = self.safe_cell_text(row.get(cols['closing'], ''))
                            if not closing_text or closing_text.strip() == '':
                                closing_blank = True
                        
                        if worknotes_blank or closing_blank:
                            person_blank += 1
            
            application_groups = set()
            if cols and self.df:
                for row in self.df:
                    if individual_col:
                        row_person = self.safe_cell_text(row.get(individual_col, 'Unassigned'))
                        row_person = row_person.strip() if row_person.strip() else 'Unassigned'
                    else:
                        row_person = 'Unassigned'
                    
                    if row_person == person_name:
                        if app_group_col:
                            row_group = self.safe_cell_text(row.get(app_group_col, 'Ungrouped'))
                            row_group = row_group.strip() if row_group.strip() else 'Ungrouped'
                        else:
                            row_group = 'Ungrouped'
                        application_groups.add(row_group)
            
            rows.append({
                'S.No.': idx,
                'Resolved By': person_name,
                'Application Group': ', '.join(sorted(application_groups)) if application_groups else 'Ungrouped',
                'Count': person_count,
                'Worknotes Avg': round(person_worknotes_avg, 1),
                'Closing Avg': round(person_closing_avg, 1),
                'Total Avg': round(person_overall_avg, 1),
                'Good': person_quality.get('Good', 0),
                'Average': person_quality.get('Average', 0),
                'Poor': person_quality.get('Poor', 0),
                'Blank Records': person_blank
            })
        
        return rows
    
    def get_group_analysis_rows(self):
        """Build application group analysis rows for display/export"""
        grouped_results = self.group_results_by_application()
        if not grouped_results:
            return []
        
        cols = self.detect_columns()
        rows = []
        
        for idx, group_name in enumerate(sorted(grouped_results.keys()), start=1):
            group_data = grouped_results[group_name]
            group_count = len(group_data)
            group_worknotes_avg = sum(r['Worknotes Score'] for r in group_data) / group_count
            group_closing_avg = sum(r['Closing Comments Score'] for r in group_data) / group_count
            group_quality = Counter(r['Total Rating'] for r in group_data)
            
            group_blank = 0
            if cols and self.df:
                app_col = cols.get('app_group')
                for row in self.df:
                    if app_col:
                        row_group = self.safe_cell_text(row.get(app_col, 'Ungrouped'))
                        row_group = row_group.strip() if row_group.strip() else 'Ungrouped'
                    else:
                        row_group = 'Ungrouped'
                    
                    if row_group == group_name:
                        worknotes_blank = False
                        closing_blank = False
                        
                        if cols.get('worknotes'):
                            worknotes_text = self.safe_cell_text(row.get(cols['worknotes'], ''))
                            if not worknotes_text or worknotes_text.strip() == '':
                                worknotes_blank = True
                        
                        if cols.get('closing'):
                            closing_text = self.safe_cell_text(row.get(cols['closing'], ''))
                            if not closing_text or closing_text.strip() == '':
                                closing_blank = True
                        
                        if worknotes_blank or closing_blank:
                            group_blank += 1
            
            group_avg = (group_worknotes_avg + group_closing_avg) / 2
            
            rows.append({
                'S.No.': idx,
                'Group': group_name,
                'Count': group_count,
                'Worknotes Avg': round(group_worknotes_avg, 1),
                'Closing Avg': round(group_closing_avg, 1),
                'Total Avg': round(group_avg, 1),
                'Good': group_quality.get('Good', 0),
                'Average': group_quality.get('Average', 0),
                'Poor': group_quality.get('Poor', 0),
                'Blank Worknotes': group_blank
            })
        
        return rows
    
    def export_resolver_analysis_to_excel(self, file_path, resolver_rows):
        """Export resolver analysis rows to Excel"""
        from openpyxl.styles import PatternFill
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        if sheet is None:
            sheet = workbook.create_sheet("Resolver Analysis")
        else:
            sheet.title = "Resolver Analysis"
        
        if not resolver_rows:
            workbook.save(file_path)
            return
        
        # Define color fills
        good_fill = PatternFill(start_color="A8E6CF", end_color="A8E6CF", fill_type="solid")
        average_fill = PatternFill(start_color="B3D9FF", end_color="B3D9FF", fill_type="solid")
        poor_fill = PatternFill(start_color="FFE5B4", end_color="FFE5B4", fill_type="solid")
        
        # Get thresholds
        criteria = self.config.get('evaluation_criteria', {})
        good_threshold = criteria.get('good_threshold', 74)
        average_threshold = criteria.get('average_threshold', 50)
        
        headers = list(resolver_rows[0].keys())
        sheet.append(headers)
        
        for row_idx, row in enumerate(resolver_rows, start=2):
            sheet.append([row.get(header, "") for header in headers])
            
            # Apply color based on Total Avg
            total_avg = row.get('Total Avg', 0)
            if isinstance(total_avg, (int, float)):
                if total_avg > good_threshold:
                    fill = good_fill
                elif total_avg >= average_threshold:
                    fill = average_fill
                else:
                    fill = poor_fill
                
                # Apply fill to entire row
                for col_idx in range(1, len(headers) + 1):
                    sheet.cell(row=row_idx, column=col_idx).fill = fill
        
        workbook.save(file_path)
    
    def export_group_analysis_to_excel(self, file_path, grouped_rows):
        """Export application group analysis rows to Excel"""
        from openpyxl.styles import PatternFill
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        if sheet is None:
            sheet = workbook.create_sheet("Group Analysis")
        else:
            sheet.title = "Group Analysis"
        
        if not grouped_rows:
            workbook.save(file_path)
            return
        
        # Define color fills
        good_fill = PatternFill(start_color="A8E6CF", end_color="A8E6CF", fill_type="solid")
        average_fill = PatternFill(start_color="B3D9FF", end_color="B3D9FF", fill_type="solid")
        poor_fill = PatternFill(start_color="FFE5B4", end_color="FFE5B4", fill_type="solid")
        
        # Get thresholds
        criteria = self.config.get('evaluation_criteria', {})
        good_threshold = criteria.get('good_threshold', 74)
        average_threshold = criteria.get('average_threshold', 50)
        
        headers = list(grouped_rows[0].keys())
        sheet.append(headers)
        
        for row_idx, row in enumerate(grouped_rows, start=2):
            sheet.append([row.get(header, "") for header in headers])
            
            # Apply color based on Total Avg
            total_avg = row.get('Total Avg', 0)
            if isinstance(total_avg, (int, float)):
                if total_avg > good_threshold:
                    fill = good_fill
                elif total_avg >= average_threshold:
                    fill = average_fill
                else:
                    fill = poor_fill
                
                # Apply fill to entire row
                for col_idx in range(1, len(headers) + 1):
                    sheet.cell(row=row_idx, column=col_idx).fill = fill
        
        workbook.save(file_path)
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configuration Settings")
        settings_window.geometry("600x700")
        
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Worknotes settings
        worknotes_frame = ttk.Frame(notebook)
        notebook.add(worknotes_frame, text="Worknotes")
        self.create_settings_tab(worknotes_frame, 'worknotes')
        
        # Closing comments settings
        closing_frame = ttk.Frame(notebook)
        notebook.add(closing_frame, text="Closing Comments")
        self.create_settings_tab(closing_frame, 'closing_comments')
        
        # Buttons
        btn_frame = ttk.Frame(settings_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(btn_frame, text="Save", command=lambda: self.save_settings(settings_window)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.RIGHT)
    
    def create_settings_tab(self, parent, config_key):
        """Create settings tab content"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Required keywords
        ttk.Label(frame, text="Required Keywords (comma-separated):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(frame, text="Scoring is based 100% on keyword presence",
                 font=('Arial', 9, 'italic')).grid(row=1, column=0, sticky=tk.W, pady=2)
        req_kw_text = scrolledtext.ScrolledText(frame, width=50, height=10)
        req_kw_text.grid(row=2, column=0, columnspan=2, pady=5)
        req_kw_text.insert(1.0, ', '.join(self.config[config_key]['required_keywords']))
        
        # Store references for saving
        setattr(self, f'{config_key}_req_kw', req_kw_text)
    
    def save_settings(self, window):
        """Save configuration settings"""
        try:
            if not all([
                self.worknotes_req_kw,
                self.closing_comments_req_kw,
            ]):
                raise ValueError("Settings controls are not initialized")
            
            worknotes_req_kw = self.worknotes_req_kw
            closing_comments_req_kw = self.closing_comments_req_kw
            
            # Update worknotes config
            self.config['worknotes']['required_keywords'] = [
                kw.strip() for kw in worknotes_req_kw.get(1.0, tk.END).split(',') if kw.strip()
            ]
            
            # Update closing comments config
            self.config['closing_comments']['required_keywords'] = [
                kw.strip() for kw in closing_comments_req_kw.get(1.0, tk.END).split(',') if kw.strip()
            ]
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def reset_config(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            self.config = self.load_default_config()
            messagebox.showinfo("Success", "Settings reset to defaults!")
    
    def safe_cell_text(self, value):
        """Convert Excel cell values to safe text"""
        return "" if value is None else str(value)
    
    def read_excel_data(self, file_path):
        """Read Excel data without pandas"""
        extension = os.path.splitext(file_path)[1].lower()
        
        if extension == '.xlsx':
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            sheet = workbook.active
            if sheet is None:
                return []
            rows = list(sheet.iter_rows(values_only=True))
        elif extension == '.xls':
            workbook = xlrd.open_workbook(file_path)
            sheet = workbook.sheet_by_index(0)
            rows = [sheet.row_values(i) for i in range(sheet.nrows)]
        else:
            raise ValueError("Unsupported file format. Please select .xlsx or .xls")
        
        if not rows:
            return []
        
        headers = [str(cell) if cell is not None else f"Column{idx+1}" for idx, cell in enumerate(rows[0])]
        data = []
        for row in rows[1:]:
            row_dict = {}
            for idx, header in enumerate(headers):
                row_dict[header] = row[idx] if idx < len(row) else None
            data.append(row_dict)
        return data
    
    def calculate_average(self, key):
        values = [float(row.get(key, 0) or 0) for row in (self.evaluation_results or [])]
        return sum(values) / len(values) if values else 0
    
    def calculate_median(self, key):
        values = sorted(float(row.get(key, 0) or 0) for row in (self.evaluation_results or []))
        if not values:
            return 0
        mid = len(values) // 2
        if len(values) % 2 == 0:
            return (values[mid - 1] + values[mid]) / 2
        return values[mid]
    
    def calculate_min(self, key):
        values = [float(row.get(key, 0) or 0) for row in (self.evaluation_results or [])]
        return min(values) if values else 0
    
    def calculate_max(self, key):
        values = [float(row.get(key, 0) or 0) for row in (self.evaluation_results or [])]
        return max(values) if values else 0
    
    def export_results_to_excel(self, file_path):
        """Export original data and results without pandas"""
        from openpyxl.styles import PatternFill
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        if sheet is None:
            sheet = workbook.create_sheet("Evaluation Results")
        else:
            sheet.title = "Evaluation Results"
        
        # Define color fills
        good_fill = PatternFill(start_color="A8E6CF", end_color="A8E6CF", fill_type="solid")
        average_fill = PatternFill(start_color="B3D9FF", end_color="B3D9FF", fill_type="solid")
        poor_fill = PatternFill(start_color="FFE5B4", end_color="FFE5B4", fill_type="solid")
        
        # Get thresholds
        criteria = self.config.get('evaluation_criteria', {})
        good_threshold = criteria.get('good_threshold', 74)
        average_threshold = criteria.get('average_threshold', 50)
        
        original_columns = list(self.df[0].keys()) if self.df else []
        cols = self.detect_columns() or {}
        excluded_original_columns = {
            col_name for col_name in [
                cols.get('incident'),
                cols.get('worknotes'),
                cols.get('closing'),
                cols.get('app_group')
            ] if col_name
        }
        export_original_columns = [col for col in original_columns if col not in excluded_original_columns]
        result_columns = [
            'Number',
            'Group',
            'Resolved by',
            'Resolved',
            'Worknotes Score',
            'Worknotes Rating',
            'Closing Comments Score',
            'Closing Comments Rating',
            'Total Score',
            'Total Rating',
            'Worknotes Issues',
            'Closing Comments Issues'
        ]
        headers = ['S.No.'] + result_columns
        sheet.append(headers)
        
        max_rows = len(self.evaluation_results or [])
        for idx in range(max_rows):
            result_row = self.evaluation_results[idx] if idx < len(self.evaluation_results or []) else {}
            row_values = [idx + 1] + [result_row.get(col, "") for col in result_columns]
            sheet.append(row_values)
            
            # Apply color based on Total Score
            total_score = result_row.get('Total Score', 0)
            if isinstance(total_score, (int, float)):
                if total_score > good_threshold:
                    fill = good_fill
                elif total_score >= average_threshold:
                    fill = average_fill
                else:
                    fill = poor_fill
                
                # Apply fill to entire row
                row_idx = idx + 2  # +2 for header and 1-based indexing
                for col_idx in range(1, len(headers) + 1):
                    sheet.cell(row=row_idx, column=col_idx).fill = fill
        
        workbook.save(file_path)


def main():
    root = tk.Tk()
    app = IncidentEvaluator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# Made with Bob
