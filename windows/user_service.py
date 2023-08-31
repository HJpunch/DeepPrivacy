import os

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QLineEdit, QLabel, QWidget, QMessageBox, QPushButton,\
                            QGridLayout, QVBoxLayout
from PyQt6.QtGui import QIntValidator

from windows.basic_window import newIcon
from windows.function_widgets import DefaultWidget
from utils.utility_widget import remove_all_widgets, QConnectionErrorMessage, QResultDisplayWidget, QDownloadButton
from utils.HTTP_request import post_file, read_file, get_file


class PrivacyRegisterDialog(QDialog):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.url = url
        self.setWindowTitle("Privacy Register Foam")
        layout = QGridLayout()

        button = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(button)

        self.phone_num = QLineEdit()
        self.phone_num.setValidator(QIntValidator(self))
        self.resident_num_1 = QLineEdit()
        self.resident_num_1.setValidator(QIntValidator(self))
        self.resident_num_2 = QLineEdit()
        self.resident_num_2.setValidator(QIntValidator(self))
        self.resident_num_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.driver_num = QLineEdit()
        self.car_num = QLineEdit()
        self.face = QLineEdit()
        self.face.setPlaceholderText("Enter File Directory")

        self.privacy_list = [self.phone_num, self.resident_num_1, self.resident_num_2, \
                             self.driver_num, self.car_num, self.face]

        self.file_select = QPushButton()
        self.file_select.setIcon(newIcon("folder-search-result"))
        self.file_select.clicked.connect(self.file_dialog_open)

        layout.addWidget(QLabel("Phone Number(without '-'): "), 0, 0)
        layout.addWidget(self.phone_num, 0, 1)
        layout.addWidget(QLabel("Resident Number: "), 1, 0)
        layout.addWidget(self.resident_num_1, 1, 1)
        layout.addWidget(QLabel("-"), 1, 2)
        layout.addWidget(self.resident_num_2, 1, 3)
        layout.addWidget(QLabel("Driver Number: "), 2, 0)
        layout.addWidget(self.driver_num, 2, 1)
        layout.addWidget(QLabel("Car Number: "), 3, 0)
        layout.addWidget(self.car_num, 3, 1)
        layout.addWidget(QLabel("Face Shot"), 4, 0)
        layout.addWidget(self.face, 4, 1)
        layout.addWidget(self.file_select, 4, 2)
        layout.addWidget(button_box, 5, 1)

        button_box.accepted.connect(self.send_foam)
        button_box.rejected.connect(self.close_dialog)
        self.setLayout(layout)

    def set_userid(self, userid):
        self.userid = userid

    def send_foam(self):
        userid = self.userid
        phone_num = self.phone_num.text()
        resident_num = self.resident_num_1.text() + self.resident_num_2.text()
        driver_num = self.driver_num.text()
        car_num = self.car_num.text()
        face_shot = self.face.text()

        foam = dict(userid=userid, phone_num=phone_num, resident_num=resident_num, \
                    driver_num=driver_num, car_num=car_num)
        
        filter_foam = dict()
        for key, value in foam.items():
            if value:
                filter_foam[key] = value

        if face_shot:
            face_shot = read_file(face_shot)

        try:
            response = post_file(url=f"{self.url}/register/privacy", files=face_shot, data=filter_foam)
        except ValueError:
            QConnectionErrorMessage(parent=self, url=self.url).exec()
            return
        else:
            result = response['result']
            message = response['message']

        if result:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Success")
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

    def file_dialog_open(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image File", ".",
                                                  "Video File(*.jpg)")

        if filename != "":
            self.face.setText(filename)

    def close_dialog(self):
        for privacy in self.privacy_list:
            privacy.clear()
        super().reject()


class PrivacyDetectWidget(QWidget):
    def __init__(self, url:str):
        super().__init__()
        self.url = url
        self.box = QVBoxLayout()
        self.setLayout(self.box)

    def set_userid(self, userid):
        self.userid = userid

    def detect_privacy(self):
        url = f"{self.url}/detect/privacy"
        data = dict(userid=self.userid)

        try:
            result = post_file(url=url, data=data)
        except ValueError:
            QConnectionErrorMessage(parent=self, url=self.url).exec()
            return
        else:
            self.show_result(result)

    def show_result(self, result:dict):
        # 결과 None이면 그냥 dialog로 띄우기
        for key, value in result.items():
            video_file_name = os.path.basename(key)
            video_url = f"f{self.url}/{key}"

            result_widget = QResultDisplayWidget(title=f"video: {video_file_name}")
            self.box.addWidget(result_widget)

            download_button = QDownloadButton("Download Video")
            download_button.set_url(video_url)
            result_widget.layout().addWidget(download_button, 0, 0)

            for i, (crop, conf) in enumerate(value):
                crop_url = f"{self.url}/{crop}"
                crop_img = get_file(crop_url)
                result_widget.add_image(data=crop_img, row=i+1, col=0)
                result_widget.add_label(data=f"{100*conf:.2f}", row=i+1, col=1)
                
    def clear(self):
        remove_all_widgets(self.box)