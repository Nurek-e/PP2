import csv
import json
from connect import get_connection


def run_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()


def setup_database():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    print("Database setup completed.")


def get_group_id(cur, group_name):
    cur.execute(
        """
        INSERT INTO groups(name)
        VALUES(%s)
        ON CONFLICT (name) DO NOTHING
        """,
        (group_name,)
    )

    cur.execute(
        "SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)",
        (group_name,)
    )

    return cur.fetchone()[0]


def add_contact():
    name = input("Enter name: ")
    email = input("Enter email: ")
    birthday = input("Enter birthday YYYY-MM-DD: ")
    group_name = input("Enter group Family/Work/Friend/Other: ")

    conn = get_connection()
    cur = conn.cursor()

    group_id = get_group_id(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES(%s, %s, %s, %s)
        ON CONFLICT (name) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        """,
        (name, email, birthday, group_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added or updated.")


def add_phone():
    name = input("Enter contact name: ")
    phone = input("Enter phone: ")
    phone_type = input("Enter type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL add_phone(%s, %s, %s)",
        (name, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def move_contact_to_group():
    name = input("Enter contact name: ")
    group_name = input("Enter new group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL move_to_group(%s, %s)",
        (name, group_name)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved to group.")


def search():
    query = input("Enter search query: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (query,)
    )

    rows = cur.fetchall()

    print_contacts(rows)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Enter group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE LOWER(g.name) = LOWER(%s)
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.name
        """,
        (group_name,)
    )

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def search_by_email():
    email = input("Enter email part: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.email ILIKE %s
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.name
        """,
        ("%" + email + "%",)
    )

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def sort_contacts():
    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday NULLS LAST"
    else:
        order_by = "c.created_at"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY {order_by}
        """
    )

    rows = cur.fetchall()
    print_contacts(rows)

    cur.close()
    conn.close()


def pagination():
    limit = int(input("Enter page size: "))
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        print_contacts(rows)

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit

        elif command == "prev":
            offset = max(0, offset - limit)

        elif command == "quit":
            break


def export_json():
    filename = input("Enter JSON filename: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
        """
    )

    contacts = cur.fetchall()

    data = []

    for contact in contacts:
        contact_id, name, email, birthday, group_name = contact

        cur.execute(
            """
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s
            """,
            (contact_id,)
        )

        phones = cur.fetchall()

        item = {
            "name": name,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name,
            "phones": [
                {"phone": phone, "type": phone_type}
                for phone, phone_type in phones
            ]
        }

        data.append(item)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    cur.close()
    conn.close()

    print("Export completed.")


def import_json():
    filename = input("Enter JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        name = item["name"]

        cur.execute(
            "SELECT id FROM contacts WHERE LOWER(name) = LOWER(%s)",
            (name,)
        )

        exists = cur.fetchone()

        if exists:
            action = input(f"{name} already exists. skip/overwrite: ")

            if action == "skip":
                continue

            cur.execute(
                "DELETE FROM contacts WHERE LOWER(name) = LOWER(%s)",
                (name,)
            )

        group_id = get_group_id(cur, item.get("group", "Other"))

        cur.execute(
            """
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES(%s, %s, %s, %s)
            RETURNING id
            """,
            (
                item["name"],
                item.get("email"),
                item.get("birthday"),
                group_id
            )
        )

        contact_id = cur.fetchone()[0]

        for phone_item in item.get("phones", []):
            cur.execute(
                """
                INSERT INTO phones(contact_id, phone, type)
                VALUES(%s, %s, %s)
                """,
                (
                    contact_id,
                    phone_item["phone"],
                    phone_item["type"]
                )
            )

    conn.commit()
    cur.close()
    conn.close()

    print("Import completed.")


def import_csv():
    filename = input("Enter CSV filename: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_id = get_group_id(cur, row["group"])

            cur.execute(
                """
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES(%s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                SET email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
                """,
                (
                    row["name"],
                    row["email"],
                    row["birthday"],
                    group_id
                )
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO phones(contact_id, phone, type)
                VALUES(%s, %s, %s)
                """,
                (
                    contact_id,
                    row["phone"],
                    row["type"]
                )
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV import completed.")


def delete_contact():
    name = input("Enter contact name to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE LOWER(name) = LOWER(%s)",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact deleted.")


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    print("\n" + "=" * 120)
    print(f"{'ID':<5} {'Name':<18} {'Email':<25} {'Birthday':<15} {'Group':<12} {'Phones':<40}")
    print("=" * 120)

    for row in rows:
        print(
            f"{row[0]:<5} "
            f"{str(row[1]):<18} "
            f"{str(row[2]):<25} "
            f"{str(row[3]):<15} "
            f"{str(row[4]):<12} "
            f"{str(row[5]):<40}"
        )


def main():
    while True:
        print("\n=== Extended PhoneBook ===")
        print("1. Setup database")
        print("2. Add / Update contact")
        print("3. Add phone")
        print("4. Move contact to group")
        print("5. Search all fields")
        print("6. Filter by group")
        print("7. Search by email")
        print("8. Sort contacts")
        print("9. Pagination")
        print("10. Export JSON")
        print("11. Import JSON")
        print("12. Import CSV")
        print("13. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        try:
            if choice == "1":
                setup_database()

            elif choice == "2":
                add_contact()

            elif choice == "3":
                add_phone()

            elif choice == "4":
                move_contact_to_group()

            elif choice == "5":
                search()

            elif choice == "6":
                filter_by_group()

            elif choice == "7":
                search_by_email()

            elif choice == "8":
                sort_contacts()

            elif choice == "9":
                pagination()

            elif choice == "10":
                export_json()

            elif choice == "11":
                import_json()

            elif choice == "12":
                import_csv()

            elif choice == "13":
                delete_contact()

            elif choice == "0":
                break

            else:
                print("Invalid choice.")

        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()