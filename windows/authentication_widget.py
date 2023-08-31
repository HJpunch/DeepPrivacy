import requests

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QLineEdit, \
    QPushButton, QGroupBox, QDialog, QDialogButtonBox, QMessageBox, QSizePolicy

from utils.utility_widget import QConnectionErrorMessage, QLoginErrorMessage
from utils.HTTP_request import check_server_status


class LoginWidget(QGroupBox):
    # loginSignal = pyqtSignal(dict)
    loginSignal = pyqtSignal(str)
    def __init__(self, url):
        super().__init__()
        self.url = url
        
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.userid = QLineEdit()
        self.userid.setMaximumWidth(400)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setMaximumWidth(400)
        self.password.returnPressed.connect(self.send_login_form)

        login_btn = QPushButton()
        login_btn.setMaximumWidth(100)
        login_btn.setText("Login")
        login_btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        join_btn = QPushButton()
        join_btn.setMaximumWidth(100)
        join_btn.setText("Join")
        join_btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        login_label = QLabel("Login")
        font = login_label.font()
        font.setPointSize(20)
        font.setBold(True)
        login_label.setFont(font)

        self.layout().addStretch(0)

        self.layout().addWidget(login_label)
        self.layout().addWidget(QLabel("\nUserid"))
        self.layout().addWidget(self.userid)
        self.layout().addWidget(QLabel("Password"))
        self.layout().addWidget(self.password)
        self.layout().addWidget(login_btn)
        self.layout().addWidget(join_btn)

        login_btn.clicked.connect(self.send_login_form)
        join_btn.clicked.connect(self.show_join_form)

        self.layout().addStretch(0)

    def send_login_form(self):
        if not check_server_status(self.url):
            QConnectionErrorMessage(parent=self, url=self.url).exec()
            return

        userid = self.userid.text()
        password = self.password.text()
        login_form = dict(userid=userid, password=password)
        response = requests.post(url=f"{self.url}/login", data=login_form)

        if response.status_code == 200:
            status = response.json()['status']
            login_type = response.json()['login_type']
            
            if status and login_type == 'user':
                self.userid.clear()
                self.password.clear()
                self.loginSignal.emit(userid)

            elif status and login_type == 'admin':
                self.userid.clear()
                self.password.clear()
                self.loginSignal.emit('admin')
                
            else:  # id o, pw x
                QLoginErrorMessage(parent=self, error='password').exec()
                self.password.clear()
                return
        else:  # id x
            QLoginErrorMessage(parent=self, error='userid').exec()
            self.password.clear()
            return

    def show_join_form(self):
        JoinDialog(parent=self, url=self.url).exec()


class JoinDialog(QDialog):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.url = url
        self.setWindowTitle("DeepPrivacy Join Foam")
        layout = QGridLayout()

        button = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(button)

        self.userid = QLineEdit()
        self.userid.setPlaceholderText("String of 16 characters or less")

        self.email = QLineEdit()
        self.email.setPlaceholderText("String of 32 characters of less")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("String of 16 characters of less")
        
        self.re_password = QLineEdit()
        self.re_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.re_password.setPlaceholderText("Enter password one more time")

        layout.addWidget(QLabel("Email: "), 0, 0)
        layout.addWidget(self.email, 0, 1)
        layout.addWidget(QLabel("ID: "), 1, 0)
        layout.addWidget(self.userid, 1, 1)
        layout.addWidget(QLabel("Password: "), 2, 0)
        layout.addWidget(self.password, 2, 1)
        layout.addWidget(QLabel("Repeat Password: "), 3, 0)
        layout.addWidget(self.re_password, 3, 1)
        layout.addWidget(button_box, 4, 1)

        button_box.accepted.connect(self.send_join_foam)
        button_box.rejected.connect(self.close_dialog)
        self.setLayout(layout)

    def send_join_foam(self):
        userid = self.userid.text()
        email = self.email.text()
        password = self.password.text()
        re_password = self.re_password.text()

        foam = dict(userid=userid, email=email, password=password, re_password=re_password)
        response = requests.post(url=f"{self.url}/register", data=foam)

        if response.status_code == 200:
            result = response.json()['result']
            message = response.json()['message']

            if result:
                dialog = QMessageBox(self)
                dialog.setWindowTitle("Registration Success")
                dialog.setText(message)
                dialog.setIcon(QMessageBox.Icon.Information)
                dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
                button = dialog.exec()
                if button:
                    self.close()

            else:
                dialog = QMessageBox(self)
                dialog.setWindowTitle("Registration Failure")
                dialog.setText(message)
                dialog.setIcon(QMessageBox.Icon.Warning)
                dialog.setStandardButtons(QMessageBox.StandardButton.Close)
                dialog.exec()

        else:
            QConnectionErrorMessage(parent=self, url=self.url).exec()
            return
        
    def close_dialog(self):
        super().reject()
        

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LoginWidget()
    window.show()

    app.exec()