import pandas as pd

from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout,\
    QLabel, QPushButton, QComboBox, QFileDialog, QListWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Literal

from windows.basic_window import ICONS_DIR
from utils.HTTP_request import check_server_status, read_file, post_file, get_file
from utils.utility_widget import remove_all_widgets, QPixmapLabel, QDragAndDropLabel, QResultDisplayWidget, QDownloadButton,\
 QConnectionErrorButton


class FileUploadWidget(QGroupBox):
    resultSignal = pyqtSignal(dict)
    def __init__(self, file_type:Literal['image', 'video']):
        super().__init__()
        self.file_type = file_type
        self.threshold = 0.5
        self.root_url = str()  # url for server status check
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

        label = QDragAndDropLabel("Drag and Drop Files Here")
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

        self.result_widget = QWidget()
        self.result_widget.setVisible(False)
        self.result_widget.setLayout(QVBoxLayout())
        self.box.addWidget(self.result_widget)

    def set_root_url(self, url):
        self.root_url = url

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
        
        if not check_server_status(self.root_url):
            button = QConnectionErrorButton(parent=self, url=self.url)
            button.exec()
            return

        if filenames:
            self.clear()
            self.file_list.setVisible(True)
            self.result_widget.setVisible(True)

            if isinstance(filenames, list):
                for f in filenames:
                    self.file_list.addItem(f)
            else:
                self.file_list.addItem(filenames)

            upload = read_file(filenames)
            data = {"threshold": self.threshold}
            result = post_file(url=self.url, files=upload, data=data)
            self.resultSignal.emit(result)

    def clear(self):
        self.file_list.clear()
        remove_all_widgets(self.result_widget.layout())
        self.file_list.setVisible(False)
        self.result_widget.setVisible(False)


# logout 버튼만 추가된 기본 위젯 + 
class DefaultWidget(QWidget):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.threshold = 0.5
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # define and add logout widget
        self.logout = QPushButton("Logout")
        self.logout.setMaximumWidth(100)
        self.layout.addWidget(self.logout)

        # self.result_widget = QWidget()
        # self.result_widget.setLayout(QVBoxLayout())
        

# 개인정보 탐지 강도 선택 기능 추가
class DetectionWidget(DefaultWidget):
    def __init__(self, url):
        super().__init__(url)

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
    def __init__(self, url):
        super().__init__(url)
        self.upload_widget = FileUploadWidget(file_type="image")
        self.layout.addWidget(self.upload_widget)

        self.upload_widget.set_root_url(url)
        self.upload_widget.set_url(f'{self.url}/detect/image')
        self.upload_widget.resultSignal.connect(self.show_result)

        # self.layout.addWidget(self.result_widget)

    def index_changed(self, index):
        threshold = super().index_changed(index)
        self.upload_widget.threshold = threshold

    def show_result(self, result):
        result = result['result']

        for image_name in result.keys():
            container = QWidget()
            container.setLayout(QHBoxLayout())
            image_url = f"{self.url}/{image_name}"
            image = get_file(image_url)
            label = QPixmapLabel(data=image)
            container.layout().addWidget(label)

            detect_result = QResultDisplayWidget(title="Detection Information")
            container.layout().addWidget(detect_result)
            self.upload_widget.result_widget.layout().addWidget(container)

            if result[image_name] == []:
                detect_result.add_label(data="None", row=0, col=0)
                continue

            for i, temp in enumerate(result[image_name]):
                obj_class = temp['class']
                confidence = temp['conf']
                crop_dir = temp['crop_dir']
                coord = temp['xyxy']

                crop_url = f"{self.url}/{crop_dir}"
                crop_image = get_file(crop_url)
                detect_result.add_image(data=crop_image, row=i, col=0)

                label = f"class: {obj_class}\n\nconfidence: {confidence}\n\ncoord: {coord}"
                detect_result.add_label(data=label, row=i, col=1)


class VideoDetectionWidget(DetectionWidget):
    def __init__(self, url:str):
        super().__init__(url)
        self.upload_widget = FileUploadWidget(file_type="video")
        self.layout.addWidget(self.upload_widget)

        self.upload_widget.set_root_url(url)
        self.upload_widget.set_url(f'{self.url}/detect/video')
        self.upload_widget.resultSignal.connect(self.show_result)

        # self.layout.addWidget(self.result_widget)

    def index_changed(self, index):
        threshold = super().index_changed(index)
        self.upload_widget.threshold = threshold

    def show_result(self, result):
        output_video_dir = result['video_dir']
        output_video_url = f"{self.url}/{output_video_dir}"
        fps = result['fps']

        download_button = QDownloadButton("Douwnload Output Video")
        download_button.set_url(output_video_url)
        self.upload_widget.result_widget.layout().addWidget(download_button)

        for i, frame in enumerate(result['result'].keys()):
            sec = f"{i/fps:.4f}"
            exp = f"frame_{i}   sec: {sec}"

            detect_result = QResultDisplayWidget(title=exp)
            self.upload_widget.result_widget.layout().addWidget(detect_result)

            for idx, temp in enumerate(result['result'][frame]):
                obj_class = temp['class']
                confidence = temp['conf']
                crop_dir = temp['crop_dir']
                coord = temp['xyxy']

                crop_url = f"{self.url}/{crop_dir}"
                crop_image = get_file(crop_url)
                detect_result.add_image(data=crop_image, row=idx, col=0)

                label = f"class: {obj_class}\n\nconfidence: {confidence}\n\ncoord: {coord}"
                detect_result.add_label(data=label, row=idx, col=1)


class VideoRecognitionWidget(DefaultWidget):
    def __init__(self, url:str):
        super().__init__(url)
        self.upload_widget = FileUploadWidget("image")
        self.layout.addWidget(self.upload_widget)

        self.upload_widget.set_root_url(url)
        self.upload_widget.set_url(f'{self.url}/recognize/video')
        self.upload_widget.resultSignal.connect(self.show_result)

        # self.layout.addWidget(self.result_widget)

    def show_result(self, result):
        csv_save_dir = result['csv_save_dir']
        result = result['result']

        crop_img_dir_list = result['crop_img_dir_list']
        recognize_result = result['recognize']
        video_unique_result = result['video']

        if len(crop_img_dir_list) == 0:
            self.upload_widget.result_widget.layout().addWidget(QResultDisplayWidget(title="None"))
            return

        for i, (img_json, video) in enumerate(zip(recognize_result, video_unique_result)):
            crop_dir = crop_img_dir_list[i]
            csv = csv_save_dir + f"/result_{i}.csv"
            csv_url = f"{self.url}/{csv}"

            recognize_result_widget = QResultDisplayWidget(title=f"face {i}")
            self.upload_widget.result_widget.layout().addWidget(recognize_result_widget)

            crop_url = f"{self.url}/{crop_dir}"
            crop_image = get_file(crop_url)
            recognize_result_widget.add_image(data=crop_image, row=0, col=0)

            download_button = QDownloadButton("Download CSV File")
            download_button.set_url(csv_url)

            if not video:
                recognize_result_widget.add_label(data="None", row=0, col=1)
                continue

            video_list = [i for i in list(video)]
            recognize_result_widget.add_label(data=str(video_list), row=0, col=1)
            recognize_result_widget.layout().addWidget(download_button, 1, 0)

            df = pd.DataFrame(img_json)
            for row in range(len(df)):
                temp = df.iloc[row]
                image_path = temp['path']
                frame = temp['frame']
                video_name = [temp['video']]
                conf = temp['theta']

                # 서버 내 별도 디렉토리에 있어 가져올 수 없음
                # image_url = f"{self.url}/{image_path}"
                # image = get_file(image_url)
                # recognize_result_widget.add_image(data=image, row=row+1, col=0)

                label = f"frame: {frame}\nvideo: {video_name}\nconfidence: {conf}"
                recognize_result_widget.add_label(data=label, row=row+2, col=1)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ImageDetectionWidget()
    window.show()

    exit(app.exec())
