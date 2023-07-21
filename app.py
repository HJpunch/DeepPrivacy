import sys
from PyQt6.QtWidgets import QApplication
from windows.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(ip='192.168.1.230', port=18400)
    window.show()

    app.exec()


r"""
TODO
1. 영상 인식 결과에서 DB 내 이미지 보이는 방법
   각 비디오 내에서 앞에서 5개 이미지만 끊어서 static 내에 cp 후 get해오기?
"""