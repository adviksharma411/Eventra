import datetime
from db import get_connection


def simulate_payment(amount, booking_id):
    return "TXN" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def book_ticket(user_id, event_id, num_tickets, payment_mode):
    if num_tickets <= 0:
        return False, "Number of tickets must be at least 1."

    conn = get_connection()
    if conn is None:
        return False, "DB connection failed."
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM events WHERE event_id = %s AND status = 'Active'",
            (event_id,)
        )
        event = cursor.fetchone()
        if not event:
            return False, "Event not found or inactive."
        if event["available_seats"] < num_tickets:
            return False, f"Only {event['available_seats']} seats available."

        total = float(event["ticket_price"]) * num_tickets

        cursor.execute("""
            INSERT INTO bookings (user_id, event_id, num_tickets, total_amount, booking_status)
            VALUES (%s, %s, %s, %s, 'Confirmed')
        """, (user_id, event_id, num_tickets, total))
        booking_id = cursor.lastrowid

        txn = simulate_payment(total, booking_id)

        cursor.execute("""
            INSERT INTO payments (booking_id, amount, payment_mode, payment_status, transaction_id)
            VALUES (%s, %s, %s, 'Success', %s)
        """, (booking_id, total, payment_mode, txn))

        cursor.execute(
            "UPDATE events SET available_seats = available_seats - %s WHERE event_id = %s",
            (num_tickets, event_id)
        )
        conn.commit()
        return True, {
            "booking_id": booking_id,
            "txn_id": txn,
            "total": total,
            "event_name": event["event_name"]
        }
    except Exception as e:
        conn.rollback()
        return False, f"Booking failed: {e}"
    finally:
        cursor.close()
        conn.close()


def my_bookings(user_id):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT b.booking_id, e.event_name, b.num_tickets, b.total_amount,
                   b.booking_date, b.booking_status
            FROM bookings b
            JOIN events e ON b.event_id = e.event_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        """, (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def cancel_booking(user_id, booking_id):
    conn = get_connection()
    if conn is None:
        return False, "DB connection failed."
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM bookings WHERE booking_id = %s AND user_id = %s",
            (booking_id, user_id)
        )
        booking = cursor.fetchone()
        if not booking:
            return False, "Booking not found."
        if booking["booking_status"] == "Cancelled":
            return False, "Already cancelled."

        cursor.execute("UPDATE bookings SET booking_status = 'Cancelled' "
                       "WHERE booking_id = %s", (booking_id,))
        cursor.execute("UPDATE payments SET payment_status = 'Refunded' "
                       "WHERE booking_id = %s", (booking_id,))
        cursor.execute("UPDATE events SET available_seats = available_seats + %s "
                       "WHERE event_id = %s",
                       (booking["num_tickets"], booking["event_id"]))
        conn.commit()
        return True, f"Booking #{booking_id} cancelled. {booking['num_tickets']} seats released."
    except Exception as e:
        conn.rollback()
        return False, f"Cancel failed: {e}"
    finally:
        cursor.close()
        conn.close()