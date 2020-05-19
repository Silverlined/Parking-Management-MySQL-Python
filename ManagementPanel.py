from PyQt5.QtWidgets import (
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGridLayout,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QApplication,
    QSplashScreen,
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, qApp
import PyQt5.QtGui
import sys, time
from mysql.connector import MySQLConnection, Error
from uuid import uuid1
from datetime import datetime
from DatabaseDAO import DatabaseDAO


class ManagementPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        widget = QWidget()
        widget.setStyleSheet("background:#467f90")
        layout_horizontal = QHBoxLayout()
        menu_vertical_layout = QVBoxLayout()

        self.btn_home = QPushButton("Lot\nOverview")
        self.btn_add = QPushButton("Car\nRegistration")
        self.btn_manage = QPushButton("Manage\nMenu")

        menu_vertical_layout.setContentsMargins(0, 0, 0, 0)
        menu_vertical_layout.setSpacing(0)
        self.btn_home.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white"
        )
        self.btn_add.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white"
        )
        self.btn_manage.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white"
        )

        self.btn_home.clicked.connect(self.show_overview_menu)
        self.btn_add.clicked.connect(self.show_add_menu)
        self.btn_manage.clicked.connect(self.show_manage_menu)

        menu_frame = QFrame()
        menu_vertical_layout.addWidget(self.btn_home)
        menu_vertical_layout.addWidget(self.btn_add)
        menu_vertical_layout.addWidget(self.btn_manage)
        menu_vertical_layout.addStretch()
        menu_frame.setLayout(menu_vertical_layout)
        # menu_frame.setMinimumWidth(200)
        # menu_frame.setMaximumHeight(200)

        parent_vertical = QVBoxLayout()
        parent_vertical.setContentsMargins(0, 0, 0, 0)
        self.vertical_1 = QVBoxLayout()
        self.overview_menu()
        self.vertical_2 = QVBoxLayout()
        self.vertical_2.setContentsMargins(0, 0, 0, 0)
        self.add_menu()

        self.vertical_3 = QVBoxLayout()
        self.vertical_3.setContentsMargins(0, 0, 0, 0)
        self.manage_menu()

        self.frame_1 = QFrame()
        self.frame_1.setMinimumWidth(self.width())
        self.frame_1.setMaximumWidth(self.width())
        self.frame_1.setMinimumHeight(self.height())
        self.frame_1.setMaximumHeight(self.height())

        self.frame_1.setLayout(self.vertical_1)
        self.frame_2 = QFrame()
        self.frame_2.setLayout(self.vertical_2)
        self.frame_3 = QFrame()
        self.frame_3.setLayout(self.vertical_3)

        parent_vertical.addWidget(self.frame_1)
        parent_vertical.addWidget(self.frame_2)
        parent_vertical.addWidget(self.frame_3)

        layout_horizontal.addWidget(menu_frame)
        layout_horizontal.addLayout(parent_vertical)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        parent_vertical.setContentsMargins(0, 0, 0, 0)
        parent_vertical.addStretch()
        # menu_vertical_layout.addStretch()
        layout_horizontal.addStretch()
        widget.setLayout(layout_horizontal)

        self.frame_1.show()
        self.frame_2.hide()
        self.frame_3.hide()

        self.setCentralWidget(widget)

    def show_add_menu(self):
        self.btn_home.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white"
        )
        self.btn_add.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white"
        )
        self.btn_manage.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white"
        )

        self.frame_1.hide()
        self.frame_3.hide()
        self.frame_2.show()

    def add_menu(self):
        layout = QVBoxLayout()
        frame = QFrame()

        license_plate_label = QLabel("License Plate: ")
        license_plate_label.setStyleSheet(
            "color:#fff;padding:8px 0px;font-size:20px"
        )
        brand_name_label = QLabel("Brand: ")
        brand_name_label.setStyleSheet(
            "color:#fff;margin-top:32px;padding:8px 0px;font-size:20px"
        )
        fuel_type_label = QLabel("Fuel: ")
        fuel_type_label.setStyleSheet(
            "color:#fff;margin-top:32px;padding:8px 0px;font-size:20px"
        )

        license_plate_input = QLineEdit()
        license_plate_input.setStyleSheet(
            "color:#fff;padding:8px 0px;font-size:20px"
        )
        brand_name_input = QLineEdit()
        brand_name_input.setStyleSheet(
            "color:#fff;padding:8px 0px;font-size:20px"
        )
        fuel_type_input = QComboBox()
        fuel_type_input.setStyleSheet(
            "color:#fff;padding:8px 0px;font-size:20px;border:1px solid white"
        )
        fuel_type_input.addItem("Gasoline")
        fuel_type_input.addItem("Diesel")
        fuel_type_input.addItem("Hydrogen")
        fuel_type_input.addItem("Electric")

        button = QPushButton("Check-in")
        button.setStyleSheet(
            "color:#fff;margin-top:32px;padding:8px 0px;font-size:20px;background:blue;border:1px solid white"
        )

        layout.addWidget(license_plate_label)
        layout.addWidget(license_plate_input)
        layout.addWidget(brand_name_label)
        layout.addWidget(brand_name_input)
        layout.addWidget(fuel_type_label)
        layout.addWidget(fuel_type_input)
        layout.addWidget(button)

        layout.setContentsMargins(0, 0, 0, 0)
        frame.setMinimumHeight(self.height())
        frame.setMinimumWidth(self.width())
        frame.setMaximumHeight(self.width())
        frame.setMaximumWidth(self.width())

        layout.addStretch()
        frame.setLayout(layout)
        button.clicked.connect(
            lambda: self.add_car_db(
                license_plate_input.text(),
                brand_name_input.text(),
                fuel_type_input.currentText(),
            )
        )
        self.vertical_2.addWidget(frame)

    def add_car_db(self, license_plate, brand_name, fuel_type):
        owner_id = None
        record_id = uuid1().bytes
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        with DatabaseDAO("ticket_booth") as dao:
            space_id = dao.get_random_parking_space(fuel_type)[0]
            car_data = (license_plate, owner_id, brand_name, fuel_type)
            record_data = (record_id, license_plate, space_id, formatted_date)
            dao.register_new_car(car_data)
            dao.create_new_car_record(record_data)
            dao.occupy_parking_space(space_id)

    def show_manage_menu(self):
        self.btn_home.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white"
        )
        self.btn_add.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white"
        )
        self.btn_manage.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white"
        )

        self.frame_1.hide()
        self.frame_2.hide()
        self.frame_3.show()
        self.refresh_manage_menu()

    def manage_menu(self):
        self.table = QTableWidget()
        self.table.setStyleSheet("background:#fff")
        self.table.resize(self.width(), self.height())
        self.table.setColumnCount(7)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("License Plate"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Car Brand"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Owner Name"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Space ID"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Check-in time"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Discount"))
        self.table.setHorizontalHeaderItem(6, QTableWidgetItem("ACTION"))

        self.refresh_manage_menu()

        frame = QFrame()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.table)
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setMaximumWidth(self.width())
        frame.setMinimumWidth(self.width())
        frame.setMaximumHeight(self.height())
        frame.setMinimumHeight(self.height())
        self.vertical_3.addWidget(frame)
        self.vertical_3.addStretch()

    def refresh_manage_menu(self):
        with DatabaseDAO("ticket_booth") as dao:
            data = dao.get_currently_parked_cars()
            self.table.setRowCount(len(data))
        for index, row in enumerate(data):
            self.table.setItem(index, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(index, 1, QTableWidgetItem(str(row[1])))
            if row[2] is not None:
                self.table.setItem(
                    index, 2, QTableWidgetItem(str(row[2]) + " " + str(row[3]))
                )
            else:
                self.table.setItem(index, 2, QTableWidgetItem("VISITOR"))
            self.table.setItem(index, 3, QTableWidgetItem(str(row[4])))
            self.table.setItem(index, 4, QTableWidgetItem(str(row[5])))
            self.discout_drop_down = QComboBox()
            if row[6] is not None:
                self.discout_drop_down.addItem(str(row[6]))
            else:
                self.discout_drop_down.addItem("0")
            self.discout_drop_down.addItem("10")
            self.discout_drop_down.addItem("15")
            self.discout_drop_down.addItem("20")
            self.discout_drop_down.addItem("25")
            self.discout_drop_down.addItem("30")
            self.table.setCellWidget(index, 5, self.discout_drop_down)
            self.button_check_out = QPushButton("Check-out")
            self.button_check_out.setStyleSheet(
                "color:#fff;padding:4px 0px;font-size:16px;background:green;border:1px solid white"
            )
            self.table.setCellWidget(index, 6, self.button_check_out)
            self.button_check_out.clicked.connect(self.check_out_call)

    def check_out_call(self):
        btn = self.sender()
        if btn:
            index = self.table.indexAt(btn.pos()).row()
            license_plate = str(self.table.item(index, 0).text())
            space_id = str(self.table.item(index, 3).text())
            new_discount = self.table.cellWidget(index, 5).currentText()
            check_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with DatabaseDAO("ticket_booth") as dao:
                dao.check_out_car(
                    license_plate, space_id, check_out_time, new_discount
                )
            self.table.removeRow(index)

    def show_overview_menu(self):
        self.btn_home.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:blue;color:#fff;font-weight:bold;border:1px solid white"
        )
        self.btn_add.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white"
        )
        self.btn_manage.setStyleSheet(
            "width:200px;height:160px;font-size:20px;background:orange;color:#fff;font-weight:bold;border:1px solid white"
        )

        self.frame_2.hide()
        self.frame_3.hide()
        self.frame_1.show()
        self.refresh_overview_menu()

    def overview_menu(self):
        self.vertical_1.setContentsMargins(0, 0, 0, 0)

        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        frame = QFrame()

        horizontal = QHBoxLayout()
        horizontal.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addLayout(horizontal)

        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(0)
        vertical_layout.addLayout(self.gridLayout)

        self.refresh_overview_menu()

        frame.setLayout(vertical_layout)
        self.vertical_1.addWidget(frame)
        self.vertical_1.addStretch()

    def refresh_overview_menu(self):
        while self.gridLayout.count():
            child = self.gridLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        data = None
        with DatabaseDAO("ticket_booth") as dao:
            data = dao.get_parking_spaces()
        if data is not None:
            row = 0
            i = 0
            for parking_space in data:
                label = QPushButton("Space\n" + str(parking_space[0]))

                if parking_space[1] == 0:  # Not occupied.
                    label.setStyleSheet(
                        "background-color:green;color:white;padding:5px;width:100px;height:100px;border:1px solid white;text-align:center;font-weight:bold"
                    )
                else:
                    label.setStyleSheet(
                        "background-color:red;color:white;padding:5px;width:100px;height:100px;border:1px solid white;text-align:center;font-weight:bold"
                    )

                if i % 5 == 0:
                    i = 0
                    row = row + 1

                self.gridLayout.addWidget(label, row, i)
                i = i + 1


###############################################################


def main():
    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = PyQt5.QtGui.QPixmap("./res/logo.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    time.sleep(1)

    management_panel = ManagementPanel()
    management_panel.show()
    splash.finish(management_panel)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
