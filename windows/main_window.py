from PyQt6 import QtGui
import requests

from PyQt6.QtWidgets import QToolBar, QStackedWidget, QLabel
from PyQt6.QtGui import QIcon, QAction, QActionGroup, QPixmap
from PyQt6.QtCore import Qt, QCoreApplication

from windows.basic_window import BasicWindow, ICONS_DIR
from windows.login_widget import LoginWidget
from windows.function_widgets import ImageDetectionWidget, VideoDetectionWidget, VideoRecognitionWidget, PornRecognitionWidget, \
                                     VideoAnalysisWidget

def newIcon(icon:str) -> QIcon:
    return QIcon(ICONS_DIR + icon)


class MainWindow(BasicWindow):
    def __init__(self, ip:str, port:int):
        super().__init__()
        self.url = f"http://{ip}:{port}"
        self.login_widget = LoginWidget(self.url)
        self.login_widget.loginSignal.connect(self.try_login)
        self.login_status = False

        # define user widget object
        self.image_detection_widget = ImageDetectionWidget(self.url)
        self.video_detection_widget = VideoDetectionWidget(self.url)
        self.video_recognition_widget = VideoRecognitionWidget(self.url)
        self.porn_recognition_widget = PornRecognitionWidget(self.url)

        # define admin widget object
        self.video_analysis_widget = VideoAnalysisWidget(self.url)

        # define user actions
        self.image_detection_act = self.action(name="Image\nDetection", icon="image_detection.svg")
        self.image_detection_act.setCheckable(True)
        self.video_detection_act = self.action(name="Video\nDetection", icon="video_detection.svg")
        self.video_detection_act.setCheckable(True)
        self.video_recognition_act = self.action(name="Video\nRecognition", icon="video_detection.svg")
        self.video_recognition_act.setCheckable(True)
        self.porn_recognition_act = self.action(name="Porn\nRecognition", icon="video_detection.svg")
        self.porn_recognition_act.setCheckable(True)

        # define admin actions
        self.video_analysis_act = self.action(name="Video\nAnalysis", icon="video_detection.svg")
        self.video_analysis_act.setCheckable(True)
        self.video_analysis_act.setVisible(False)

        # define general actions
        self.app_logout = self.action("Logout", icon="logout.svg", tip="Logout")
        self.app_logout.triggered.connect(self.try_logout)
        self.app_logout.setDisabled(True)
        self.app_quit = self.action("Quit", icon="quit.svg", shortcut="Ctrl+q", tip="Quit Application")
        self.app_quit.triggered.connect(self.quit)

        # create toolbar
        self.toolbar = QToolBar("Tool Bar")
        self.toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.toolbar.addAction(self.image_detection_act)
        self.toolbar.addAction(self.video_detection_act)
        self.toolbar.addAction(self.video_recognition_act)
        self.toolbar.addAction(self.porn_recognition_act)
        self.toolbar.addAction(self.video_analysis_act)  # admin function
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.app_logout)
        self.toolbar.addAction(self.app_quit)
        self.addToolBar(self.toolbar)

        # define action group
        self.action_group = QActionGroup(self.toolbar)
        self.action_group.addAction(self.image_detection_act)
        self.action_group.addAction(self.video_detection_act)
        self.action_group.addAction(self.video_recognition_act)
        self.action_group.addAction(self.porn_recognition_act)
        self.action_group.addAction(self.video_analysis_act)
        self.action_group.setExclusive(True)
        self.action_group.triggered.connect(self.change_mode)
        self.action_group.setDisabled(True)  # disable until login

        # add widgets
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.image_detection_widget)
        self.stacked_widget.addWidget(self.video_detection_widget)
        self.stacked_widget.addWidget(self.video_recognition_widget)
        self.stacked_widget.addWidget(self.porn_recognition_widget)
        self.stacked_widget.addWidget(self.video_analysis_widget)
        self.stacked_widget.addWidget(self.login_widget)  # login widget is always at last order of stacked widget
        self.stacked_widget.setCurrentIndex(self.stacked_widget.count()-1)  # set login widget for default
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
        checked_action = self.action_group.checkedAction()

        pre_widget = self.stacked_widget.currentWidget()
        pre_index = self.stacked_widget.currentIndex()
        post_index = action_list.index(checked_action)

        if pre_index != post_index:
            pre_widget.upload_widget.clear()
            self.stacked_widget.setCurrentIndex(post_index)
            self.stacked_widget.setCurrentIndex(pre_index)
            self.stacked_widget.setCurrentIndex(post_index)

    def try_login(self, signal):
        if signal == 'user' and not self.login_status:
            self.login_status = True
            self.app_logout.setEnabled(True)

            self.action_group.setEnabled(True)
            self.image_detection_act.setChecked(True)
            self.stacked_widget.setCurrentIndex(0)

        elif signal == 'admin' and not self.login_status:
            self.login_status = True
            self.app_logout.setEnabled(True)
            self.toolbar.insertAction(self.app_logout, self.video_analysis_act)

            self.video_analysis_act.setVisible(True)
            self.video_analysis_act.setEnabled(True)
            self.video_analysis_act.setChecked(True)
            self.stacked_widget.setCurrentIndex(4)

    def try_logout(self):
        response = requests.get(url=f"{self.url}/logout")
        result = response.json()['result']
        if result:  # to login widget
            self.login_status = False
            pre_widget = self.stacked_widget.currentWidget()
            pre_index = self.stacked_widget.currentIndex()
            pre_widget.upload_widget.clear()
            self.action_group.checkedAction().setChecked(False)

            self.stacked_widget.setCurrentIndex(self.stacked_widget.count()-1)
            self.stacked_widget.setCurrentIndex(pre_index)
            self.stacked_widget.setCurrentIndex(self.stacked_widget.count()-1)

            self.video_analysis_act.setVisible(False)
            self.app_logout.setDisabled(True)
            self.action_group.setDisabled(True)

            try:
                self.toolbar.removeAction(self.video_analysis_act)
            except:
                pass

            # self.removeToolBar(self.toolbar)
            # self.removeToolBar(self.admin_toolbar)

    def quit(self):
        if self.login_status:
            self.try_logout()
        QCoreApplication.instance().quit()

    def closeEvent(self, event):
        self.quit()
        super().closeEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow(ip='192.168.1.230', port=18400)
    window.show()

    app.exec()
