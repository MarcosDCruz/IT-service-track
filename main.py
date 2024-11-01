import database
import datetime


MENU_PROMPT = """
-----Menu-----

1. Add a New Customer
2. Remove a Customer
3. View last payment date for a customer
4. View late payments
5. Add Services or Equipment
6. Remove Services or Equipment
7. Change cost of Service or Equipment
8. Exit
Enter your choice: 
"""


# add customers - need first, last name and phone number
def prompt_add_customer():
    first_name, last_name = input("Please enter your first and last name: ").split()
    phone_number = input("What is your phone number? ")

    address, city, state = input("Please enter your address, separated by commas (ex. 123 17th St., Knoxville, TN): ").split(",")

    card_info = input("Please type in the last 4 digits on your credit card: ")
    last_payment = input("Please type in the date of your last payment (ex. MM-DD-YYYY)")
    last_payment_date = datetime.datetime.strptime(last_payment, "%m-%d-%Y")
    last_payment_ts = last_payment_date.timestamp()

    database.add_customer(first_name, last_name, phone_number, address, city, state, card_info, last_payment_ts)


# remove customers
def prompt_remove_customer():
    first_name, last_name = input("To remove, please enter your first and last name: ").split()
    phone_number = input("And your phone number: ")

    database.remove_customer(first_name, last_name, phone_number)

# search for cust by name or location and retrieve last payment date


# view all cust late on payment

def view_late_payments():
    thirty_days_in_seconds = datetime.timedelta(days=30).total_seconds()
    today = datetime.datetime.today().timestamp()
    payments = database.view_payments()
    for payment in payments:
        payment_date_from_db = payment[2]
        payment_date = datetime.datetime.strptime(payment_date_from_db, "%Y-%m-%d")
        payment_date_timestamp = payment_date.timestamp()
        if today - payment_date_timestamp >= thirty_days_in_seconds:
            print(f"{payment[0]} {payment[1]: Payment is late!}")
        else:
            print(f"{payment[0]} {payment[1]}: Payment is not late!")


# add services and equipment for a customer
def print_services():
    services = database.view_services()
    print("----Services----")
    [print(f"{service_price[0]}. {service_price[1]} is ${service_price[2]}") for service_price in services]
    print("-----------------")


def print_equipment():
    equipment = database.view_equipment()
    print("----Equipment----")
    [print(f"{equipment_price[0]}. {equipment_price[1]} is ${equipment_price[2]}") for equipment_price in equipment]
    print("-----------------")


def print_locations():
    locations = database.view_locations()
    print("----Locations----")
    [print(f"{location[0]}. {location[1]}, {location[2]}, {location[3]}") for location in locations]
    print("------------------")


def prompt_add_service_or_equipment():
    service_or_equipment = input("Which would you like to do?\n1. Add service\n2. Add Equipment\nChoose: ")
    if service_or_equipment == "1":
        print_services()
        print_locations()
        location_ID, service_ID = input("Please enter the ID associated with the location and service you want (ex. location ID, service ID): ").split(',')
        database.add_services(location_ID,service_ID)
    else:
        print_equipment()
        print_locations()
        location_ID, equipment_ID = input("Please enter the ID associated with the location and equipment you want (location ID, equipment ID): ").split(',')
        database.add_equipment(location_ID,equipment_ID)


# change cost of service/equipment
def prompt_update_price():
    service_or_equipment = input("Which would you like to do?\n1. Update service\n2. Update Equipment\nChoose: ")
    if service_or_equipment == "1":
        print_services()
        service_cost, service_type = input("Enter new price and name of service (ex. 35.99,Internet): ").split(',')
        database.update_service_price(service_cost, service_type)
    else:
        print_equipment()
        equipment_type, equipment_cost = input("Enter new price and name of equipment (ex. 35.99,Router): ").split(',')
        database.update_equipment_price(equipment_type, equipment_cost)


# calculate cost of bill
def calculate_cust_bill():
    pass


MENU_OPTIONS = {
    "1": prompt_add_customer,
    "2": prompt_remove_customer,
    "4": view_late_payments,
    "6": prompt_add_service_or_equipment,
    "8": prompt_update_price
}


def menu():
    database.create_tables()

    while (user_choice := input(MENU_PROMPT)) != "9":
        try:
            MENU_OPTIONS[user_choice]()
        except KeyError:
            print("Invalid input. Please select a list number.")


if __name__ == '__main__':
    menu()


