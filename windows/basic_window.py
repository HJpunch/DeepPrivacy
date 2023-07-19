#-*-coding:utf-8-*-
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea
from PyQt6.QtGui import QPixmap

ASSET = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/asset"
# ASSET = os.path.abspath(os.path.pardir) + "/asset"
ICONS_DIR = ASSET + "/icons/"


class BasicWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DeepPrivacy")
        self.resize(820, 640)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.basic_widget = QWidget()
        self.basic_layout = QVBoxLayout()
        # self.basic_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        self.logo = QLabel()
        # self.logo.setMinimumSize(1,1)
        self.logo_image = QPixmap(ASSET + "/templates/DeepPrivacy_Dark.png")
        self.logo.setPixmap(self.logo_image)
        self.basic_layout.addWidget(self.logo)

        self.basic_widget.setLayout(self.basic_layout)
        # self.setCentralWidget(self.basic_widget)

        scroll_area.setWidget(self.basic_widget)
        self.setCentralWidget(scroll_area)

    def resizeEvent(self, event):
        width = self.width() if self.width() <= self.logo_image.width() else self.logo_image.width()
        height = self.height() if self.height() <= self.logo_image.height() else self.logo_image.height()

        self.logo.setPixmap(self.logo_image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.basic_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        super().resizeEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = BasicWindow()
    window.show()

    app.exec()
