def test_connection():
    from db import get_connection
    conn = get_connection()
    if conn is None:
        print("[FAIL] DB connection")
        return False
    print("[OK]   DB connection")
    conn.close()
    return True

def test_tables():
    from db import get_connection
    conn = get_connection()
    if conn is None:
        return False
    cur = conn.cursor()
    ok = True
    for t in ["users", "events", "bookings", "payments"]:
        try:
            cur.execute(f"SELECT 1 FROM {t} LIMIT 1")
            cur.fetchall()               # <-- consume result
            print(f"[OK]   Table '{t}'")
        except Exception:
            print(f"[FAIL] Table '{t}'")
            ok = False
    cur.close()
    conn.close()
    return ok

def test_imports():
    try:
        import auth, events, bookings, reports
        print("[OK]   Logic modules import")
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False


def test_gui_imports():
    try:
        import gui_user, gui_admin
        print("[OK]   GUI modules import")
        return True
    except ImportError as e:
        print(f"[FAIL] GUI import error: {e}")
        return False


def main():
    print("=" * 55)
    print("EVENTRA — TEST SUITE")
    print("=" * 55)
    results = [test_connection(), test_tables(),
               test_imports(), test_gui_imports()]
    print("=" * 55)
    print("✅ ALL PASSED" if all(results) else "❌ SOME FAILED")


if __name__ == "__main__":
    main()