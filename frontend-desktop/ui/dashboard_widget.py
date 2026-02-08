from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
                             QFileDialog, QMessageBox, QFrame, QScrollArea, QGridLayout,
                             QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class DashboardWidget(QWidget):
    """Main dashboard widget"""
    
    logout_signal = pyqtSignal()
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.datasets = []
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)
        
        # Upload section
        self.upload_section = self.create_upload_section()
        self.content_layout.addWidget(self.upload_section)
        
        # Dataset selector
        self.dataset_selector = self.create_dataset_selector()
        self.content_layout.addWidget(self.dataset_selector)
        
        # Visualization area (initially hidden)
        self.viz_widget = QWidget()
        self.viz_layout = QVBoxLayout(self.viz_widget)
        self.viz_layout.setSpacing(20)
        self.viz_widget.hide()
        self.content_layout.addWidget(self.viz_widget)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def create_header(self):
        """Create header bar"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #e5e7eb;
            }
        """)
        header.setFixedHeight(80)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Left side - Title
        left_layout = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title = QLabel("Chemical Equipment Visualizer")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #667eea;")
        
        subtitle = QLabel("Data Analysis & Visualization Platform")
        subtitle.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        left_layout.addLayout(title_layout)
        left_layout.addStretch()
        
        # Right side - User info and logout
        right_layout = QHBoxLayout()
        right_layout.setSpacing(15)
        
        if self.api_client.user:
            user_name = self.api_client.user.get('first_name', '') + ' ' + self.api_client.user.get('last_name', '')
            if not user_name.strip():
                user_name = self.api_client.user.get('username', 'User')
            
            user_label = QLabel(f"Welcome, {user_name}")
            user_label.setFont(QFont("Arial", 12, QFont.Bold))
            user_label.setStyleSheet("color: #1f2937;")
            right_layout.addWidget(user_label)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        right_layout.addWidget(logout_btn)
        
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        
        return header
    
    def create_upload_section(self):
        """Create CSV upload section"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Title
        title = QLabel("Upload CSV Data")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #1f2937;")
        layout.addWidget(title)
        
        # Upload button
        btn_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Select & Upload CSV File")
        self.upload_btn.setMinimumHeight(45)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.upload_btn.clicked.connect(self.handle_upload)
        btn_layout.addWidget(self.upload_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Info label
        info = QLabel("Upload CSV files with columns: Equipment Name, Type, Flowrate, Pressure, Temperature")
        info.setStyleSheet("color: #6b7280; font-size: 12px; margin-top: 10px;")
        layout.addWidget(info)
        
        return card
    
    def create_dataset_selector(self):
        """Create dataset selector section"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        title = QLabel("Your Datasets")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #1f2937;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_datasets)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Dataset combo box
        combo_layout = QHBoxLayout()
        
        combo_layout.addWidget(QLabel("Select Dataset:"))
        
        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumHeight(35)
        self.dataset_combo.currentIndexChanged.connect(self.handle_dataset_selection)
        combo_layout.addWidget(self.dataset_combo, 1)
        
        # Action buttons
        self.view_btn = QPushButton("View Details")
        self.view_btn.setEnabled(False)
        self.view_btn.clicked.connect(self.load_dataset_details)
        self.view_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        """)
        combo_layout.addWidget(self.view_btn)
        
        self.download_btn = QPushButton("Download PDF")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_report)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        combo_layout.addWidget(self.download_btn)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_dataset)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        combo_layout.addWidget(self.delete_btn)
        
        layout.addLayout(combo_layout)
        
        return card
    
    def load_datasets(self):
        """Load datasets from API"""
        try:
            self.datasets = self.api_client.get_datasets()
            self.dataset_combo.clear()
            
            if not self.datasets:
                self.dataset_combo.addItem("No datasets available")
                self.view_btn.setEnabled(False)
                self.download_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
            else:
                for dataset in self.datasets:
                    self.dataset_combo.addItem(
                        f"{dataset['filename']} ({dataset['total_count']} items)",
                        dataset['id']
                    )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load datasets: {str(e)}")
    
    def handle_dataset_selection(self, index):
        """Handle dataset selection"""
        if index >= 0 and self.datasets:
            self.view_btn.setEnabled(True)
            self.download_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            self.view_btn.setEnabled(False)
            self.download_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
    
    def handle_upload(self):
        """Handle CSV upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                self.upload_btn.setEnabled(False)
                self.upload_btn.setText("Uploading...")
                
                self.api_client.upload_csv(file_path)
                
                QMessageBox.information(self, "Success", "File uploaded successfully!")
                self.load_datasets()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Upload failed: {str(e)}")
            finally:
                self.upload_btn.setEnabled(True)
                self.upload_btn.setText("Select & Upload CSV File")
    
    def load_dataset_details(self):
        """Load and display dataset details"""
        dataset_id = self.dataset_combo.currentData()
        if not dataset_id:
            return
        
        try:
            self.current_dataset = self.api_client.get_dataset_detail(dataset_id)
            self.display_dataset_details()
            self.viz_widget.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load dataset: {str(e)}")
    
    def display_dataset_details(self):
        """Display dataset details with charts and table"""
        # Clear previous content
        while self.viz_layout.count():
            child = self.viz_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        dataset = self.current_dataset
        
        # Summary cards
        summary_card = self.create_summary_cards(dataset)
        self.viz_layout.addWidget(summary_card)
        
        # Charts
        charts_widget = self.create_charts(dataset)
        self.viz_layout.addWidget(charts_widget)
        
        # Data table
        table_card = self.create_data_table(dataset)
        self.viz_layout.addWidget(table_card)
    
    def create_summary_cards(self, dataset):
        """Create summary statistics cards"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        title = QLabel("Summary Statistics")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Grid of stats
        grid = QGridLayout()
        grid.setSpacing(15)
        
        stats = [
            ("Total Equipment", dataset['total_count'], "#667eea"),
            ("Avg Flowrate", f"{dataset['avg_flowrate']:.2f}", "#10b981"),
            ("Avg Pressure", f"{dataset['avg_pressure']:.2f}", "#f59e0b"),
            ("Avg Temperature", f"{dataset['avg_temperature']:.2f}", "#ef4444"),
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_frame = QFrame()
            stat_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border-radius: 8px;
                    padding: 15px;
                }}
            """)
            
            stat_layout = QVBoxLayout(stat_frame)
            
            stat_label = QLabel(label)
            stat_label.setStyleSheet("color: white; font-size: 12px; font-weight: 600;")
            stat_layout.addWidget(stat_label)
            
            stat_value = QLabel(str(value))
            stat_value.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
            stat_layout.addWidget(stat_value)
            
            grid.addWidget(stat_frame, 0, i)
        
        layout.addLayout(grid)
        
        return card
    
    def create_charts(self, dataset):
        """Create visualization charts"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        title = QLabel("Data Visualization")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Create figure with subplots
        fig = Figure(figsize=(14, 10))
        
        # Equipment Type Distribution (Pie Chart)
        ax1 = fig.add_subplot(2, 2, 1)
        types = list(dataset['equipment_types'].keys())
        counts = list(dataset['equipment_types'].values())
        colors = ['#667eea', '#764ba2', '#10b981', '#f59e0b', '#ef4444', '#3b82f6']
        ax1.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)])
        ax1.set_title('Equipment Type Distribution', fontweight='bold', fontsize=12)
        
        # Parameter Comparison (Bar Chart)
        ax2 = fig.add_subplot(2, 2, 2)
        records = dataset['records'][:10]  # Show first 10 for readability
        names = [r['equipment_name'] for r in records]
        flowrates = [r['flowrate'] for r in records]
        pressures = [r['pressure'] for r in records]
        temperatures = [r['temperature'] for r in records]
        
        x = range(len(names))
        width = 0.25
        
        ax2.bar([i - width for i in x], flowrates, width, label='Flowrate', color='#667eea')
        ax2.bar(x, pressures, width, label='Pressure', color='#764ba2')
        ax2.bar([i + width for i in x], temperatures, width, label='Temperature', color='#10b981')
        
        ax2.set_xlabel('Equipment', fontweight='bold')
        ax2.set_ylabel('Value', fontweight='bold')
        ax2.set_title('Parameter Comparison (First 10)', fontweight='bold', fontsize=12)
        ax2.set_xticks(x)
        ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # Flowrate Trend (Line Chart)
        ax3 = fig.add_subplot(2, 2, 3)
        all_names = [r['equipment_name'] for r in dataset['records']]
        all_flowrates = [r['flowrate'] for r in dataset['records']]
        ax3.plot(all_flowrates, marker='o', color='#667eea', linewidth=2, markersize=4)
        ax3.set_xlabel('Equipment Index', fontweight='bold')
        ax3.set_ylabel('Flowrate', fontweight='bold')
        ax3.set_title('Flowrate Trend', fontweight='bold', fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.fill_between(range(len(all_flowrates)), all_flowrates, alpha=0.3, color='#667eea')
        
        # Pressure vs Temperature Scatter
        ax4 = fig.add_subplot(2, 2, 4)
        all_pressures = [r['pressure'] for r in dataset['records']]
        all_temperatures = [r['temperature'] for r in dataset['records']]
        scatter = ax4.scatter(all_pressures, all_temperatures, c=all_flowrates, 
                            cmap='viridis', s=100, alpha=0.6, edgecolors='black')
        ax4.set_xlabel('Pressure', fontweight='bold')
        ax4.set_ylabel('Temperature', fontweight='bold')
        ax4.set_title('Pressure vs Temperature (colored by Flowrate)', fontweight='bold', fontsize=12)
        ax4.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax4, label='Flowrate')
        
        fig.tight_layout()
        
        # Add canvas to layout
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        return card
    
    def create_data_table(self, dataset):
        """Create data table"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        title = QLabel("Equipment Records")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Create table
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setAlternatingRowColors(True)
        
        records = dataset['records']
        table.setRowCount(len(records))
        
        for i, record in enumerate(records):
            table.setItem(i, 0, QTableWidgetItem(record['equipment_name']))
            table.setItem(i, 1, QTableWidgetItem(record['equipment_type']))
            table.setItem(i, 2, QTableWidgetItem(f"{record['flowrate']:.2f}"))
            table.setItem(i, 3, QTableWidgetItem(f"{record['pressure']:.2f}"))
            table.setItem(i, 4, QTableWidgetItem(f"{record['temperature']:.2f}"))
        
        layout.addWidget(table)
        
        return card
    
    def download_report(self):
        """Download PDF report"""
        dataset_id = self.dataset_combo.currentData()
        if not dataset_id:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", f"report_{dataset_id}.pdf", "PDF Files (*.pdf)"
        )
        
        if save_path:
            try:
                self.api_client.download_report(dataset_id, save_path)
                QMessageBox.information(self, "Success", f"Report saved to:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to download report: {str(e)}")
    
    def delete_dataset(self):
        """Delete selected dataset"""
        dataset_id = self.dataset_combo.currentData()
        if not dataset_id:
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            "Are you sure you want to delete this dataset?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.api_client.delete_dataset(dataset_id)
                QMessageBox.information(self, "Success", "Dataset deleted successfully!")
                self.load_datasets()
                self.viz_widget.hide()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete dataset: {str(e)}")
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self, "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.logout_signal.emit()
