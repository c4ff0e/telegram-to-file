import sys
import os
import subprocess
import datetime
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal, QObject, QSettings


class LogSignal(QObject):
    log_signal = pyqtSignal(str) # потокобезопасность

class BotGUI(QMainWindow):
    
    def __init__(self):
        self.bot_process = None
        super().__init__()
        
        self.settings = QSettings("TelegramToMd", "BotLauncher") #сохранение токена между запусками
        token = self.settings.value("token")
        
        self.log_emitter = LogSignal()
        self.log_emitter.log_signal.connect(self.on_log)
        self.init_ui()
        
        if token:
            self.token_input.setText(token) #вставить если существует
        
    def init_ui(self):
        self.setWindowTitle("Telegram to .md bot launcher")
        self.setGeometry(500, 500, 700, 500)
        
        label = QLabel("BOT_TOKEN:")
        self.token_input = QLineEdit()
        self.start_button = QPushButton("Start", enabled=True)
        self.stop_button = QPushButton("Stop", enabled=False)
        self.log_window = QTextEdit()
    
        central_widget = QWidget(self)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.token_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.log_window)
        
        self.start_button.clicked.connect(self.start_clicked)
        self.stop_button.clicked.connect(self.stop_clicked)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_token(self):
        self.settings.setValue("token", self.token_input.text())
    
    def on_log(self, text):
        self.log_window.append(text)

    def read_logs(self):
        while self.bot_process:
            line = self.bot_process.stdout.readline()
            if line:
                self.log_emitter.log_signal.emit(line.strip())
        
    def start_clicked(self):
        self.log_window.append(f"Started {[datetime.datetime.now().strftime('%H:%M:%S')]}")
        env = os.environ.copy()
        python_path = sys.executable
        env["BOT_TOKEN"] = self.token_input.text()
        
        self.bot_process = subprocess.Popen([python_path, "bot_main.py"], env = env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
        
        thread = threading.Thread(target=self.read_logs, daemon=True) # отдельный тред для чтения логов(васянство!)
        thread.start()
        self.save_token()
        
        time.sleep(0.5)
        if self.bot_process.poll() is None:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.log_window.append(f"Error: {self.bot_process.poll()}")
        
    def stop_clicked(self): 
        self.log_window.append(f"Stopped {[datetime.datetime.now().strftime('%H:%M:%S')]}")
        if self.bot_process:
            self.bot_process.kill() # чтобы наверняка
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
            
    def closeEvent(self, event): # вызывается при закрытии окна
        if self.bot_process:
            self.bot_process.kill()
            self.bot_process.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotGUI()
    window.show()
    sys.exit(app.exec_())