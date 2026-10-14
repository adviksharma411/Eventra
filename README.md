# Eventra

A simple **Event Management and Ticketing System** built with **Python 3** and **MySQL**.
Class 12 Computer Science project by **Advik** and **Aayushi**.

---

## About the Project

Eventra lets users browse events, book tickets, and manage their bookings.
Admins can add, update, and delete events, view all users and bookings, and
generate simple reports. Payments are **simulated** (no real gateway).

---

## Features

### Guest
- View all events
- Search events by name, category, or city
- Register a new account
- Login

### User (after login)
- View all events
- Search events
- Book tickets (with simulated payment)
- View my bookings
- Cancel a booking
- Logout

### Admin (after login)
- View all events
- Add new event
- Update existing event
- Delete event
- View all bookings
- View all users
- Reports
  - Total revenue
  - Event-wise bookings
  - Most popular events
  - User booking history
- Logout

---

## Technologies Used

- Python 3
- MySQL Server + MySQL Workbench
- mysql-connector-python
- Git & GitHub

---

## Database Tables

| Table | Purpose |
|---|---|
| `users` | Stores registered users and admins |
| `events` | Stores event details |
| `bookings` | Stores ticket bookings made by users |
| `payments` | Stores simulated payment records |

Database name: `eventra_db`

---

## Project Structure

    Eventra/
    ├── .gitignore
    ├── README.md
    ├── db_config_example.py
    ├── db_config.py
    ├── schema.sql
    ├── seed_data.sql
    ├── db.py
    ├── ui.py
    ├── auth.py
    ├── events.py
    ├── bookings.py
    ├── reports.py
    ├── admin.py
    ├── main.py
    └── test_all.py

---

## Setup Instructions

1. **Clone the repository**

        git clone <repo-url>
        cd Eventra

2. **Install Python dependency**

        pip install mysql-connector-python

3. **Create the database in MySQL**

   Open MySQL Workbench and run:

        source schema.sql;
        source seed_data.sql;

   This creates the `eventra_db` database, all tables, and sample data.

4. **Create your local `db_config.py`**

   Copy `db_config_example.py` to `db_config.py` and fill in your
   MySQL password:

        DB_HOST = "localhost"
        DB_USER = "root"
        DB_PASSWORD = "your_password_here"
        DB_NAME = "eventra_db"

   Note: `db_config.py` is gitignored, so every teammate creates their own.

5. **Run the application**

        python main.py

---

## Default Admin Login

    Email:    admin@eventra.com
    Password: admin123

---

## Notes

- Passwords are stored as plain text (Class 12 level project).
- Payments are simulated — no real payment gateway is used.
- Transaction IDs are auto-generated fake IDs.

---

## Team

- **Advik** — Ubuntu — auth.py, events.py, main.py
- **Aayushi** — Windows — bookings.py, reports.py, admin.py

---

## License

This project is for educational purposes only.
