import sqlite3
import datetime

# <-----------------------------------------------------
# create table commands
CREATE_CUSTOMER = """
CREATE TABLE IF NOT EXISTS Customer
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
first_name VARCHAR(50),
last_name VARCHAR(50),
phone_number VARCHAR(20));"""

CREATE_LOCATIONS = """
CREATE TABLE IF NOT EXISTS Locations
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
customer_ID INTEGER,
address VARCHAR(255),
city VARCHAR(50),
state VARCHAR(2),
FOREIGN KEY (customer_ID) REFERENCES customer(ID) ON DELETE CASCADE);"""

CREATE_EQUIPMENT = """
CREATE TABLE IF NOT EXISTS Equipment
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
equipment_type VARCHAR(50),
equipment_cost DECIMAL(10,2));"""

CREATE_SERVICES = """
CREATE TABLE IF NOT EXISTS Services
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
service_type VARCHAR(50),
service_cost DECIMAL(10,2));"""

CREATE_LOCATIONS_EQUIPMENT = """
CREATE TABLE IF NOT EXISTS LocationsEquipment
(location_ID INTEGER,
equipment_ID INTEGER,
PRIMARY KEY (location_ID, equipment_ID),
FOREIGN KEY (location_ID) REFERENCES Locations(ID) ON DELETE CASCADE,
FOREIGN KEY (equipment_ID) REFERENCES Equipment(ID) ON DELETE CASCADE);"""

CREATE_LOCATIONS_SERVICES = """
CREATE TABLE IF NOT EXISTS LocationsServices
(location_ID INTEGER,
service_ID INTEGER,
PRIMARY KEY (location_ID, service_ID),
FOREIGN KEY (location_ID) REFERENCES Locations(ID) ON DELETE CASCADE,
FOREIGN KEY (service_ID) REFERENCES Services(ID) ON DELETE CASCADE);"""

CREATE_BILLING = """
CREATE TABLE IF NOT EXISTS Billing
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
customer_ID INTEGER,
card_on_file VARCHAR(20),
last_payment_date DATE, # change DATE data type
FOREIGN KEY (customer_ID) REFERENCES Customer(ID) ON DELETE CASCADE);"""

# SELECT statements

SELECT_SERVICES = """SELECT ID, service_type, service_cost FROM Services;"""

SELECT_EQUIPMENT = """SELECT ID, equipment_type, equipment_cost FROM Equipment;"""

SELECT_LOCATIONS = """SELECT ID, address, city, state FROM Locations;"""

SELECT_CUST_AND_BILLING = """SELECT c.first_name, c.last_name, b.last_payment_date
 FROM Customer AS c
 JOIN Billing AS b ON c.ID = b.customer_ID;"""

# INSERT statements

INSERT_CUSTOMER = """INSERT INTO Customer(first_name, last_name, phone_number) VALUES (?,?,?) RETURNING ID;"""

INSERT_CUSTOMER_LOCATION = """INSERT INTO Locations(customer_id, address, city, state) VALUES (?,?,?,?);"""

INSERT_CUSTOMER_BILLING = """INSERT INTO Billing(customer_ID, card_on_file, last_payment_date) VALUES (?,?,?);"""

INSERT_SERVICES_AT_LOCATIONS = """INSERT INTO LocationsServices (location_ID, service_ID) VALUES (?, ?);"""

INSERT_EQUIPMENT_AT_LOCATIONS = """INSERT INTO LocationsEquipment (location_ID, equipment_ID) VALUES (?, ?);"""

# UPDATE statements
UPDATE_SERVICE_PRICE = """UPDATE Services SET service_cost = ? WHERE service_type = ?"""

UPDATE_EQUIPMENT_PRICE = """UPDATE Equipment SET equipment_cost = ? WHERE equipment_type = ?"""

# DELETE Customer
DELETE_CUSTOMER = "DELETE FROM Customer WHERE first_name = ? AND last_name = ? AND phone_number = ?;"

DELETE_CUST_SERVICE = "DELETE FROM LocationsServices WHERE service_ID = ? and location_ID = ?;;"

DELETE_CUST_EQUIPMENT = "DELETE FROM LocationsEquipment WHERE equipment_ID = ? and location_ID = ?;"


# <-----------------------------------------------------

connection = sqlite3.connect("company_tracking_system.db")
connection.execute('PRAGMA foreign_keys = ON')


def create_tables():
    with connection:
        connection.execute(CREATE_CUSTOMER)
        connection.execute(CREATE_LOCATIONS)
        connection.execute(CREATE_EQUIPMENT)
        connection.execute(CREATE_SERVICES)
        connection.execute(CREATE_LOCATIONS_EQUIPMENT)
        connection.execute(CREATE_LOCATIONS_SERVICES)
        connection.execute(CREATE_BILLING)


def add_customer(first_name, last_name, phone_number, address, city, state, card_on_file, last_payment_ts):
    with connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_CUSTOMER, (first_name, last_name, phone_number))
        customer_id = cursor.fetchone()[0]
        cursor.execute(INSERT_CUSTOMER_LOCATION, (customer_id, address, city, state))
        cursor.execute(INSERT_CUSTOMER_BILLING, (customer_id, card_on_file, last_payment_ts))


def remove_customer(first_name, last_name, phone_number):
    with connection:
        connection.execute(DELETE_CUSTOMER, (first_name, last_name, phone_number))


def add_services(location_ID, equipment_ID):
    with connection:
        connection.execute(INSERT_SERVICES_AT_LOCATIONS, (location_ID, equipment_ID))


def add_equipment(location_ID, service_ID):
    with connection:
        connection.execute(INSERT_EQUIPMENT_AT_LOCATIONS, (location_ID, service_ID))


def view_locations():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_LOCATIONS)
        return cursor.fetchall()


def view_services():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_SERVICES)
        return cursor.fetchall()


def view_equipment():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_EQUIPMENT)
        return cursor.fetchall()


def view_payments():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_CUST_AND_BILLING)
        return cursor.fetchall()


def update_service_price(service_cost, service_type):
    with connection:
        connection.execute(UPDATE_SERVICE_PRICE, (service_cost, service_type))


def update_equipment_price(equipment_type, equipment_cost):
    with connection:
        connection.execute(UPDATE_EQUIPMENT_PRICE, (equipment_type, equipment_cost))
