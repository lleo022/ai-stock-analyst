import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel)
from PyQt5.QtCore import QThread, pyqtSignal
from finance import valid_ticker, get_stock_data
from ai import get_ai_analysis

class Analyzer(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str) 

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        
    def run(self):
        try:
            stock_data = get_stock_data(self.ticker)
            analysis = get_ai_analysis(self.ticker, stock_data)
            self.finished.emit(analysis)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Stock Assistant")
        self.setMinimumSize(600, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input Section
        input_layout = QHBoxLayout()
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("Enter Ticker (e.g., AAPL)")
        self.analyze_btn = QPushButton("Analyze Stock")
        self.analyze_btn.clicked.connect(self.start_analysis)
        
        input_layout.addWidget(self.ticker_input)
        input_layout.addWidget(self.analyze_btn)

        # Output Section
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.status_label = QLabel("Ready")

        layout.addLayout(input_layout)
        layout.addWidget(self.result_display)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def start_analysis(self):
        ticker = self.ticker_input.text().upper().strip()
        
        # Check if input is valid
        valid, msg = valid_ticker(ticker)
        if not valid:
            self.status_label.setText(f"Error: {msg}")
            return
        
        # Loading UI
        self.result_display.clear()
        self.status_label.setText("Loading...")
        self.analyze_btn.setEnabled(False)
        
        # Start the analysis thread in background
        self.worker = Analyzer(ticker)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        
    def on_finished(self, result):
        self.result_display.setText(result)
        self.status_label.setText("Analysis Complete.")
        self.analyze_btn.setEnabled(True)

    def on_error(self, error_msg):
        self.result_display.setText(error_msg)
        self.status_label.setText("API Error")
        self.analyze_btn.setEnabled(True)
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

