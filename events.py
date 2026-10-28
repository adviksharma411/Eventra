from db import get_connection


def list_events(only_active=True):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        q = "SELECT * FROM events"
        if only_active:
            q += " WHERE status = 'Active'"
        q += " ORDER BY event_date"
        cursor.execute(q)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def search_events(keyword, by="name"):
    field = {"name": "event_name", "category": "category", "city": "city"}.get(by, "event_name")
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            f"SELECT * FROM events WHERE {field} LIKE %s AND status = 'Active' "
            "ORDER BY event_date", (f"%{keyword}%",)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_event(event_id):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def add_event(organizer_id, data):
    conn = get_connection()
    if conn is None:
        return False, "DB connection failed."
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO events
            (event_name, category, description, venue, city, event_date,
             start_time, total_seats, available_seats, ticket_price,
             organizer_id, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Active')
        """, (
            data["event_name"], data["category"], data["description"],
            data["venue"], data["city"], data["event_date"], data["start_time"],
            data["total_seats"], data["total_seats"], data["ticket_price"],
            organizer_id
        ))
        conn.commit()
        return True, cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return False, f"Failed: {e}"
    finally:
        cursor.close()
        conn.close()


def update_event(event_id, field, value):
    allowed = {"event_name", "category", "description", "venue", "city",
               "event_date", "start_time", "total_seats", "ticket_price", "status"}
    if field not in allowed:
        return False, "Invalid field."
    conn = get_connection()
    if conn is None:
        return False, "DB connection failed."
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE events SET {field} = %s WHERE event_id = %s",
                       (value, event_id))
        conn.commit()
        return cursor.rowcount > 0, "Updated" if cursor.rowcount else "Not found"
    except Exception as e:
        conn.rollback()
        return False, f"Failed: {e}"
    finally:
        cursor.close()
        conn.close()


def delete_event(event_id):
    conn = get_connection()
    if conn is None:
        return False, "DB connection failed."
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE events SET status = 'Cancelled' WHERE event_id = %s",
                       (event_id,))
        cursor.execute(
            "UPDATE bookings SET booking_status = 'Cancelled' "
            "WHERE event_id = %s AND booking_status = 'Confirmed'", (event_id,)
        )
        conn.commit()
        return True, "Event cancelled. Related bookings marked cancelled."
    except Exception as e:
        conn.rollback()
        return False, f"Failed: {e}"
    finally:
        cursor.close()
        conn.close()