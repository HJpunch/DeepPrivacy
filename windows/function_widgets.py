from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QBoxLayout, \
    QLabel, QPushButton, QComboBox, QFileDialog, QListWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Literal

from windows.basic_window import ICONS_DIR
from utils.HTTP_request import read_file, post_file


class FileUploadWidget(QGroupBox):
    resultSignal = pyqtSignal(list)
    def __init__(self, file_type:Literal['image', 'video']):
        super().__init__()
        self.file_type = file_type
        self.threshold = 0.5
        self.url = str()

        self.setTitle("Upload File")
        self.box = QVBoxLayout()
        self.setLayout(self.box)

        self.upload = QWidget()
        self.box.addWidget(self.upload)
        self.upload_box = QHBoxLayout()
        self.upload.setLayout(self.upload_box)
        # self.upload.setMaximumWidth(600)
        # self.upload.setMinimumSize(600, 30)

        # add widgets
        label = QLabel()
        pixmap = QPixmap(ICONS_DIR+"upload.svg")
        pixmap.scaled(20, 20)
        label.setPixmap(pixmap)
        self.upload_box.addWidget(label)

        label = DragAndDrop("Drag and Drop Files Here")
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.upload_box.addWidget(label)

        self.browse_button = QPushButton("Browse Files")
        self.browse_button.setMaximumWidth(100)
        self.browse_button.clicked.connect(self.dialog_open)
        self.upload_box.addWidget(self.browse_button)

        self.file_list = QListWidget()
        self.file_list.setVisible(False)
        self.box.addWidget(self.file_list)
        # self.file_list.model().rowsInserted.connect(self.request)

    def set_url(self, url):
        self.url = url

    def dialog_open(self):
        if self.file_type == "image":
            filter = "Image(*.png *.jpg)"
            file_dialog = QFileDialog.getOpenFileNames
            caption = "Select one or more images to upload"
        elif self.file_type == "video":
            filter = "Video(*.mp4)"
            file_dialog = QFileDialog.getOpenFileName
            caption = "Select video to upload"

        filenames, _ = file_dialog(\
                parent=self, caption=caption, directory=".",\
                filter=filter)
        
        if filenames:
            self.file_list.setVisible(True)
            self.file_list.clear()
            if isinstance(filenames, list):
                for f in filenames:
                    self.file_list.addItem(f)
            else:
                self.file_list.addItem(f)

            upload = read_file(filenames)
            data = {"threshold": self.threshold}
            result = post_file(url=self.url, files=upload, data=data)
            self.resultSignal.emit(result)


class ImageFileUploadWidget(FileUploadWidget):
    def __init__(self):
        super().__init__(file_type="image")
        self.setTitle("Upload Image(s)")

    def dialog_open(self):
        filenames, _ = QFileDialog.getOpenFileNames(\
            self, "Select one or more images to upload", ".", \
                "Image(*.png *.jpg)")
        
        if filenames:
            self.file_list.setVisible(True)
            self.file_list.clear()
            for f in filenames:
                self.file_list.addItem(f)


class VideoFileUploadWidget(FileUploadWidget):
    def __init__(self):
        super().__init__(file_type="video")
        self.setTitle("Upload Video")

    def dialog_open(self):
        filename, _ = QFileDialog.getOpenFileName(\
            self, "Select video to upload", ".", \
                "Video(*.mp4)")
        
        if filename:
            self.file_list.setVisible(True)
            self.file_list.clear()
            self.file_list.addItem(filename)


class DragAndDrop(QLabel):  # 가상 os라 안되는 거 같음. 로컬에서 시도해볼 것.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.file_list = list()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        for f in files:
            self.file_list.append(f)

    # def resizeEvent(self, event):
    #     self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
    #     super().resizeEvent(event)


# logout 버튼만 추가된 기본 위젯
class DefaultWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.threshold = 0.5
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # define and add logout widget
        self.logout = QPushButton("Logout")
        self.logout.setMaximumWidth(100)
        self.layout.addWidget(self.logout)
        

# 개인정보 탐지 강도 선택 기능 추가
class DetectionWidget(DefaultWidget):
    def __init__(self):
        super().__init__()

        self.threshold_group = QGroupBox()
        self.layout.addWidget(self.threshold_group)
        self.threshold_group.setTitle("Select Privacy Detection Strength")
        self.threshold_group.setLayout(QVBoxLayout())

        # combobox for threshold selection
        self.threshold_combobox = QComboBox()
        self.threshold_combobox.setMaximumWidth(400)
        # self.threshold_group_combobox.addItems(["둔감", "보통", "민감"])
        self.threshold_combobox.addItems(["Insensitive", "Normal", "Sensitive"])
        self.threshold_combobox.setCurrentIndex(1)
        self.threshold_combobox.currentIndexChanged.connect(self.index_changed)

        # self.layout.addWidget(self.threshold_group_combobox)
        self.threshold_group.layout().addWidget(self.threshold_combobox)

    def index_changed(self, index):
        threshold = [0.2, 0.5, 0.8]
        return threshold[index]


class ImageDetectionWidget(DetectionWidget):
    def __init__(self):
        super().__init__()
        # self.upload_widget = ImageFileUploadWidget()
        self.upload_widget = FileUploadWidget(file_type="image")
        self.layout.addWidget(self.upload_widget)

        self.upload_widget.set_url('http://192.168.1.230:4000/upload')
        self.upload_widget.resultSignal.connect(self.show_result)

        self.result_test = QLabel()
        self.layout.addWidget(self.result_test)

    def index_changed(self, index):
        threshold = super().index_changed(index)
        self.upload_widget.threshold = threshold

    def show_result(self, result):
        pixmap = QPixmap.fromImage(result)
        self.result_test.setPixmap(pixmap)


class VideoDetectionWidget(DetectionWidget):
    def __init__(self):
        super().__init__()
        # self.upload_widget = VideoFileUploadWidget()
        self.upload_widget = FileUploadWidget(file_type="video")
        self.layout.addWidget(self.upload_widget)

        self.upload_widget.resultSignal.connect(self.show_result)

    def index_changed(self, index):
        threshold = super().index_changed(index)
        self.upload_widget.threshold = threshold

    def show_result(self, result):
        pass


class VideoRecognitionWidget(DefaultWidget):
    def __init__(self):
        super().__init__()
        # self.upload_widget = ImageFileUploadWidget()
        self.upload_widget = FileUploadWidget("image")
        self.layout.addWidget(self.upload_widget)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ImageDetectionWidget()
    window.show()

    exit(app.exec())
