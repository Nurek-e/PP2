from connect import get_connection
import csv
def show_contacts():
    limit = 5
    page = int(input("Enter page number: "))
    offset = (page - 1) * limit

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s",
        (limit, offset)
    )

    rows = cur.fetchall()

    if not rows:
        print("No data")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added!")


def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Updated!")

def search_contact():
    value = input("Enter name or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE name ILIKE %s OR phone LIKE %s",
        ('%' + value + '%', '%' + value + '%')
    )

    rows = cur.fetchall()

    if not rows:
        print("Not found")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()

def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE name = %s OR phone = %s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!")


def import_csv():
    filename = input("Enter CSV file name: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported!")


def main():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1 - Show contacts (pagination)")
        print("2 - Add contact")
        print("3 - Update contact")
        print("4 - Search contact")
        print("5 - Delete contact")
        print("6 - Import CSV")
        print("7 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            show_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            import_csv()
        elif choice == "7":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()