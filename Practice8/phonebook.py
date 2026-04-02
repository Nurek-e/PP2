from connect import get_connection

def show_menu():
    print("\n1 - Search")
    print("2 - Add / Update")
    print("3 - Show (pagination)")
    print("4 - Delete")
    print("5 - Exit")

def search():
    conn = get_connection()
    cur = conn.cursor()

    pattern = input("Enter search: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()

def upsert():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Name: ")
    phone = input("Phone: ")

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()

    conn.close()

def show_paginated():
    conn = get_connection()
    cur = conn.cursor()

    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()

def delete():
    conn = get_connection()
    cur = conn.cursor()

    value = input("Enter name or phone: ")

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    conn.close()

def main():
    while True:
        show_menu()
        choice = input("Choose: ")

        if choice == "1":
            search()
        elif choice == "2":
            upsert()
        elif choice == "3":
            show_paginated()
        elif choice == "4":
            delete()
        elif choice == "5":
            break

main()