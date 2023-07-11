import sys

from PyQt6.QtWidgets import QMainWindow, QWidget, QStackedWidget, QTextEdit, QPushButton, QLabel, QGroupBox, QListView, QBoxLayout, QApplication
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import QModelIndex, Qt, pyqtSlot


class StWidgetForm(QGroupBox):
    def __init__(self):
        super().__init__()
        self.box = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.setLayout(self.box)

    
class Widget1(StWidgetForm):
    def __init__(self):
        super().__init__()
        self.setTitle("Widget1")
        self.box.addWidget(QPushButton("test1"))
        self.box.addWidget(QPushButton("test2"))
        self.box.addWidget(QPushButton("test3"))


class Widget2(StWidgetForm):
    def __init__(self):
        super().__init__()
        self.setTitle("Widget2")
        self.box.addWidget(QTextEdit())


class Widget3(StWidgetForm):
    def __init__(self):
        super().__init__()
        self.setTitle("Widget3")
        self.box.addWidget(QLabel("Test Label"))


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget(self)
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("Stacked Widget Test")
        widget_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)

        group = QGroupBox()
        box = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        group.setLayout(box)
        group.setTitle("Buttons")
        widget_layout.addWidget(group)

        fruits = ["Buttons in GroupBox", "TextBox in GroupBox", "Label in GroupBox", "TextEdit"]
        view = QListView(self)
        model = QStandardItemModel()
        
        for f in fruits:
            model.appendRow(QStandardItem(f))
        view.setModel(model)
        box.addWidget(view)

        self.stacked_widget.addWidget(Widget1())
        self.stacked_widget.addWidget(Widget2())
        self.stacked_widget.addWidget(Widget3())
        self.stacked_widget.addWidget(QTextEdit())

        widget_layout.addWidget(self.stacked_widget)
        self.setLayout(widget_layout)

        # signal-slot
        view.clicked.connect(self.slot_clicked_item)

    @pyqtSlot(QModelIndex)
    def slot_clicked_item(self, QModelIndex):
        self.stacked_widget.setCurrentIndex(QModelIndex.row())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec())