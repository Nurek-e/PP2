import psycopg2
import csv
from config import load_config


def connect_db():
    config = load_config()
    conn = psycopg2.connect(**config)
    return conn


def create_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table is ready!")


def insert_from_csv():
    conn = connect_db()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            phone = row[1]

            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Contacts imported from CSV!")


def insert_from_console():
    conn = connect_db()
    cur = conn.cursor()

    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added!")


def show_contacts():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def update_contact():
    conn = connect_db()
    cur = conn.cursor()

    name = input("Enter the name of contact to update: ")
    new_phone = input("Enter new phone: ")

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()

    if cur.rowcount == 0:
        print("Contact not found.")
    else:
        print("Contact updated!")

    cur.close()
    conn.close()


def search_contact():
    conn = connect_db()
    cur = conn.cursor()

    print("1 - Search by exact name")
    print("2 - Search by phone prefix")
    choice = input("Choose option: ")

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE name = %s",
            (name,)
        )

    elif choice == "2":
        prefix = input("Enter phone prefix: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (prefix + "%",)
        )

    else:
        print("Wrong option.")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()

    if len(rows) == 0:
        print("No matching contacts found.")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def delete_contact():
    conn = connect_db()
    cur = conn.cursor()

    print("1 - Delete by name")
    print("2 - Delete by phone")
    choice = input("Choose option: ")

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "DELETE FROM phonebook WHERE name = %s",
            (name,)
        )

    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute(
            "DELETE FROM phonebook WHERE phone = %s",
            (phone,)
        )

    else:
        print("Wrong option.")
        cur.close()
        conn.close()
        return

    conn.commit()

    if cur.rowcount == 0:
        print("Contact not found.")
    else:
        print("Contact deleted!")

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1 - Create table")
        print("2 - Upload from CSV")
        print("3 - Add from console")
        print("4 - Show contacts")
        print("5 - Update contact")
        print("6 - Search contact")
        print("7 - Delete contact")
        print("0 - Exit")

        choice = input("Select option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            show_contacts()
        elif choice == "5":
            update_contact()
        elif choice == "6":
            search_contact()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Wrong choice. Try again.")


menu()