# Eventra

Event Management & Ticketing System — Python 3 + Tkinter + MySQL.
Class 12 project by **Aayushi** and **Advik**.

## Features

**Guest**
- Register / Login

**User**
- Browse events in a card grid
- Search by name / category / city
- Book tickets with simulated payment (UPI / Card / Cash)
- View and cancel bookings

**Admin**
- Manage events (add / edit / delete)
- View all users and bookings
- Reports: Revenue, Event-Wise, Popular, User History

## Technologies

Python 3, Tkinter, MySQL, mysql-connector-python, Git

## Project Structure

    Eventra/
    ├── .gitignore
    ├── README.md
    ├── db_config_example.py
    ├── db_config.py             (local only — create yourself)
    ├── schema.sql
    ├── seed_data.sql
    ├── db.py
    ├── auth.py
    ├── events.py
    ├── bookings.py
    ├── reports.py
    ├── theme.py                 (colors, fonts, styles)
    ├── gui_user.py              (login, register, user screens)
    ├── gui_admin.py             (admin screens)
    └── main.py                  (entry point)

## Setup

1. `pip install mysql-connector-python`
2. In MySQL Workbench: `source schema.sql;` then `source seed_data.sql;`
3. `cp db_config_example.py db_config.py` — then edit with your MySQL password
4. `python main.py`

## Default Admin Login

    admin@eventra.com / admin123

## Notes

- Passwords stored as plain text (Class 12 level).
- Payments are simulated — no real gateway used.
- Uses soft-delete for events (status = 'Cancelled').
