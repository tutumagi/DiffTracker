import os
import tempfile
from PIL import ImageGrab, Image
import Quartz.CoreGraphics as CG


def capture_area(region, save_path):
    screenshot = ImageGrab.grab(bbox=region)
    screenshot.save(save_path)


def select_area():
    # TODO: 在这里添加代码以获取用户选择的屏幕区域
    # 你可以使用 Tkinter 的 Toplevel 窗口来实现一个简单的选择界面
    # 返回选取的区域坐标 (x, y, width, height)
    x = 1807
    y = 105
    width = 445
    height = 709
    region = (x, y, x + width, y + height)
    return region


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QRect
from PIL import ImageGrab


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.is_selecting = False

    def mousePressEvent(self, event):
        self.start_x = event.x()
        self.start_y = event.y()
        self.current_x = event.x()
        self.current_y = event.y()
        self.is_selecting = True

    def mouseMoveEvent(self, event):
        self.current_x = event.x()
        self.current_y = event.y()
        self.update()

    def mouseReleaseEvent(self, event):
        self.is_selecting = False
        print(
            f"Region selected: ({self.start_x}, {self.start_y}) to ({self.current_x}, {self.current_y})"
        )

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.is_selecting:
            rect = QRect(
                self.start_x,
                self.start_y,
                self.current_x - self.start_x,
                self.current_y - self.start_y,
            )
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(rect)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Screen Capture with PyQt5")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.showFullScreen()

        # Get screen size
        screen_geometry = QApplication.desktop().screenGeometry()
        pixelRatio = QApplication.desktop().devicePixelRatio()
        print(f"pixel ration is {pixelRatio}")
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.setGeometry(0, 0, screen_width, screen_height)

        # Capture the screen
        screen_capture = ImageGrab.grab()
        screen_capture.save("screen_capture.png")

        # Load the screen capture
        self.image_label = ImageLabel()
        pixmap = QPixmap("screen_capture.png")
        pixmap.setDevicePixelRatio(pixelRatio)
        self.image_label.setPixmap(pixmap)
        # self.image_label.resize(pixmap.width(), pixmap.height())

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        # Set layout in the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    # Enable high DPI scaling
    # app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    # Use the DPI of the monitor

    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
