import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLineEdit, QProgressBar, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import ollama
import time
import os
import PyPDF2
from io import BytesIO

topics = [
    "The role of non-governmental organizations (NGOs) in the Israel-Palestine conflict",
    "History of United States economics",
    "U.S. Gross Domestic Product (GDP) explanation",
    "Components of U.S. GDP",
    "U.S. economic indicators",
    "Unemployment rate in the United States",
    "Inflation rate in the United States",
    "Consumer Price Index (CPI) U.S.",
    "Producer Price Index (PPI) U.S.",
    "U.S. Federal Reserve System",
    "Role of the Federal Reserve",
    "Federal Open Market Committee (FOMC)",
    "U.S. monetary policy",
    "Fiscal policy in the United States",
    "U.S. budget deficit",
]

class PDFSearchThread(QThread):
    update_progress = pyqtSignal(int)
    update_result = pyqtSignal(list)

    def __init__(self, topics):
        super().__init__()
        self.topics = topics

    def run(self):
        all_pdfs = []
        for i, topic in enumerate(self.topics):
            self.update_progress.emit((i + 1) * 100 // len(self.topics))
            print(f"Searching for topic {i+1}/{len(self.topics)}: {topic}")
            query = f"{topic} filetype:pdf"
            urls = list(search(query, num=5, stop=5, pause=2))
            all_pdfs.extend(urls)
        self.update_result.emit(all_pdfs)

class PDFSearchAI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Search AI')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.search_button = QPushButton("Search PDFs")
        self.search_button.clicked.connect(self.start_search)
        layout.addWidget(self.search_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def start_search(self):
        self.result_display.clear()
        self.progress_bar.setValue(0)
        self.search_thread = PDFSearchThread(topics)
        self.search_thread.update_progress.connect(self.update_progress)
        self.search_thread.update_result.connect(self.display_result)
        self.search_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def display_result(self, all_pdfs):
        with open('pdf_links.txt', 'w') as f:
            for url in all_pdfs:
                f.write(f"{url}\n")
        self.result_display.append(f"PDF links have been saved to pdf_links.txt")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFSearchAI()
    ex.show()
    sys.exit(app.exec_())