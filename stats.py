import sys
import random
from config import *
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QComboBox,
    QHeaderView,
    QDateTimeEdit,
)
from PyQt5.QtCore import QTimer, Qt, QDateTime
from PyQt5.QtGui import QColor


class MainWindow(QWidget):
    def __init__(self, s3_client, bucket_name):
        super().__init__()
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Device Connection Status")
        self.setGeometry(100, 100, 600, 400)  # Adjusted for added widgets

        self.dateTimeEdit = QDateTimeEdit(self)
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEdit.dateTimeChanged.connect(self.dateTimeChanged)

        # Table setup as before
        self.table = QTableWidget()
        self.table.setRowCount(4)  # Devices, Apple Watch, Sleep Pose, BP
        self.table.setColumnCount(4)  # Header + 3 devices
        self.table.setHorizontalHeaderLabels(["Device Status", "CT01", "CT02", "CT03"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)

        # Setting the row names
        row_labels = ["Raw Data", "Apple Watch", "Sleep Pose", "BP"]
        for i, label in enumerate(row_labels):
            self.table.setItem(i, 0, QTableWidgetItem(label))
            self.table.item(i, 0).setForeground(QColor("black"))
            for j in range(1, 4):
                self.table.setItem(i, j, QTableWidgetItem(""))
                self.table.item(i, j).setBackground(QColor("red"))

        # Adjusting column widths and row heights for better aesthetics
        header = self.table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(50)

        # Adding the table to the main layout
        layout = QVBoxLayout()
        layout.addWidget(self.dateTimeEdit)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Update timer to check S3 every hour
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkS3ForData)
        self.timer.start(3600000)  # 1 hour in milliseconds

    def dateTimeChanged(self, datetime):
        # This method can be used to perform actions when the date/time changes
        self.checkS3ForData()

    def checkS3ForData(self):
        # Example path: device_01/20240108/MAT/
        date_str = self.dateTimeEdit.dateTime().toString("yyyyMMdd")
        hour_str = self.dateTimeEdit.dateTime().toString("HH")

        for row in range(1, 4):  # Assuming the first row is for raw data
            for col in range(1, 4):  # Device columns
                device_folder = f"device_0{col}/{date_str}/MAT/"
                file_prefix = f"raw_{hour_str}"
                try:
                    response = self.s3_client.list_objects_v2(
                        Bucket=self.bucket_name, Prefix=device_folder
                    )
                    files = [
                        obj["Key"]
                        for obj in response.get("Contents", [])
                        if file_prefix in obj["Key"]
                    ]
                    if files:
                        self.table.item(0, col).setBackground(QColor("green"))
                    else:
                        self.table.item(0, col).setBackground(QColor("red"))
                except Exception as e:
                    print(f"Error checking S3: {e}")
                    self.table.item(row, col).setBackground(QColor("red"))


if __name__ == "__main__":
    # AWS credentials and S3 client setup
    s3_bucket_name = "data-blusim-care"
    os.environ["AWS_DEFAULT_REGION"] = app_cfg["aws_config_region"]
    os.environ["AWS_ACCESS_KEY_ID"] = app_cfg["aws_config_key"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = app_cfg["aws_config_pass"]
    s3_client = boto3.client("s3")

    def list_s3_buckets():
        try:
            # Create an S3 client
            s3 = boto3.client("s3")
            # Call S3 to list current buckets
            response = s3.list_buckets()
            # Get a list of all bucket names from the response
            buckets = [bucket["Name"] for bucket in response["Buckets"]]

            # Print out the bucket list
            print("Bucket List:")
            for bucket in buckets:
                print(bucket)

            return True
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except ClientError as e:
            print(f"Client error: {e}")
            return False

    if __name__ == "__main__":
        if list_s3_buckets():
            print("Successfully connected to S3 and listed buckets.")
        else:
            print("Failed to connect to S3.")

    app = QApplication(sys.argv)
    mainWindow = MainWindow(s3_client, s3_bucket_name)
    mainWindow.show()

    sys.exit(app.exec_())
