from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import cv2
import time
from cannyEdgeDetection import cannyDetector

class App(QWidget):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.title = 'Canny Edge Detection'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.fileName = None
        self.exportPath = None
        self.saveFlag = False
        self.centralwidget = QtWidgets.QWidget(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        # create a label
        self.label1 = QLabel(self)
        self.label1.move(200, 300)
        self.label1.resize(640, 480)

        self.label2 = QLabel(self)
        self.label2.move(1000, 300)
        self.label2.resize(640, 480)

        # Create buttons
        self.button1 = QPushButton('select video file', self)
        self.button1.setToolTip('This is an button')
        self.button1.move(800, 100)
        self.button1.resize(300, 30)
        self.button1.clicked.connect(self.openFileNameDialog)

        self.button2 = QPushButton('start', self)
        self.button2.setToolTip('This is an button')
        self.button2.move(1200, 100)
        self.button2.resize(100, 30)
        self.button2.clicked.connect(self.play)

        self.button2 = QPushButton('stop', self)
        self.button2.setToolTip('This is an button')
        self.button2.move(1300, 100)
        self.button2.resize(100, 30)
        self.button2.clicked.connect(self.stop)

        self.button3 = QPushButton('Save', self)
        self.button3.setToolTip('This is an button')
        self.button3.move(1400, 100)
        self.button3.resize(100, 30)
        self.button3.clicked.connect(self.save)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(300, 100)
        self.textbox.resize(500, 30)

        # Create text
        self.text_label1 = QLabel("Original Video", self)
        self.text_label1.move(450, 250)
        self.text_label1.resize(150, 40)

        self.text_label2 = QLabel("Proceeded Video", self)
        self.text_label2.move(1250, 250)
        self.text_label2.resize(150, 40)

    @pyqtSlot()
    def openFileNameDialog(self):
        self.fileName=None
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "select a video file", "", "All Files (*)", options=options)
        self.fileName = fileName
        if fileName:
            self.textbox.setText(fileName.encode('utf-8'))
        else:
            self.textbox.setText("No File Selected!")

    def play(self):
        cap = cv2.VideoCapture(self.fileName.encode('utf-8'))
        fps = cap.get(cv2.CAP_PROP_FPS)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                canny_frame = cannyDetector(frame)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.label1.setPixmap(QPixmap.fromImage(rgbImage))
                self.label2.setPixmap(QPixmap.fromImage(canny_frame))
                self.label1.repaint()
                self.label2.repaint()

                time.sleep(1/fps)
                QtGui.QGuiApplication.processEvents()

            else:
                break

    def stop(self):
        sys.exit(0)

    @pyqtSlot()
    def save(self):
        self.exportPath = None
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        exportPath, _ = QFileDialog.getSaveFileName(self,"save video", "", "Video files(*.mp4)", options=options)
        self.exportPath = exportPath
        if exportPath:
            cap = cv2.VideoCapture(self.fileName.encode('utf-8'))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = cap.get(cv2.CAP_PROP_FPS)
            size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            canny_video = cv2.VideoWriter(exportPath, fourcc, fps, size, False)

            while True:
                ret, frame = cap.read()
                if ret:
                    out_frame = cannyDetector(frame)
                    canny_video.write(out_frame)
                else:
                    sys.exit(0)
        else:
            self.textbox.setText("No File Saved!")



app = QtWidgets.QApplication(sys.argv)
ex = App()
ex.show()
sys.exit(app.exec_())

