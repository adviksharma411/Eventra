# Eventra - Event Management and Ticketing System

A Python + MySQL based application for managing events and booking tickets.

## Team
- Aayushi
- Advik

## Setup Instructions
1. Install Python 3.10+ and MySQL 8.0
2. Run `pip install mysql-connector-python`
3. Run `schema.sql` in MySQL to create tables
4. Run `seed_data.sql` to add sample data
5. Copy `db_config_example.py` to `db_config.py` and fill your credentials
6. Run `python main.py`

## Modules
- User Module (register/login/browse/book)
- Admin Module (manage events)
- Booking Module (book/cancel tickets)
- Reports Module (revenue, popular events)
