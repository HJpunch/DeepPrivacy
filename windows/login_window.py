from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMainWindow, QGroupBox
from PyQt6 import QtWidgets

from windows.basic_window import BasicWindow


class LoginWindow(BasicWindow):
    def __init__(self):
        super().__init__()

        # define layout
        login_layout = QVBoxLayout()
        login_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # define widgets
        login_group = QGroupBox()
        login_group.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        username = QLineEdit()
        username.setMaximumWidth(400)

        password = QLineEdit()
        password.setMaximumWidth(400)

        login_btn = QPushButton()
        login_btn.setMaximumWidth(100)
        login_btn.setText("Login")
        login_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        login_label = QLabel("Login")
        font = login_label.font()
        font.setPointSize(20)
        font.setBold(True)
        login_label.setFont(font)
        login_layout.addWidget(login_label)

        login_layout.addWidget(QLabel("\nUsername"))
        login_layout.addWidget(username)
        login_layout.addWidget(QLabel("Password"))
        login_layout.addWidget(password)
        login_layout.addWidget(login_btn)

        login_group.setLayout(login_layout)

        # add margin between DeepPrivacy logo and login block
        self.basic_layout.addStretch(0)
        self.basic_layout.addWidget(login_group)
        self.basic_layout.addStretch(0)


    def resizeEvent(self, event):
        # self.login_group.resize(150, 80)
        super().resizeEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()

    app.exec()