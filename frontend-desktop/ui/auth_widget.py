from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTabWidget, QMessageBox,
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class AuthWidget(QWidget):
    """Widget for authentication (login/register)"""
    
    login_success = pyqtSignal()
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Auth card
        self.auth_card = QFrame()
        self.auth_card.setMaximumWidth(500)
        self.auth_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        card_layout = QVBoxLayout(self.auth_card)
        card_layout.setSpacing(20)
        
        # Title
        title = QLabel("Chemical Equipment Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #667eea;")
        card_layout.addWidget(title)
        
        subtitle = QLabel("Desktop Application")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #6b7280;")
        card_layout.addWidget(subtitle)
        
        # Tab widget for login/register
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f3f4f6;
                color: #6b7280;
                padding: 12px 24px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background-color: #667eea;
                color: white;
            }
        """)
        
        # Login tab
        login_tab = self.create_login_tab()
        self.tab_widget.addTab(login_tab, "Login")
        
        # Register tab
        register_tab = self.create_register_tab()
        self.tab_widget.addTab(register_tab, "Register")
        
        card_layout.addWidget(self.tab_widget)
        
        layout.addWidget(self.auth_card)
        self.setLayout(layout)
    
    def create_login_tab(self):
        """Create login tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Username
        layout.addWidget(QLabel("Username"))
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        layout.addWidget(self.login_username)
        
        # Password
        layout.addWidget(QLabel("Password"))
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.returnPressed.connect(self.handle_login)
        layout.addWidget(self.login_password)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setMinimumHeight(45)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_register_tab(self):
        """Create register tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Name fields
        name_layout = QHBoxLayout()
        
        first_layout = QVBoxLayout()
        first_layout.addWidget(QLabel("First Name"))
        self.register_first_name = QLineEdit()
        self.register_first_name.setPlaceholderText("John")
        first_layout.addWidget(self.register_first_name)
        
        last_layout = QVBoxLayout()
        last_layout.addWidget(QLabel("Last Name"))
        self.register_last_name = QLineEdit()
        self.register_last_name.setPlaceholderText("Doe")
        last_layout.addWidget(self.register_last_name)
        
        name_layout.addLayout(first_layout)
        name_layout.addLayout(last_layout)
        layout.addLayout(name_layout)
        
        # Username
        layout.addWidget(QLabel("Username *"))
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username")
        layout.addWidget(self.register_username)
        
        # Email
        layout.addWidget(QLabel("Email *"))
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("your.email@example.com")
        layout.addWidget(self.register_email)
        
        # Password
        layout.addWidget(QLabel("Password *"))
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setPlaceholderText("At least 6 characters")
        layout.addWidget(self.register_password)
        
        # Confirm Password
        layout.addWidget(QLabel("Confirm Password *"))
        self.register_confirm_password = QLineEdit()
        self.register_confirm_password.setEchoMode(QLineEdit.Password)
        self.register_confirm_password.setPlaceholderText("Re-enter your password")
        self.register_confirm_password.returnPressed.connect(self.handle_register)
        layout.addWidget(self.register_confirm_password)
        
        # Register button
        self.register_button = QPushButton("Create Account")
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setMinimumHeight(45)
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def handle_login(self):
        """Handle login"""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        try:
            self.login_button.setEnabled(False)
            self.login_button.setText("Signing in...")
            
            self.api_client.login(username, password)
            
            QMessageBox.information(self, "Success", "Login successful!")
            self.login_success.emit()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
        finally:
            self.login_button.setEnabled(True)
            self.login_button.setText("Sign In")
    
    def handle_register(self):
        """Handle registration"""
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text()
        confirm_password = self.register_confirm_password.text()
        first_name = self.register_first_name.text().strip()
        last_name = self.register_last_name.text().strip()
        
        # Validation
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all required fields")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return
        
        try:
            self.register_button.setEnabled(False)
            self.register_button.setText("Creating account...")
            
            self.api_client.register(username, email, password, first_name, last_name)
            
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.login_success.emit()
            
        except Exception as e:
            error_msg = str(e)
            if "username" in error_msg.lower():
                error_msg = "Username already exists"
            elif "email" in error_msg.lower():
                error_msg = "Email already exists"
            QMessageBox.critical(self, "Error", f"Registration failed: {error_msg}")
        finally:
            self.register_button.setEnabled(True)
            self.register_button.setText("Create Account")
    
    def clear_form(self):
        """Clear all form fields"""
        self.login_username.clear()
        self.login_password.clear()
        self.register_username.clear()
        self.register_email.clear()
        self.register_password.clear()
        self.register_confirm_password.clear()
        self.register_first_name.clear()
        self.register_last_name.clear()
        self.tab_widget.setCurrentIndex(0)
