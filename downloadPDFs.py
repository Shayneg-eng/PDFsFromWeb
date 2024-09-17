import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class DownloadThread(QThread):
    update_progress = pyqtSignal(int)
    update_status = pyqtSignal(str)

    def __init__(self, urls, folder):
        super().__init__()
        self.urls = urls
        self.folder = folder

    def run(self):
        for i, url in enumerate(self.urls):
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
                    filename = os.path.join(self.folder, f"pdf_{i+1}.pdf")
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    self.update_status.emit(f"Downloaded: {filename}")
                else:
                    self.update_status.emit(f"Skipped: {url} (Not a valid PDF)")
            except Exception as e:
                self.update_status.emit(f"Error downloading {url}: {str(e)}")
            self.update_progress.emit((i + 1) * 100 // len(self.urls))

class PDFDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Downloader')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.download_button = QPushButton("Download PDFs")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        layout.addWidget(self.status_display)

        self.setLayout(layout)

    def start_download(self):
        self.status_display.clear()
        self.progress_bar.setValue(0)

        # Create downloads folder
        download_folder = "pdf_downloads"
        os.makedirs(download_folder, exist_ok=True)

        # Read URLs from the txt file
        try:
            with open('pdf_links.txt', 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.status_display.append("Error: pdf_links.txt not found.")
            return

        self.download_thread = DownloadThread(urls, download_folder)
        self.download_thread.update_progress.connect(self.update_progress)
        self.download_thread.update_status.connect(self.update_status)
        self.download_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.status_display.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFDownloader()
    ex.show()
    sys.exit(app.exec_())