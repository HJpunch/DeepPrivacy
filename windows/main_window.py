import requests

from PyQt6.QtWidgets import QToolBar, QStackedWidget
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtCore import Qt, QCoreApplication

from windows.basic_window import BasicWindow, ICONS_DIR
from windows.login_widget import LoginWidget
from windows.function_widgets import ImageDetectionWidget, VideoDetectionWidget, VideoRecognitionWidget
from utils.utility_widget import QLoginErrorMessage

def newIcon(icon:str) -> QIcon:
    return QIcon(ICONS_DIR + icon)


class MainWindow(BasicWindow):
    # function_index = {"Image\nDetection": 0, "Video\n"}
    def __init__(self, ip:str, port:int):
        super().__init__()
        self.url = f"http://{ip}:{port}"
        self.login = LoginWidget(self.url)

        self.image_detection_widget = ImageDetectionWidget(self.url)
        self.video_detection_widget = VideoDetectionWidget(self.url)
        self.video_recognition_widget = VideoRecognitionWidget(self.url)

        # define actions
        self.image_detection_act = self.action(name="Image\nDetection", icon="image_detection.svg")
        self.image_detection_act.setCheckable(True)
        self.video_detection_act = self.action(name="Video\nDetection", icon="video_detection.svg")
        self.video_detection_act.setCheckable(True)
        self.video_recognition_act = self.action(name="Video\nRecognition", icon="video_detection.svg")
        self.video_recognition_act.setCheckable(True)

        self.app_logout = self.action("Logout", icon="logout.svg", tip="Logout")
        self.app_logout.triggered.connect(self.try_logout)
        self.app_logout.setDisabled(True)
        app_quit = self.action("Quit", icon="quit.svg", shortcut="Ctrl+q", tip="Quit Application")
        app_quit.triggered.connect(QCoreApplication.instance().quit)

        # create toolbar
        toolbar = QToolBar("Tool Bar")
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)
        toolbar.addAction(self.image_detection_act)
        toolbar.addAction(self.video_detection_act)
        toolbar.addAction(self.video_recognition_act)
        toolbar.addSeparator()
        toolbar.addAction(self.app_logout)
        toolbar.addAction(app_quit)

        # define action group
        self.action_group = QActionGroup(toolbar)
        self.action_group.addAction(self.image_detection_act)
        self.action_group.addAction(self.video_detection_act)
        self.action_group.addAction(self.video_recognition_act)
        self.action_group.setExclusive(True)
        self.action_group.triggered.connect(self.change_mode)
        self.action_group.setDisabled(True)  # disable until login
        # self.image_detection.setChecked(True)

        # add widgets
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.image_detection_widget)
        self.stacked_widget.addWidget(self.video_detection_widget)
        self.stacked_widget.addWidget(self.video_recognition_widget)
        self.stacked_widget.addWidget(self.login)
        self.stacked_widget.setCurrentIndex(3)  # set login widget for default
        self.basic_layout.addWidget(self.stacked_widget)

        self.login.loginSignal.connect(self.try_login)

        function_widget_list = [self.image_detection_widget,
                                self.video_detection_widget,
                                self.video_recognition_widget]
        for widget in function_widget_list:
            widget.logoutSignal.connect(self.try_logout)


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

    def try_login(self, login_form):
        response = requests.post(url=f"{self.url}/login", data=login_form)
        
        if response.status_code == 200:
            result = response.json()['result']
            if result:
                self.app_logout.setEnabled(True)
                self.action_group.setEnabled(True)
                self.image_detection_act.setChecked(True)
                self.stacked_widget.setCurrentIndex(0)
            else:  # id o, pw x
                QLoginErrorMessage(parent=self, error='password').exec()
                return

        else:  # id x
            QLoginErrorMessage(parent=self, error='userid').exec()
            return

    def try_logout(self):
        response = requests.get(url=f"{self.url}/logout")
        result = response.json()['result']
        if result:  # 로그인화면으로
            pre_widget = self.stacked_widget.currentWidget()
            pre_index = self.stacked_widget.currentIndex()
            pre_widget.upload_widget.clear()

            self.stacked_widget.setCurrentIndex(3)
            self.stacked_widget.setCurrentIndex(pre_index)
            self.stacked_widget.setCurrentIndex(3)

            self.app_logout.setDisabled(True)
            self.action_group.setDisabled(True)
        

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow(ip='192.168.1.230', port=18400)
    window.show()

    app.exec()
