import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel)
from finance import valid_ticker, get_stock_data
from ai import get_ai_analysis

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
        
        self.result_display.clear()
        self.status_label.setText("Loading...")
        self.analyze_btn.setEnabled(False)
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

