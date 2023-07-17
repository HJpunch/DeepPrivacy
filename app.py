import sys
from PyQt6.QtWidgets import QApplication
from windows.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(ip='192.168.1.230', port=18400)
    window.show()

    app.exec()