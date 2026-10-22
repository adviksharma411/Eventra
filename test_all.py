# test_all.py - End-to-end test of the whole setup
# Tests: connection, read, write, update, and display

from db import get_connection
import ui


def test_connection():
    """Test 1: Can we connect to MySQL?"""
    ui.print_line()
    print("TEST 1: Database Connection")
    ui.print_line()
    conn = get_connection()
    if conn and conn.is_connected():
        ui.print_success("Connected to Eventra database!")
        return conn
    else:
        ui.print_error("Connection failed. Check db_config.py")
        return None


def test_read_events(conn):
    """Test 2: Read existing events."""
    ui.print_line()
    print("TEST 2: Reading Events from Database")
    ui.print_line()
    cursor = conn.cursor()
    cursor.execute("SELECT event_id, event_name, city, ticket_price, available_seats FROM events")
    rows = cursor.fetchall()
    if not rows:
        ui.print_info("No events found in database.")
    else:
        print(f"{'ID':<5}{'Event Name':<25}{'City':<12}{'Price':<10}{'Seats':<8}")
        ui.print_line()
        for row in rows:
            print(f"{row[0]:<5}{row[1]:<25}{row[2]:<12}{row[3]:<10}{row[4]:<8}")
    cursor.close()


def test_insert_event(conn):
    """Test 3: Insert a new event."""
    ui.print_line()
    print("TEST 3: Inserting a New Event")
    ui.print_line()
    cursor = conn.cursor()
    sql = """INSERT INTO events
             (event_name, category, description, venue, city, event_date,
              start_time, total_seats, available_seats, ticket_price, organizer_id)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (
        "Test Event - Code Verification",
        "Technology",
        "Inserted by test_all.py to verify the pipeline",
        "Test Venue",
        "Test City",
        "2025-12-31",
        "18:00:00",
        50, 50, 199.00, 1
    )
    cursor.execute(sql, values)
    conn.commit()
    ui.print_success(f"Inserted event ID: {cursor.lastrowid}")
    cursor.close()


def test_read_users(conn):
    """Test 4: Read users from database."""
    ui.print_line()
    print("TEST 4: Reading Users from Database")
    ui.print_line()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, role FROM users")
    rows = cursor.fetchall()
    if not rows:
        ui.print_info("No users found.")
    else:
        print(f"{'ID':<5}{'Name':<20}{'Email':<30}{'Role':<10}")
        ui.print_line()
        for row in rows:
            print(f"{row[0]:<5}{row[1]:<20}{row[2]:<30}{row[3]:<10}")
    cursor.close()


def test_booking_count(conn):
    """Test 5: Count bookings (may be 0, that's fine)."""
    ui.print_line()
    print("TEST 5: Booking Count")
    ui.print_line()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bookings")
    count = cursor.fetchone()[0]
    ui.print_info(f"Total bookings in database: {count}")
    cursor.close()


def main():
    ui.print_banner()
    print("\nRunning full pipeline test...\n")

    # Test 1
    conn = test_connection()
    if not conn:
        return

    # Test 2
    test_read_events(conn)

    # Test 3
    test_insert_event(conn)

    # Test 4
    test_read_users(conn)

    # Test 5
    test_booking_count(conn)

    # Re-read events to show the new one
    print("\nRe-reading events after insertion:")
    test_read_events(conn)

    conn.close()
    ui.print_line()
    ui.print_success("All tests complete! Pipeline is working.")
    ui.print_line()


if __name__ == "__main__":
    main()