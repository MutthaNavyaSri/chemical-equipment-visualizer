from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from api.client import APIClient
from .auth_widget import AuthWidget
from .dashboard_widget import DashboardWidget


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.init_ui()
        self.setup_styling()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget with stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Stacked widget for switching between auth and dashboard
        self.stacked_widget = QStackedWidget()
        
        # Auth widget (login/register)
        self.auth_widget = AuthWidget(self.api_client)
        self.auth_widget.login_success.connect(self.show_dashboard)
        
        # Dashboard widget
        self.dashboard_widget = DashboardWidget(self.api_client)
        self.dashboard_widget.logout_signal.connect(self.show_auth)
        
        self.stacked_widget.addWidget(self.auth_widget)
        self.stacked_widget.addWidget(self.dashboard_widget)
        
        self.main_layout.addWidget(self.stacked_widget)
        
        # Show auth page first
        self.stacked_widget.setCurrentWidget(self.auth_widget)
    
    def setup_styling(self):
        """Setup application styling"""
        # Set application palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 242, 245))
        palette.setColor(QPalette.WindowText, QColor(31, 41, 55))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(243, 244, 246))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(31, 41, 55))
        palette.setColor(QPalette.Text, QColor(31, 41, 55))
        palette.setColor(QPalette.Button, QColor(255, 255, 255))
        palette.setColor(QPalette.ButtonText, QColor(31, 41, 55))
        palette.setColor(QPalette.Link, QColor(102, 126, 234))
        palette.setColor(QPalette.Highlight, QColor(102, 126, 234))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        self.setPalette(palette)
        
        # Set global stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
            QPushButton:pressed {
                background-color: #4451b8;
            }
            QPushButton:disabled {
                background-color: #9ca3af;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
            QLabel {
                font-size: 14px;
                color: #1f2937;
            }
            QTableWidget {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
                gridline-color: #e5e7eb;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border: none;
                font-weight: 600;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
            }
            QComboBox:hover {
                border-color: #667eea;
            }
            QScrollBar:vertical {
                width: 12px;
                background: #f3f4f6;
            }
            QScrollBar::handle:vertical {
                background: #667eea;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5568d3;
            }
        """)
    
    def show_dashboard(self):
        """Show dashboard after successful login"""
        self.dashboard_widget.load_datasets()
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)
    
    def show_auth(self):
        """Show auth page after logout"""
        self.api_client.access_token = None
        self.api_client.refresh_token = None
        self.api_client.user = None
        self.stacked_widget.setCurrentWidget(self.auth_widget)
        self.auth_widget.clear_form()
