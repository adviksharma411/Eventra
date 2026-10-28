from db import get_connection


def total_revenue():
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT COUNT(*) AS total_bookings,
                   COALESCE(SUM(num_tickets), 0) AS total_tickets,
                   COALESCE(SUM(total_amount), 0) AS total_revenue
            FROM bookings WHERE booking_status = 'Confirmed'
        """)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def event_wise_bookings():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT e.event_id, e.event_name,
                   COUNT(b.booking_id) AS bookings,
                   COALESCE(SUM(b.num_tickets), 0) AS tickets,
                   COALESCE(SUM(b.total_amount), 0) AS revenue
            FROM events e
            LEFT JOIN bookings b ON e.event_id = b.event_id
                                 AND b.booking_status = 'Confirmed'
            GROUP BY e.event_id, e.event_name
            ORDER BY revenue DESC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def most_popular_events(limit=5):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT e.event_name, COALESCE(SUM(b.num_tickets), 0) AS tickets_sold
            FROM events e
            LEFT JOIN bookings b ON e.event_id = b.event_id
                                 AND b.booking_status = 'Confirmed'
            GROUP BY e.event_id, e.event_name
            ORDER BY tickets_sold DESC LIMIT %s
        """, (limit,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def user_booking_history(user_id):
    conn = get_connection()
    if conn is None:
        return None, []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, email FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return None, []
        cursor.execute("""
            SELECT b.booking_id, e.event_name, b.num_tickets, b.total_amount,
                   b.booking_date, b.booking_status
            FROM bookings b
            JOIN events e ON b.event_id = e.event_id
            WHERE b.user_id = %s ORDER BY b.booking_date DESC
        """, (user_id,))
        history = cursor.fetchall()
        user["total_bookings"] = len(history)
        user["total_spent"] = sum(float(h["total_amount"]) for h in history
                                  if h["booking_status"] == "Confirmed")
        return user, history
    finally:
        cursor.close()
        conn.close()