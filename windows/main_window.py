# # -*- coding: utf-8 -*-
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from PyQt6.QtWidgets import QToolBar, QStackedWidget
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtCore import Qt

from basic_window import BasicWindow, ASSET
from function_widgets import ImageDetectionWidget, VideoDetectionWidget, VideoRecognitionWidget


ICONS_DIR = ASSET + "/icons/"

def newIcon(icon:str) -> QIcon:
    return QIcon(ICONS_DIR + icon)


class MainWindow(BasicWindow):
    # function_index = {"Image\nDetection": 0, "Video\n"}
    def __init__(self):
        super().__init__()

        # define actions
        self.image_detection = self.action(name="Image\nDetection", icon="image_detection.svg")
        self.image_detection.setCheckable(True)
        self.video_detection = self.action(name="Video\nDetection", icon="video_detection.svg")
        self.video_detection.setCheckable(True)
        self.video_recognition = self.action(name="Video\nRecognition", icon="video_detection.svg")
        self.video_recognition.setCheckable(True)

        # create toolbar
        toolbar = QToolBar("Tool Bar")
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)
        toolbar.addAction(self.image_detection)
        toolbar.addAction(self.video_detection)
        toolbar.addAction(self.video_recognition)

        # define action group
        self.action_group = QActionGroup(toolbar)
        self.action_group.addAction(self.image_detection)
        self.action_group.addAction(self.video_detection)
        self.action_group.addAction(self.video_recognition)
        self.action_group.setExclusive(True)
        self.action_group.triggered.connect(self.change_mode)

        # add widgets
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(ImageDetectionWidget())
        self.stacked_widget.addWidget(VideoDetectionWidget())
        self.stacked_widget.addWidget(VideoRecognitionWidget())
        self.basic_layout.addWidget(self.stacked_widget)

    def action(self, name:str, icon:str=None, shortcut:str=None, tip:str=None) -> QAction:
        if icon:
            action = QAction(newIcon(icon), name, self)
        else:
            action = QAction(name, self)

        action.setObjectName(name)

        if shortcut:
            action.setShortcut(shortcut)
        if tip:
            action.setStatusTip(tip)

        return action

    def change_mode(self, action):
        action_list = self.action_group.actions()
        index = action_list.index(action)
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
