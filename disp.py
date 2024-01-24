import sys
import random
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap


class LiveDisplayApp(QWidget):
    def __init__(self, initial_values):
        super().__init__()

        self.init_ui()

        # Initialize initial values
        self.presence = initial_values["presence"]
        self.hr_prediction = initial_values["hr"]
        self.bp_systolic_prediction = initial_values["bp_systolic"]
        self.bp_diastolic_prediction = initial_values["bp_diastolic"]
        self.rr_prediction = initial_values["rr"]
        self.sp_prediction = initial_values["sleep_pose"]
        self.ss_prediction = initial_values["sleep_stage"]
        # Update labels with initial values
        self.update_labels()

    def init_ui(self):
        # Set up UI components
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("D:/Dungeon/blu/livedisplay/images/logo.png")
        self.image_label.setPixmap(pixmap.scaledToWidth(100, Qt.SmoothTransformation))

        self.presence_label = QLabel("Presence: ")
        self.hr_label = QLabel("Heart Rate: ")
        self.bp_systolic_label = QLabel("Systolic BP: ")
        self.bp_diastolic_label = QLabel("Diastolic BP: ")
        self.rr_label = QLabel("Respiratory Rate: ")
        self.sp_label = QLabel("Sleep Pose: ")
        self.ss_label = QLabel("Sleep Stage: ")

        # Create separate group boxes for each parameter
        presence_group_box = self.create_group_box("Presence", self.presence_label)
        hr_group_box = self.create_group_box("Heart Rate", self.hr_label)
        bp_group_box = self.create_group_box(
            "Blood Pressure", self.bp_systolic_label, self.bp_diastolic_label
        )
        rr_group_box = self.create_group_box("Respiratory Rate", self.rr_label)
        sleep_group_box = self.create_group_box("Sleep", self.sp_label, self.ss_label)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(presence_group_box)
        layout.addWidget(hr_group_box)
        layout.addWidget(bp_group_box)
        layout.addWidget(rr_group_box)
        layout.addWidget(sleep_group_box)

        # make modifications to appearance here

        # font = self.presence_label.font()
        # font.setPointSize(16)  # Set the font size as needed
        # self.presence_label.setFont(font)
        # self.hr_label.setFont(font)
        # self.bp_systolic_label.setFont(font)
        # self.bp_diastolic_label.setFont(font)
        # self.rr_label.setFont(font)
        # layout.setSpacing(20)  # Set the spacing between widgets as needed

        # Set up timer for live updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        # Set the size of the main window
        self.resize(400, 600)  # Set the width and height as needed
        self.setLayout(layout)
        self.setStyleSheet(
            "QWidget { background-color: white; color: black; font-family: 'Poppins Light'; font-size:10px; }"  # Set the background color and font color for the main window
            "QLabel { color: Black; font-family: 'Poppins SemiBold'; font-size:15px;}"  # Set the font color for all labels
            "QGroupBox { border: 2px inset cyan; border-radius: 5px; margin-top: 10px;}"
        )  # Style for group boxes

        # Set up timer for live updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

    def create_group_box(self, title, *widgets):
        group_box = QGroupBox(title)
        layout = QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        group_box.setLayout(layout)
        return group_box

    def update_display(self):
        # Fetch new random predictions
        self.presence = random.choice([True, False])
        self.hr_prediction = random.randint(60, 120)
        self.bp_systolic_prediction = random.randint(90, 140)
        self.bp_diastolic_prediction = random.randint(60, 90)
        self.rr_prediction = random.randint(12, 20)
        self.sp_prediction = random.choice(["supine", "prone", "left", "right"])
        self.ss_prediction = random.choice(
            ["Awake", "REM", "light sleep", "deep sleep"]
        )
        # Update labels with new predictions
        self.update_labels()

    def update_labels(self):
        if self.presence:
            self.presence_label.setText(
                '<html><body style="color: green;">'
                'Presence: Yes<div style="display: inline;">'
                '<img src="D:/Dungeon/blu/livedisplay/images/fullbed.png" width="60"></div></body></html>'
            )
            self.hr_label.setText(f"Heart Rate: {self.hr_prediction} bpm")
            self.bp_systolic_label.setText(
                f"Systolic BP: {self.bp_systolic_prediction} mmHg"
            )
            self.bp_diastolic_label.setText(
                f"Diastolic BP: {self.bp_diastolic_prediction} mmHg"
            )
            self.rr_label.setText(f"Respiratory Rate: {self.rr_prediction} breaths/min")
            self.sp_label.setText(f"Sleep Pose: {self.sp_prediction}")
            self.ss_label.setText(f"Sleep Stage: {self.ss_prediction}")
        else:
            self.presence_label.setText(
                '<html><body style="color: red;">'
                'Presence: No<div style="display: inline;">'
                '<img src="D:/Dungeon/blu/livedisplay/images/emptybed.png" width="60"></div></body></html>'
            )
            self.hr_label.setText("Heart Rate: -")
            self.bp_systolic_label.setText("Systolic BP: -")
            self.bp_diastolic_label.setText("Diastolic BP: -")
            self.rr_label.setText("Respiratory Rate: -")
            self.sp_label.setText("Sleep Pose: Empty Bed")
            self.ss_label.setText(f"Sleep Stage: Empty Bed")


if __name__ == "__main__":
    # Generate initial random values
    initial_values = {
        "presence": True,
        "hr": random.randint(60, 120),
        "bp_systolic": random.randint(90, 140),
        "bp_diastolic": random.randint(60, 90),
        "rr": random.randint(12, 20),
        "sleep_pose": "supine",
        "sleep_stage": "light sleep",
    }

    app = QApplication(sys.argv)
    window = LiveDisplayApp(initial_values)
    window.setWindowTitle("Live Display App")
    window.show()
    sys.exit(app.exec_())
