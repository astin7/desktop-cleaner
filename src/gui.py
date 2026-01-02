import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit,
                               QFrame)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QFont, QIcon
from src.watcher import DesktopWatcher
from src.optimizer import SystemOptimizer 

class WatcherThread(QThread):
    log_signal = Signal(str)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.watcher = None

    def run(self):
        self.watcher = DesktopWatcher(self.folder_path, logger_func=self.log_signal.emit)
        self.watcher.start()
        # Keep thread alive
        while not self.isInterruptionRequested():
            self.msleep(500)
        self.watcher.stop()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Desktop Cleaner")
        self.setMinimumSize(900, 600)
        
        # State
        self.folder_path = Path.home() / "Desktop" / "Cleaner_Test_Zone"
        self.worker_thread = None
        self.optimizer = SystemOptimizer() # Initialize the Speed Up Engine

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)

        title_label = QLabel("Desktop Cleaner\nV1")
        title_label.setObjectName("sidebarTitle")
        title_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title_label)

        # Nav Buttons
        self.nav_btns = []
        nav_items = ["Care", "Speed Up", "Protect", "Software Updater", "Action Center"]
        
        for item in nav_items:
            btn = QPushButton(item)
            btn.setObjectName("navButton")
            btn.setCheckable(True)
            btn.setFixedHeight(60)
            
            # Connect the buttons to swap pages
            if item == "Speed Up":
                btn.clicked.connect(self.show_speed_up_page)
            elif item == "Care":
                btn.clicked.connect(self.show_home_page)
            
            sidebar_layout.addWidget(btn)
            self.nav_btns.append(btn)
            
        self.nav_btns[0].setChecked(True) # Set "Care" as active by default

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # --- MAIN CONTENT ---
        content_area = QFrame()
        content_area.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(40, 40, 40, 40)

        # Header
        header_layout = QHBoxLayout()
        self.status_label = QLabel(f"Watching: {self.folder_path.name}")
        self.status_label.setObjectName("headerLabel")
        header_layout.addWidget(self.status_label)
        header_layout.addStretch()
        
        self.btn_select = QPushButton("Select Folder")
        self.btn_select.setObjectName("secondaryButton")
        self.btn_select.clicked.connect(self.select_folder)
        header_layout.addWidget(self.btn_select)
        content_layout.addLayout(header_layout)

        # Central Button Section
        scan_layout = QVBoxLayout()
        scan_layout.setAlignment(Qt.AlignCenter)
        
        self.scan_btn = QPushButton("SCAN")
        self.scan_btn.setObjectName("scanButton")
        self.scan_btn.setFixedSize(200, 200)
        self.scan_btn.setCheckable(True)
        # Default connection is to the Cleaner
        self.scan_btn.clicked.connect(self.toggle_cleaning)
        
        scan_layout.addWidget(self.scan_btn)
        content_layout.addLayout(scan_layout)
        
        # Log Window
        self.log_window = QTextEdit()
        self.log_window.setObjectName("logWindow")
        self.log_window.setReadOnly(True)
        self.log_window.setMaximumHeight(150)
        self.log_window.append("System Ready...")
        content_layout.addWidget(self.log_window)

        main_layout.addWidget(content_area)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e2233; }
            QLabel { color: #ffffff; font-family: 'Segoe UI', sans-serif; }
            
            #sidebar { background-color: #2a2f45; min-width: 220px; max-width: 220px; }
            #sidebarTitle { font-size: 16px; font-weight: bold; margin-bottom: 20px; color: #6a7392; }
            
            #navButton {
                background-color: transparent; color: #a4aabf; text-align: left; padding-left: 30px;
                font-size: 14px; border: none; border-left: 4px solid transparent;
            }
            #navButton:checked { background-color: #1e2233; color: #ffffff; border-left: 4px solid #007bff; }
            #navButton:hover:!checked { background-color: #353b54; }
            
            #contentArea { background-color: #1e2233; }
            #headerLabel { font-size: 18px; font-weight: bold; }
            
            #secondaryButton {
                background-color: #353b54; color: white; border: 1px solid #4a516b;
                border-radius: 15px; padding: 8px 15px; font-weight: bold;
            }
            #secondaryButton:hover { background-color: #4a516b; }
            
            #scanButton {
                background-color: qradialgradient(cx:0.5, cy:0.5, radius: 0.5, fx:0.5, fy:0.5, stop:0 #007bff, stop:1 #0056b3);
                color: white; font-size: 28px; font-weight: bold;
                border-radius: 100px; border: 8px solid #151925;
            }
            #scanButton:checked {
                background-color: qradialgradient(cx:0.5, cy:0.5, radius: 0.5, fx:0.5, fy:0.5, stop:0 #dc3545, stop:1 #a71d2a);
                border: 8px solid #2a1515;
            }
            #scanButton:hover { background-color: qradialgradient(cx:0.5, cy:0.5, radius: 0.5, fx:0.5, fy:0.5, stop:0 #008bff, stop:1 #0066c3); }
            
            #logWindow {
                background-color: #151925; color: #00ff00; font-family: 'Courier New';
                border: 1px solid #2a2f45; border-radius: 10px; padding: 10px;
            }
        """)

    # --- PAGE LOGIC ---
    def show_speed_up_page(self):
        """Switches the UI to Speed Up Mode"""
        # Update Sidebar
        for btn in self.nav_btns: btn.setChecked(False)
        self.nav_btns[1].setChecked(True) # Index 1 is Speed Up

        # Update Stats & UI
        stats = self.optimizer.get_system_stats()
        self.status_label.setText(f"System Status: {stats}")
        self.scan_btn.setText("BOOST")
        self.scan_btn.setChecked(False) # Reset button state
        
        # Rewire Button
        try: self.scan_btn.clicked.disconnect() 
        except: pass
        self.scan_btn.clicked.connect(self.perform_boost)
        
        self.log_window.append("--- Switched to Optimization Mode ---")

    def show_home_page(self):
        """Switches the UI back to File Cleaner Mode"""
        # Update Sidebar
        for btn in self.nav_btns: btn.setChecked(False)
        self.nav_btns[0].setChecked(True) # Index 0 is Care

        # Update UI
        self.status_label.setText(f"Watching: {self.folder_path.name}")
        self.scan_btn.setText("SCAN")
        self.scan_btn.setChecked(False)

        # Rewire Button
        try: self.scan_btn.clicked.disconnect() 
        except: pass
        self.scan_btn.clicked.connect(self.toggle_cleaning)
        
        self.log_window.append("--- Switched to Desktop Care Mode ---")

    # --- FUNCTIONALITY ---
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Watch")
        if folder:
            self.folder_path = Path(folder)
            self.status_label.setText(f"Watching: {self.folder_path.name}")
            self.log_window.append(f"Target changed to: {self.folder_path}")

    def update_log(self, message):
        self.log_window.append(message)
        scrollbar = self.log_window.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def perform_boost(self):
        """Runs the System Speed Up"""
        self.log_window.append("--- 🚀 Starting Speed Up Optimization ---")
        self.scan_btn.setChecked(True) # Keep it pressed visually
        QApplication.processEvents()   # Force UI update so it doesn't freeze
        
        # Run Cleaning
        result = self.optimizer.run_speed_up()
        self.log_window.append(result)
        
        # Refresh Stats
        new_stats = self.optimizer.get_system_stats()
        self.status_label.setText(f"System Status: {new_stats}")
        
        self.scan_btn.setChecked(False) # Release button

    def toggle_cleaning(self, checked):
        """Toggles the AI Desktop Watcher"""
        if checked:
            self.scan_btn.setText("STOP")
            self.log_window.append("--- AI Service Started ---")
            self.worker_thread = WatcherThread(self.folder_path)
            self.worker_thread.log_signal.connect(self.update_log)
            self.worker_thread.start()
        else:
            self.scan_btn.setText("SCAN")
            self.log_window.append("--- Stopping... ---")
            if self.worker_thread:
                self.worker_thread.requestInterruption()
                self.worker_thread.wait()
                self.worker_thread = None
                self.log_window.append("--- Service Stopped ---")