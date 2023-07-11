import sys
from urllib.request import urlopen
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PyQt6 import QtCore, QtWidgets

HOST, PORT = '127.0.0.1', 12345

class HttpDaemon(QtCore.QThread):
    def run(self):
        self._server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
        self._server.socket.close()
        self.wait()

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.button = QtWidgets.QPushButton('Start', self)
        self.button.clicked.connect(self.handleButton)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)
        self.httpd = HttpDaemon(self)

    def handleButton(self):
        if self.button.text() == 'Start':
            self.httpd.start()
            self.button.setText('Test')
        else:
            urlopen('http://%s:%s/' % (HOST, PORT))

    def closeEvent(self, event):
        self.httpd.stop()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())