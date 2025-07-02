import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.config import load_theme
from dotenv import load_dotenv

load_dotenv()

def main():
    app = QApplication(sys.argv)

    load_theme(app, mode="colorful")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
