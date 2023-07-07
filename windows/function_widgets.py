from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QBoxLayout, \
    QLabel, QPushButton, QComboBox, QFileDialog, QListWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# from main_window import ICONS_DIR
from basic_window import ASSET

ICONS_DIR = ASSET + "/icons/"


class FileUploadWidget(QGroupBox):
    def __init__(self):
        super().__init__()
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

        # label = QLabel("Drag and Drop Files Here")
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
        self.file_list.itemChanged.connect(self.api_test)

    def dialog_open(self):
        pass

    def api_test(self, item):
        pass


class ImageFileUploadWidget(FileUploadWidget):
    def __init__(self):
        super().__init__()
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

    def api_test(self, item):
        


class VideoFileUploadWidget(FileUploadWidget):
    def __init__(self):
        super().__init__()
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

    def dragEnterEvent(self, event):
        if event.mimedata().hasUrls():
            print("뭐임")
            event.accept()
        
        else:
            print("tlqkf")
            event.ignore()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimedata().urls()]
        for f in files:
            print(f)

    # def resizeEvent(self, event):
    #     self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
    #     super().resizeEvent(event)


# logout 버튼만 추가된 기본 위젯
class DefaultWidget(QWidget):
    def __init__(self):
        super().__init__()
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
        self.threshold = 0.5

        # label = QLabel("개인정보 탐지 강도 선택")
        # self.layout.addWidget(QLabel("Select Privacy Detection Strength"))

        self.threshold = QGroupBox()
        self.layout.addWidget(self.threshold)
        self.threshold.setTitle("Select Privacy Detection Strength")
        self.threshold.setLayout(QVBoxLayout())

        # combobox for threshold selection
        self.threshold_combobox = QComboBox()
        self.threshold_combobox.setMaximumWidth(400)
        # self.threshold_combobox.addItems(["둔감", "보통", "민감"])
        self.threshold_combobox.addItems(["Insensitive", "Normal", "Sensitive"])
        self.threshold_combobox.setCurrentIndex(1)
        self.threshold_combobox.currentIndexChanged.connect(self.index_changed)

        # self.layout.addWidget(self.threshold_combobox)
        self.threshold.layout().addWidget(self.threshold_combobox)

    def index_changed(self, index):
        threshold = [0.2, 0.5, 0.8]
        self.threshold = threshold[index]


class ImageDetectionWidget(DetectionWidget):
    def __init__(self):
        super().__init__()
        self.upload_widget = ImageFileUploadWidget()
        self.layout.addWidget(self.upload_widget)


class VideoDetectionWidget(DetectionWidget):
    def __init__(self):
        super().__init__()
        self.upload_widget = VideoFileUploadWidget()
        self.layout.addWidget(self.upload_widget)


class VideoRecognitionWidget(DefaultWidget):
    def __init__(self):
        super().__init__()
        self.upload_widget = ImageFileUploadWidget()
        self.layout.addWidget(self.upload_widget)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = VideoRecognitionWidget()
    window.show()

    exit(app.exec())