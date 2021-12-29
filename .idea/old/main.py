# importing required libraries
from PyQt5.QtCore import center
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import sys
import time
import cv2

# Main window class
class MainWindow(QMainWindow):

    # constructor
    def __init__(self):
        super().__init__()
        # setting geometry
        self.setGeometry(100, 100, 800, 600)

        # setting style sheet
        self.setStyleSheet("background : lightgrey;")

        # getting available cameras
        self.available_cameras = QCameraInfo.availableCameras()

        # if no camera found
        if not self.available_cameras:
            # exit the code
            sys.exit()

        # creating a status bar
        self.status = QStatusBar()

        # setting style sheet to the status bar
        self.status.setStyleSheet("background : white;")

        # adding status bar to the main window
        self.setStatusBar(self.status)

        # path to save
        self.save_path = ""

        # creating a QCameraViewfinder object
        self.viewfinder = QCameraViewfinder()

        # showing this viewfinder
        self.viewfinder.show()

        # making it central widget of main window
        self.setCentralWidget(self.viewfinder)

        # Set the default camera.
        self.select_camera(0)

        # creating a tool bar
        toolbar = QToolBar("Camera Tool Bar")

        # adding tool bar to main window
        self.addToolBar(toolbar)

        # creating a photo action to take photo
        click_action = QAction("Take photo", self)

        # adding status tip to the photo action
        click_action.setStatusTip("This will capture picture")

        # adding tool tip
        click_action.setToolTip("Capture picture")

        # adding action to it
        # calling take_photo method
        click_action.triggered.connect(self.click_photo)

        # adding this to the tool bar
        toolbar.addAction(click_action)

        # creating a combo box for selecting camera
        camera_selector = QComboBox()

        # adding status tip to it
        camera_selector.setStatusTip("Choose camera to take pictures")

        # adding tool tip to it
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)

        # adding items to the combo box
        camera_selector.addItems(
            [camera.description() for camera in self.available_cameras]
        )

        # adding action to the combo box
        # calling the select camera method
        camera_selector.currentIndexChanged.connect(self.select_camera)

        # adding this to tool bar
        toolbar.addWidget(camera_selector)

        # adding test btn
        test_BTN = QAction("Test BTN", self)
        test_BTN.triggered.connect(self.testBTN)
        toolbar.addAction(test_BTN)

        # setting tool bar stylesheet
        toolbar.setStyleSheet("background : white;")

        # setting window title
        self.setWindowTitle("AAS")

        # showing the main window
        self.show()

    # method to select camera
    def select_camera(self, i):

        # getting the selected camera
        self.camera = QCamera(self.available_cameras[i])

        # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)

        # setting capture mode to the camera
        self.camera.setCaptureMode(QCamera.CaptureStillImage)

        # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))

        # start the camera
        self.camera.start()

        # creating a QCameraImageCapture object
        self.capture = QCameraImageCapture(self.camera)

        # showing alert if error occur
        self.capture.error.connect(lambda error_msg, error, msg: self.alert(msg))

        # when image captured showing message
        self.capture.imageCaptured.connect(
            lambda d, i: self.status.showMessage(
                "Image captured : " + str(self.save_seq)
            )
        )

        # getting current camera name
        self.current_camera_name = self.available_cameras[i].description()

        # inital save sequence
        self.save_seq = 0

    # method to take photo
    def click_photo(self):

        # time stamp
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")

        # capture the image and save it on the save path
        self.capture.capture(
            os.path.join(
                self.save_path,
                "%s-%04d-%s.jpg" % (self.current_camera_name, self.save_seq, timestamp),
            )
        )

        # increment the sequence
        self.save_seq += 1

    # test dev
    def testBTN(self):
        print("check")

    # method for alerts
    def alert(self, msg):

        # error message
        error = QErrorMessage(self)

        # setting text to the error message
        error.showMessage(msg)


# Driver code
if __name__ == "__main__":

    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = MainWindow()

    # start the app
    sys.exit(App.exec())
