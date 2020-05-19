from mysql.connector import MySQLConnection, Error
from DatabaseDAO import DatabaseDAO
from decimal import getcontext, Decimal
import sys, time
import re
from uuid import uuid1
from PyQt5.QtWidgets import (
    QApplication,
    QSplashScreen,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        ############################## GUI ###############################
        self.setWindowTitle("Zernike Parking App Registration System")
        self.resize(400, 200)

        layout = QVBoxLayout()

        label_first_name = QLabel("First Name : ")
        label_surname = QLabel("Surname : ")
        label_customer_type = QLabel(
            "Wokring/Studying at ('Hanze' or 'RUG') : "
        )
        label_student_employee_code = QLabel("Student/Employee code : ")
        label_tel_number = QLabel("Tel. Number : ")
        label_email = QLabel("Email address : ")
        label_license_plate = QLabel("Car license plate : ")
        label_brand_name = QLabel("Car brand name : ")
        label_fuel_type = QLabel("Car fuel type : ")
        label_payment_method = QLabel("Payment method : ")

        self.input_first_name = QLineEdit()
        self.input_surname = QLineEdit()
        self.input_customer_type = QLineEdit()
        self.input_student_employee_code = QLineEdit()
        self.input_tel_number = QLineEdit()
        self.input_email = QLineEdit()
        self.input_license_plate = QLineEdit()
        self.input_brand_name = QLineEdit()
        self.input_fuel_type = QComboBox()
        self.input_payment_method = QComboBox()

        self.input_fuel_type.addItem("Gasoline")
        self.input_fuel_type.addItem("Diesel")
        self.input_fuel_type.addItem("Hydrogen")
        self.input_fuel_type.addItem("Electric")
        self.input_payment_method.addItem("Direct Debit")
        self.input_payment_method.addItem("Manual Payment")

        self.register_btn = QPushButton("Register")

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color:red")

        layout.addWidget(label_first_name)
        layout.addWidget(self.input_first_name)
        layout.addWidget(label_surname)
        layout.addWidget(self.input_surname)
        layout.addWidget(label_customer_type)
        layout.addWidget(self.input_customer_type)
        layout.addWidget(label_student_employee_code)
        layout.addWidget(self.input_student_employee_code)
        layout.addWidget(label_tel_number)
        layout.addWidget(self.input_tel_number)
        layout.addWidget(label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(label_license_plate)
        layout.addWidget(self.input_license_plate)
        layout.addWidget(label_brand_name)
        layout.addWidget(self.input_brand_name)
        layout.addWidget(label_fuel_type)
        layout.addWidget(self.input_fuel_type)
        layout.addWidget(label_payment_method)
        layout.addWidget(self.input_payment_method)
        layout.addWidget(self.register_btn)
        layout.addWidget(self.error_label)

        self.register_btn.clicked.connect(self.register_info)

        self.setLayout(layout)

    def register_info(self):
        getcontext().prec = 2
        owner_id = uuid1().bytes
        license_plate = self.input_license_plate.text()
        brand_name = self.input_brand_name.text()
        fuel_type = self.input_fuel_type.currentText()
        payment_method = self.input_payment_method.currentText()

        customer_type = self.input_customer_type.text().upper()
        student_employee_code = self.input_student_employee_code.text()
        discount_rate = 0
        if customer_type == "RUG":
            discount_rate = Decimal(20)
        elif customer_type == "HANZE":
            discount_rate = Decimal(25)
        first_name = self.input_first_name.text()
        surname = self.input_surname.text()
        tel_number = self.input_tel_number.text()
        email = self.input_email.text()
        ###################### Regex Validation ###########################
        if not re.match(r"[a-zA-Z\s]+$", first_name):
            self.error_label.setText("Please Enter Your First Name")
            return

        if not re.match(r"[a-zA-Z\s]+$", surname):
            self.error_label.setText("Please Enter Your Surname")
            return

        if not (customer_type == "RUG" or customer_type == "HANZE"):
            self.error_label.setText(
                "Please Enter Your Work/Study Place:\nHanze or RUG"
            )
            return

        if not re.match(r"^[0-9]{1,6}$", student_employee_code):
            self.error_label.setText(
                "Please Enter Your Student/Employee Code\n(6 digit number)"
            )
            return

        if not re.match(
            r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", tel_number
        ):
            self.error_label.setText("Please Enter Your Tel. Number")
            return

        if not re.match(r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$", email):
            self.error_label.setText("Please Enter A Valid Email Address")
            return

        if not re.match(r"^[A-Z]{1,3}[A-Z]{1,2}[0-9]{1,4}$", license_plate):
            self.error_label.setText(
                "Please Enter A Valid License Plate\ne.g. AAABB1234"
            )
            return

        if not re.match(r"[a-zA-Z\s]+$", brand_name):
            self.error_label.setText("Please Enter Brand Of Car")
            return

        if not re.match(r"[a-zA-Z\s]+$", fuel_type):
            self.error_label.setText("Please Enter Fuel Type Of Car")
            return

        ################################################################
        owner_data = (
            owner_id,
            customer_type,
            student_employee_code,
            discount_rate,
            first_name,
            surname,
            tel_number,
            email,
            payment_method,
        )
        car_data = (license_plate, owner_id, brand_name, fuel_type)
        #################### Database Transactions #####################
        dao = DatabaseDAO("zernike_parking_app")
        dao.register_new_car_owner(owner_data)
        dao.register_new_car(car_data)
        dao.close()

        self.close()


###############################################################


def main():
    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap("./res/logo.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    time.sleep(2)

    registration_window = RegistrationWindow()
    registration_window.show()
    splash.finish(registration_window)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
