from json import load
from mysql.connector import MySQLConnection, Error
from collections import namedtuple
from random import choice


class DatabaseDAO:
    def __init__(self, user):
        self.connection_object = None
        config = self.__read_db_config()[user]
        if config is not None:
            try:
                self.connection_object = MySQLConnection(
                    host=config["hostname"],
                    user=config["username"],
                    passwd=config["password"],
                    db=config["database"],
                    auth_plugin="mysql_native_password",
                )
                if self.connection_object.is_connected():
                    print("Connection: Successful.")
                else:
                    print("Connection: Failure.")
            except Error as err:
                print("Error Code:", err.errno)
                print("SQLSTATE:", err.sqlstate)
                print("Message:", err.msg)
        else:
            print("No configuration data.")

    def __enter__(self):
        return self

    def __read_db_config(self, filename="dbconfig.json"):
        config_data = None

        with open(filename, "r") as file:
            config_data = load(file)

        return config_data

    def populate_parking_lot(self, arg):
        if self.connection_object is None:
            print("No connection")
            return
        if type(arg) is not tuple:
            print("Invalid input, must be a tuple")
            return
        select_parking_lot_capacity = """SELECT capacity_all, capacity_charging from ParkingLot WHERE name = %s"""
        insert_parking_spaces = """
                                    INSERT INTO ParkingSpace(space_id, lot_id, space_type, sensor_id, is_occupied, hourly_tariff) 
                                        VALUES (%s, (SELECT lot_id FROM ParkingLot LIMIT 1), %s, %s, 0, %s)
                                """
        insert_parking_lot = """INSERT INTO `ParkingLot`(`lot_id`, `name`, `location`, `capacity_all`, `capacity_charging`) VALUES (UUID_TO_BIN(UUID()), %s,"Nettelbosje 2, 9747 AD Groningen", 60, 10)"""
        cursor = self.connection_object.cursor(named_tuple=True)

        try:
            cursor.execute(insert_parking_lot, arg)
            cursor.execute(select_parking_lot_capacity, arg)
            row = cursor.fetchone()
            capacity_all = row.capacity_all
            capacity_charging = row.capacity_charging
            ParkingSpace = namedtuple(
                "ParkingSpace", "space_id space_type sensor_id hourly_tariff"
            )
            for i in range(capacity_all):
                if i < capacity_all - capacity_charging:
                    space_data = ParkingSpace(
                        space_id=i,
                        space_type="non_charging",
                        sensor_id=i,
                        hourly_tariff=1.20,
                    )
                    cursor.execute(insert_parking_spaces, space_data)
                else:
                    space_data = ParkingSpace(
                        space_id=i,
                        space_type="charging",
                        sensor_id=i,
                        hourly_tariff=1.32,
                    )
                    cursor.execute(insert_parking_spaces, space_data)
            print("Executed")
            self.connection_object.commit()
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()

    def register_new_car(self, args):
        if self.connection_object is None:
            print("No connection")
            return
        """ 
        The parameter - args, must be a tuple which contains the necessary information for registration of a Car:
        args[0] - license_plate
        args[1] - owner_id
        args[2] - brand_name
        args[3] - fuel_type
        """

        if type(args) is not tuple:
            print("Invalid input, must be a tuple")
            return

        cursor = self.connection_object.cursor()
        duplication_check_query = """SELECT EXISTS(SELECT license_plate FROM Car WHERE license_plate =%s)"""
        insert_query = """INSERT IGNORE INTO Car (license_plate, owner_id, brand_name, fuel_type) VALUES(%s, %s, %s, %s)"""
        try:
            # cursor.execute(duplication_check_query, (args[0],))
            # if all(cursor.fetchone()):
            #     print(
            #         "Unsuccessful: There is an already registered car with the entered license plate."
            #     )
            #     cursor.close()
            #     return

            cursor.execute(insert_query, args)
            print(
                cursor.rowcount,
                "row/rows inserted successfully into Car table.",
            )
            self.connection_object.commit()
            cursor.close()
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()

    def register_new_car_owner(self, args):
        if self.connection_object is None:
            print("No connection")
            return
        """ 
        The parameter - args, must be a tuple which contains the necessary information for registration of a Car Owner:
        args[0] - owner_id
        args[1] - customer_type
        args[2] - student_employee_code
        args[3] - discount_rate
        args[4] - first_name 
        args[5] - surname
        args[6] - tel_number
        args[7] - email
        args[8] - payment_method 
        """

        if type(args) is not tuple:
            print("Invalid input, must be a tuple")
            return

        cursor = self.connection_object.cursor()
        insert_query = """INSERT INTO CarOwner (owner_id, customer_type, student_employee_code, discount_rate, first_name, surname, tel_number, email, payment_method)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            cursor.execute(insert_query, args)
            print(
                cursor.rowcount,
                "row/rows inserted successfully into CarOwner table.",
            )
            self.connection_object.commit()
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()

    def create_new_car_record(self, args):
        if self.connection_object is None:
            print("No connection")
            return
        """ 
        The parameter - args, must be a tuple which contains the necessary information for registration of a Car Owner:
        args[0] - record_id
        args[1] - license_plate
        args[2] - space_id
        args[3] - check_in
        """
        if type(args) is not tuple:
            print("Invalid input, must be a tuple")
            return

        cursor = self.connection_object.cursor()
        insert_query = """INSERT INTO CarRecord (record_id, license_plate, space_id, check_in, is_paid) VALUES(%s, %s, %s, %s, 0)"""
        try:
            cursor.execute(insert_query, args)
            print(
                cursor.rowcount,
                "row/rows inserted successfully into CarRecord table.",
            )
            self.connection_object.commit()
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()

    def occupy_parking_space(self, space_id):
        if self.connection_object is None:
            print("No connection")
            return
        arg = (space_id,)
        cursor = self.connection_object.cursor()
        update_query = (
            """UPDATE ParkingSpace SET is_occupied = 1 WHERE space_id = %s"""
        )
        try:
            cursor.execute(update_query, arg)
            self.connection_object.commit()
            print("Succesfully occupied parking space")
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()

    def get_parking_lots_free_spaces(self):
        if self.connection_object is None:
            print("No connection")
            return
        cursor = self.connection_object.cursor(named_tuple=True)
        select_query = """SELECT name,
                                COUNT(IF(space_type = 'non_charging', 1, NULL)) 'non_charging',
                                COUNT(IF(space_type = 'charging', 1, NULL)) 'charging'
                                    FROM (
                                        SELECT pl.lot_id, pl.name, pl.location, pl.capacity_all, pl.capacity_charging, ps.space_id, ps.space_type, ps.is_occupied 
                                            FROM ParkingLot pl 
                                                INNER JOIN ParkingSpace ps 
                                                    ON pl.lot_id = ps.lot_id) pl_ps
                                    WHERE pl_ps.is_occupied = 0
                                GROUP BY name
                            """
        try:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            result = []
            for index, row in enumerate(rows):
                print(
                    "Parking Lot - %s, has %d non-charging and %d charging, free spaces"
                    % (row.name, row.non_charging, row.charging)
                )
                result.insert(index, [row.name, row.non_charging, row.charging])
            return result
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()

    def get_random_parking_space(self, fuel_type):
        if self.connection_object is None:
            print("No connection")
            return
        free_spaces = None
        if fuel_type == "Electric":
            arg = ("charging",)
        else:
            arg = ("non_charging",)
        cursor = self.connection_object.cursor()
        get_random_space_query = """SELECT space_id FROM ParkingSpace WHERE is_occupied = 0 AND space_type = %s"""
        try:
            cursor.execute(get_random_space_query, arg)
            free_spaces = cursor.fetchall()
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()
            return choice(free_spaces)

    def get_currently_parked_cars(self):
        if self.connection_object is None:
            print("No connection")
            return
        checked_in_records = None
        cursor = self.connection_object.cursor()
        select_query = """SELECT
                            rc.license_plate, rc.brand_name, o.first_name, o.surname, rc.space_id, rc.check_in, o.discount_rate
                        FROM
                            (
                            SELECT r.license_plate, c.brand_name, c.owner_id, r.space_id, r.check_in
                            FROM
                                CarRecord r
                            INNER JOIN Car c 
                                ON r.license_plate = c.license_plate AND r.check_out is NULL
                        ) rc
                        LEFT JOIN CarOwner o USING(owner_id)"""
        try:
            cursor.execute(select_query)
            checked_in_records = cursor.fetchall()
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()
            return checked_in_records

    def check_out_car(self, license_plate, space_id, check_out, discount_rate):
        if self.connection_object is None:
            print("No connection")
            return

        cursor = self.connection_object.cursor()
        update_parking_space_query = (
            """UPDATE ParkingSpace SET is_occupied = 0 WHERE space_id = %s"""
        )
        update_car_record_query = (
            """UPDATE CarRecord SET check_out = %s WHERE license_plate = %s"""
        )
        update_discount_query = """UPDATE CarOwner SET discount_rate = %s WHERE owner_id = (SELECT owner_id FROM Car WHERE license_plate = %s)"""
        try:
            cursor.execute(update_parking_space_query, (space_id,))
            cursor.execute(update_car_record_query, (check_out, license_plate))
            cursor.execute(
                update_discount_query, (discount_rate, license_plate)
            )
            self.connection_object.commit()
            cursor.close()
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()

    def get_parking_spaces(self):
        if self.connection_object is None:
            print("No connection")
            return
        parking_spaces = None
        cursor = self.connection_object.cursor()
        select_query = """SELECT space_id, is_occupied FROM ParkingSpace"""
        try:
            cursor.execute(select_query)
            parking_spaces = cursor.fetchall()
        except Error as err:
            self.connection_object.rollback()
            print("Error Code:", err.errno)
            print("SQLSTATE:", err.sqlstate)
            print("Message:", err.msg)
        finally:
            cursor.close()
            return parking_spaces

    def close(self):
        if (
            self.connection_object is not None
            and self.connection_object.is_connected
        ):
            self.connection_object.close()
            self.connection_object = None
            print("Connection: Closed")

    def __exit__(self, exc_type, exc_value, traceback):
        if (
            self.connection_object is not None
            and self.connection_object.is_connected
        ):
            self.connection_object.close()
            self.connection_object = None
            print("Connection: Closed")
