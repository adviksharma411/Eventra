from db import get_connection


def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]


def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10


def register_user(name, email, phone, password):
    name, email = name.strip(), email.strip().lower()
    phone, password = phone.strip(), password.strip()

    if not all([name, email, phone, password]):
        return False, "All fields are required."
    if not is_valid_email(email):
        return False, "Please enter a valid email address."
    if not is_valid_phone(phone):
        return False, "Phone number must be 10 digits."

    conn = get_connection()
    if conn is None:
        return False, "Could not connect to database."
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "Email is already registered."
        cursor.execute(
            "INSERT INTO users (name, email, phone, password, role) "
            "VALUES (%s, %s, %s, %s, 'user')",
            (name, email, phone, password)
        )
        conn.commit()
        return True, cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return False, f"Registration failed: {e}"
    finally:
        cursor.close()
        conn.close()


def login_user(email, password):
    email, password = email.strip().lower(), password.strip()
    if not email or not password:
        return False, "Email and password are required."

    conn = get_connection()
    if conn is None:
        return False, "Could not connect to database."
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT user_id, name, email, role FROM users "
            "WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()
        return (True, user) if user else (False, "Invalid email or password.")
    except Exception as e:
        return False, f"Login failed: {e}"
    finally:
        cursor.close()
        conn.close()