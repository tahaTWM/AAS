import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QApplication,
    QSlider,
)
from pyqtgraph import ImageView


class StartWindow(QMainWindow):
    def __init__(self, camera=None):
        super().__init__()
        self.camera = camera

        self.central_widget = QWidget()

        self.button_movie = QPushButton("Start Movie", self.central_widget)
        self.image_view = ImageView()

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_movie)
        self.layout.addWidget(self.image_view)

        self.setCentralWidget(self.central_widget)

        self.button_movie.clicked.connect(self.start_movie)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)

    def update_image(self):
        frame = self.camera.get_frame()
        self.image_view.setImage(frame.T)

    def update_movie(self):
        self.image_view.setImage(self.camera.last_frame.T)

    def update_brightness(self, value):
        value /= 10
        self.camera.set_brightness(value)

    def start_movie(self):
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.start()
        self.update_timer.start(30)


class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)


if __name__ == "__main__":
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())
