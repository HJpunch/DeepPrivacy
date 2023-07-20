from requests import get
from typing import Literal
from PyQt6.QtWidgets import QLayout, QGridLayout, QLabel, QGroupBox, QPushButton, \
    QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap


def remove_all_widgets(layout:QLayout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().deleteLater()


class QPixmapLabel(QLabel):
    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:  # data: bytes
            data = kwargs.pop('data')
        super().__init__(*args, **kwargs)
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.setPixmap(pixmap)


class QDragAndDropLabel(QLabel):  # 가상 os라 안되는 거 같음. 로컬에서 시도해볼 것.
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


class QResultDisplayWidget(QGroupBox):
    def __init__(self, title:str):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setTitle(title)

    def add_image(self, data:bytes, row:int, col:int):
        label = QPixmapLabel(data=data)
        self.grid.addWidget(label, row, col)

    def add_label(self, data:str, row:int, col:int):
        self.grid.addWidget(QLabel(data), row, col)


class QDownloadButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumWidth(200)

        self.clicked.connect(self.download)

    def set_url(self, url):
        self.url = url

    def download(self):
        file_name = self.url.split('/')[-1]
        save_dir= QFileDialog.getSaveFileName(self,
                                              "Save File",
                                              f'./{file_name}')
        save_dir = save_dir[0]
        if save_dir:
            with open(save_dir, 'wb') as f:
                response = get(self.url)
                f.write(response.content)


class QErrorMessage(QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStandardButtons(QMessageBox.StandardButton.Close)
        self.setIcon(QMessageBox.Icon.Critical)


class QConnectionErrorMessage(QErrorMessage):
    def __init__(self, parent, url):
        # if 'url' in kwargs:
        #     url = kwargs.pop('url')
        # super().__init__(*args, **kwargs)
        super().__init__(parent)
        self.setWindowTitle("Server Connection Error")
        self.setText(f"No connection adapters were found for {url}.\n\
Please try again later or contact system administrator")
        
    
class QLoginErrorMessage(QErrorMessage):
    def __init__(self, parent, error:Literal['userid', 'password']):
        super().__init__(parent)

        self.setWindowTitle("Login Failure")

        if error == 'userid':
            self.setText("There is no registered member information.\n\
Please check your ID again or use it after registering as a member.")
        elif error =='password':
            self.setText("Password error. Please try again.")