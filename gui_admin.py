import tkinter as tk
from tkinter import ttk, messagebox

from db import get_connection
from events import list_events, search_events, add_event, update_event, delete_event
from reports import (total_revenue, event_wise_bookings,
                     most_popular_events, user_booking_history)

from gui_user import (
    PRIMARY, PRIMARY_DARK, PRIMARY_TINT, ACCENT, ACCENT_LIGHT, ACCENT_DARK,
    SUCCESS, BG, BG_SUBTLE, BG_HOVER, CARD_BG, BORDER, BORDER_STRONG,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_TERTIARY,
    TEXT_DARK, TEXT_LIGHT,
    FONT_TITLE, FONT_SECTION, FONT_H1, FONT_H2,
    FONT_BODY, FONT_SMALL, FONT_TINY, FONT_LABEL, FONT_BUTTON,
    primary_button, secondary_button, accent_button, ghost_button,
    modern_entry, make_navbar, EventCard
)


# ============================================================
# ADMIN EVENTS GRID
# ============================================================

class AdminEventsWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        make_navbar(self.frame, self.app.user, self.app)

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=32, pady=(28, 4))
        title_col = tk.Frame(header, bg=BG)
        title_col.pack(side="left", anchor="w")
        tk.Label(title_col, text="Events", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(title_col, text="Manage every event on Eventra.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(4, 0))

        primary_button(header, "+  Add event",
                       self.app.show_add_event).pack(side="right", pady=8)

        search_row = tk.Frame(self.frame, bg=BG)
        search_row.pack(fill="x", padx=32, pady=(20, 16))
        self.search_var = tk.StringVar()
        sw, ent = modern_entry(search_row, width=44)
        ent.config(textvariable=self.search_var)
        sw.pack(side="left", ipady=0)
        ent.bind("<Return>", lambda e: self._search())
        ghost_button(search_row, "Search", self._search
                     ).pack(side="left", padx=(8, 4))
        ghost_button(search_row, "Reset", self._load_all).pack(side="left")

        cf = tk.Frame(self.frame, bg=BG)
        cf.pack(fill="both", expand=True, padx=32, pady=(0, 20))

        self.canvas = tk.Canvas(cf, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.inner = tk.Frame(self.canvas, bg=BG)
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._on_inner_cfg)
        self.canvas.bind("<Configure>", self._on_canvas_cfg)

        self.frame.bind_all("<MouseWheel>",
                            lambda e: self.canvas.yview_scroll(
                                int(-1 * (e.delta / 120)), "units"))
        self.frame.bind_all("<Button-4>",
                            lambda e: self.canvas.yview_scroll(-2, "units"))
        self.frame.bind_all("<Button-5>",
                            lambda e: self.canvas.yview_scroll(2, "units"))

        self._load_all()

    def _on_inner_cfg(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_cfg(self, event):
        self.canvas.itemconfigure(self._win, width=event.width)

    def _load_all(self):
        self.search_var.set("")
        self._render(list_events(only_active=False))

    def _search(self):
        kw = self.search_var.get().strip()
        self._render(search_events(kw) if kw else list_events(only_active=False))

    def _render(self, events):
        for w in self.inner.winfo_children():
            w.destroy()
        if not events:
            tk.Label(self.inner, text="No events found.",
                     font=FONT_BODY, bg=BG, fg=TEXT_TERTIARY
                     ).grid(row=0, column=0, pady=60, padx=20)
            return
        for i, ev in enumerate(events):
            r, c = divmod(i, 3)
            EventCard(self.inner, ev, on_edit=self._edit,
                      on_delete=self._delete).grid(
                row=r, column=c, padx=8, pady=8, sticky="nsew")
        for c in range(3):
            self.inner.grid_columnconfigure(c, weight=1, minsize=300)

    def _edit(self, ev):
        self.app.show_edit_event(ev)

    def _delete(self, ev):
        if not messagebox.askyesno(
                "Delete event",
                f"Delete '{ev['event_name']}'?\n\n"
                "All its bookings will be cancelled."):
            return
        ok, msg = delete_event(ev["event_id"])
        if ok:
            messagebox.showinfo("Deleted", msg)
            self._load_all()
        else:
            messagebox.showerror("Error", msg)

    def destroy(self):
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.frame.unbind_all(seq)
        self.frame.destroy()


# ============================================================
# ADD / EDIT EVENT FORM
# ============================================================

class AddEditEventForm:
    def __init__(self, root, app, mode="add", event=None):
        self.app = app
        self.mode = mode
        self.event = event
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        make_navbar(self.frame, self.app.user, self.app)

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=32, pady=(28, 18))
        title = "Add event" if self.mode == "add" else "Edit event"
        subtitle = ("Create a new event on Eventra." if self.mode == "add"
                    else f"Updating: {self.event['event_name']}")
        tk.Label(header, text=title, font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(header, text=subtitle, font=FONT_SMALL,
                 bg=BG, fg=TEXT_SECONDARY).pack(anchor="w", pady=(4, 0))

        # Card container
        outer = tk.Frame(self.frame, bg=BG)
        outer.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        card = tk.Frame(outer, bg=CARD_BG,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True)

        form = tk.Frame(card, bg=CARD_BG, padx=28, pady=24)
        form.pack(fill="both", expand=True)

        self.entries = {}
        defs = [
            ("EVENT NAME", "event_name"),
            ("CATEGORY", "category"),
            ("VENUE", "venue"),
            ("CITY", "city"),
            ("DATE (YYYY-MM-DD)", "event_date"),
            ("START TIME (HH:MM)", "start_time"),
            ("TOTAL SEATS", "total_seats"),
            ("TICKET PRICE (₹)", "ticket_price"),
        ]
        for i, (label, key) in enumerate(defs):
            r, c = i // 2, (i % 2) * 2
            tk.Label(form, text=label, font=FONT_LABEL,
                     bg=CARD_BG, fg=TEXT_SECONDARY
                     ).grid(row=r, column=c, sticky="w",
                            pady=(10, 5), padx=(0, 12))
            wrapper, ent = modern_entry(form, width=32)
            wrapper.grid(row=r + 1, column=c, sticky="ew",
                         pady=(0, 12), padx=(0, 24))
            # Note: adding an extra row per field, so shift row counter
            if self.event and key in self.event:
                val = self.event[key]
                if key == "start_time":
                    val = str(val)
                    if len(val) > 5:
                        val = val[:5]
                elif key == "event_date":
                    val = str(val)
                ent.insert(0, str(val))
            self.entries[key] = ent

        # Rebuild using tighter grid — actually simpler to just track rows
        # Cleanup above approach and rewrite
        for w in form.winfo_children():
            w.destroy()

        self.entries = {}
        defs = [
            ("EVENT NAME", "event_name"),
            ("CATEGORY", "category"),
            ("VENUE", "venue"),
            ("CITY", "city"),
            ("DATE (YYYY-MM-DD)", "event_date"),
            ("START TIME (HH:MM)", "start_time"),
            ("TOTAL SEATS", "total_seats"),
            ("TICKET PRICE (₹)", "ticket_price"),
        ]
        for i, (label, key) in enumerate(defs):
            col = i % 2
            row = (i // 2) * 2
            tk.Label(form, text=label, font=FONT_LABEL,
                     bg=CARD_BG, fg=TEXT_SECONDARY
                     ).grid(row=row, column=col, sticky="w",
                            pady=(10, 5), padx=(0, 24))
            wrapper, ent = modern_entry(form, width=32)
            wrapper.grid(row=row + 1, column=col, sticky="ew",
                         pady=(0, 12), padx=(0, 24))
            if self.event and key in self.event:
                val = self.event[key]
                if key == "start_time":
                    val = str(val)[:5]
                elif key == "event_date":
                    val = str(val)
                ent.insert(0, str(val))
            self.entries[key] = ent

        # Description
        desc_row = (len(defs) // 2) * 2
        tk.Label(form, text="DESCRIPTION", font=FONT_LABEL,
                 bg=CARD_BG, fg=TEXT_SECONDARY
                 ).grid(row=desc_row, column=0, columnspan=2,
                        sticky="w", pady=(14, 5))
        desc_wrapper = tk.Frame(form, bg=BORDER_STRONG, padx=1, pady=1)
        desc_wrapper.grid(row=desc_row + 1, column=0, columnspan=2,
                          sticky="ew", pady=(0, 12))
        self.desc = tk.Text(desc_wrapper, font=FONT_BODY, bd=0, relief="flat",
                            height=4, bg=CARD_BG, fg=TEXT_PRIMARY,
                            insertbackground=TEXT_PRIMARY, wrap="word")
        self.desc.pack(fill="x", ipady=6, padx=11, pady=2)
        self.desc.bind("<FocusIn>",
                       lambda e: desc_wrapper.config(bg=PRIMARY))
        self.desc.bind("<FocusOut>",
                       lambda e: desc_wrapper.config(bg=BORDER_STRONG))
        if self.event and self.event["description"]:
            self.desc.insert("1.0", self.event["description"])

        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        # Error label
        self.err = tk.Label(form, text="", font=FONT_SMALL,
                             bg=CARD_BG, fg=ACCENT)
        self.err.grid(row=desc_row + 2, column=0, columnspan=2,
                      sticky="w", pady=(4, 12))

        # Buttons
        btn_row = tk.Frame(form, bg=CARD_BG)
        btn_row.grid(row=desc_row + 3, column=0, columnspan=2,
                     sticky="w", pady=(6, 0))
        primary_button(btn_row,
                       "Save event" if self.mode == "add" else "Update event",
                       self._save).pack(side="left", padx=(0, 8))
        secondary_button(btn_row, "Cancel",
                         self.app.show_admin_home).pack(side="left")

    def _save(self):
        try:
            t = self.entries["start_time"].get().strip()
            if t.count(":") == 1:
                t += ":00"
            data = {
                "event_name": self.entries["event_name"].get().strip(),
                "category": self.entries["category"].get().strip(),
                "description": self.desc.get("1.0", "end").strip(),
                "venue": self.entries["venue"].get().strip(),
                "city": self.entries["city"].get().strip(),
                "event_date": self.entries["event_date"].get().strip(),
                "start_time": t,
                "total_seats": int(self.entries["total_seats"].get()),
                "ticket_price": float(self.entries["ticket_price"].get()),
            }
        except ValueError:
            self.err.config(
                text="✕  Seats must be a whole number, price must be a number.")
            return

        if not all([data["event_name"], data["category"],
                    data["venue"], data["city"], data["event_date"]]):
            self.err.config(text="✕  Please fill all required fields.")
            return

        if self.mode == "add":
            ok, res = add_event(self.app.user["user_id"], data)
            if not ok:
                self.err.config(text=f"✕  {res}")
                return
            messagebox.showinfo("Success", f"Event added (ID: {res}).")
        else:
            for field in ["event_name", "category", "description", "venue",
                          "city", "event_date", "start_time",
                          "total_seats", "ticket_price"]:
                update_event(self.event["event_id"], field, data[field])
            messagebox.showinfo("Success", "Event updated.")
        self.app.show_admin_home()

    def destroy(self):
        self.frame.destroy()


# ============================================================
# ALL USERS
# ============================================================

class UsersWindow:
    def __init__(self, root, app):
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        make_navbar(self.frame, self.app.user, self.app)

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=32, pady=(28, 18))
        tk.Label(header, text="Users", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(header, text="Everyone registered on Eventra.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(4, 0))

        tf = tk.Frame(self.frame, bg=CARD_BG,
                      highlightbackground=BORDER, highlightthickness=1)
        tf.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        cols = ("id", "name", "email", "phone", "role")
        tree = ttk.Treeview(tf, columns=cols, show="headings", height=18)
        heads = {"id": "ID", "name": "Name", "email": "Email",
                 "phone": "Phone", "role": "Role"}
        widths = {"id": 60, "name": 160, "email": 240, "phone": 140, "role": 100}
        for c in cols:
            tree.heading(c, text=heads[c])
            tree.column(c, anchor="w", width=widths[c])
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("SELECT user_id, name, email, phone, role "
                    "FROM users ORDER BY user_id")
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        cur.close()
        conn.close()

    def destroy(self):
        self.frame.destroy()


# ============================================================
# ALL BOOKINGS
# ============================================================

class AllBookingsWindow:
    def __init__(self, root, app):
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        make_navbar(self.frame, self.app.user, self.app)

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=32, pady=(28, 18))
        tk.Label(header, text="Bookings", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(header, text="Every booking made on Eventra.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(4, 0))

        tf = tk.Frame(self.frame, bg=CARD_BG,
                      highlightbackground=BORDER, highlightthickness=1)
        tf.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        cols = ("id", "user", "event", "qty", "total", "status")
        tree = ttk.Treeview(tf, columns=cols, show="headings", height=18)
        heads = {"id": "Booking ID", "user": "User", "event": "Event",
                 "qty": "Qty", "total": "Total", "status": "Status"}
        widths = {"id": 100, "user": 160, "event": 220, "qty": 70,
                  "total": 120, "status": 120}
        for c in cols:
            tree.heading(c, text=heads[c])
            tree.column(c, anchor="w", width=widths[c])
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT b.booking_id, u.name, e.event_name, b.num_tickets,
                   b.total_amount, b.booking_status
            FROM bookings b
            JOIN users u  ON b.user_id = u.user_id
            JOIN events e ON b.event_id = e.event_id
            ORDER BY b.booking_date DESC
        """)
        for r in cur.fetchall():
            tree.insert("", "end", values=(
                r[0], r[1], r[2], r[3], f"₹{float(r[4]):.2f}", r[5]
            ))
        cur.close()
        conn.close()

    def destroy(self):
        self.frame.destroy()


# ============================================================
# REPORTS
# ============================================================

class ReportsWindow:
    def __init__(self, root, app):
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        make_navbar(self.frame, self.app.user, self.app)

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=32, pady=(28, 18))
        tk.Label(header, text="Reports", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(header, text="Insights on bookings, events, and revenue.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(4, 0))

        nb = ttk.Notebook(self.frame)
        nb.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        # ---- Revenue ----
        t1 = tk.Frame(nb, bg=CARD_BG)
        nb.add(t1, text="Revenue")
        rev = total_revenue()
        if rev:
            cards = tk.Frame(t1, bg=CARD_BG)
            cards.pack(fill="x", padx=28, pady=28)

            for label, value, is_accent in [
                ("Confirmed bookings", str(rev["total_bookings"]), False),
                ("Tickets sold", str(rev["total_tickets"]), False),
                ("Total revenue", f"₹{float(rev['total_revenue']):.2f}", True),
            ]:
                box = tk.Frame(cards, bg=CARD_BG,
                               highlightbackground=BORDER, highlightthickness=1)
                box.pack(side="left", padx=(0, 12), ipadx=24, ipady=16)
                tk.Label(box, text=label.upper(), font=FONT_LABEL,
                         bg=CARD_BG, fg=TEXT_TERTIARY
                         ).pack(anchor="w", padx=20, pady=(14, 4))
                color = PRIMARY if is_accent else TEXT_PRIMARY
                tk.Label(box, text=value,
                         font=(FONT_H1[0], 22, "bold"),
                         bg=CARD_BG, fg=color
                         ).pack(anchor="w", padx=20, pady=(0, 14))

        # ---- Event-wise ----
        t2 = tk.Frame(nb, bg=CARD_BG)
        nb.add(t2, text="By event")
        self._table(t2,
            ["Event ID", "Event name", "Bookings", "Tickets", "Revenue"],
            [(r["event_id"], r["event_name"], r["bookings"],
              r["tickets"], f"₹{float(r['revenue']):.2f}")
             for r in event_wise_bookings()],
            widths=[90, 260, 110, 100, 140])

        # ---- Popular ----
        t3 = tk.Frame(nb, bg=CARD_BG)
        nb.add(t3, text="Popular")
        self._table(t3,
            ["Rank", "Event name", "Tickets sold"],
            [(i + 1, r["event_name"], r["tickets_sold"])
             for i, r in enumerate(most_popular_events())],
            widths=[80, 320, 140])

        # ---- User history ----
        t4 = tk.Frame(nb, bg=CARD_BG)
        nb.add(t4, text="User history")

        top = tk.Frame(t4, bg=CARD_BG)
        top.pack(fill="x", padx=24, pady=(20, 12))
        tk.Label(top, text="USER ID", font=FONT_LABEL,
                 bg=CARD_BG, fg=TEXT_SECONDARY
                 ).pack(side="left", padx=(0, 8))
        self.uid_wrap, self.uid = modern_entry(top, width=10)
        self.uid_wrap.pack(side="left", ipady=0)
        primary_button(top, "Load",
                       lambda: self._history(t4)).pack(side="left", padx=8)

        self.hist = tk.Frame(t4, bg=CARD_BG)
        self.hist.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    def _table(self, parent, headers, rows, widths=None):
        tf = tk.Frame(parent, bg=CARD_BG,
                      highlightbackground=BORDER, highlightthickness=1)
        tf.pack(fill="both", expand=True, padx=24, pady=24)

        tree = ttk.Treeview(tf, columns=list(range(len(headers))),
                            show="headings", height=15)
        for i, h in enumerate(headers):
            tree.heading(i, text=h)
            w = widths[i] if widths else 180
            tree.column(i, anchor="w", width=w)
        for r in rows:
            tree.insert("", "end", values=r)
        tree.pack(fill="both", expand=True, padx=8, pady=8)

    def _history(self, parent):
        try:
            uid = int(self.uid.get())
        except ValueError:
            return
        for w in self.hist.winfo_children():
            w.destroy()
        user, history = user_booking_history(uid)
        if not user:
            tk.Label(self.hist, text="User not found.",
                     font=FONT_BODY, bg=CARD_BG, fg=ACCENT).pack(pady=20)
            return

        # User header card
        head = tk.Frame(self.hist, bg=CARD_BG,
                        highlightbackground=BORDER, highlightthickness=1)
        head.pack(fill="x", pady=(0, 12))

        left = tk.Frame(head, bg=CARD_BG)
        left.pack(side="left", padx=20, pady=14)
        tk.Label(left, text=user["name"], font=FONT_H2,
                 bg=CARD_BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(left, text=user["email"], font=FONT_SMALL,
                 bg=CARD_BG, fg=TEXT_SECONDARY).pack(anchor="w")

        right = tk.Frame(head, bg=CARD_BG)
        right.pack(side="right", padx=20, pady=14)
        tk.Label(right,
                 text=f"{user['total_bookings']} bookings  ·  "
                      f"₹{user['total_spent']:.2f} spent",
                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_PRIMARY
                 ).pack(anchor="e")

        # History table
        tf = tk.Frame(self.hist, bg=CARD_BG,
                      highlightbackground=BORDER, highlightthickness=1)
        tf.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            tf, columns=("id", "event", "qty", "total", "date", "status"),
            show="headings", height=10)
        heads = {"id": "Booking ID", "event": "Event", "qty": "Qty",
                 "total": "Total", "date": "Date", "status": "Status"}
        widths = {"id": 100, "event": 220, "qty": 70,
                  "total": 120, "date": 130, "status": 120}
        for c in ("id", "event", "qty", "total", "date", "status"):
            tree.heading(c, text=heads[c])
            tree.column(c, anchor="w", width=widths[c])
        for h in history:
            tree.insert("", "end", values=(
                h["booking_id"], h["event_name"], h["num_tickets"],
                f"₹{float(h['total_amount']):.2f}",
                str(h["booking_date"])[:10], h["booking_status"]
            ))
        tree.pack(fill="both", expand=True, padx=8, pady=8)

    def destroy(self):
        self.frame.destroy()