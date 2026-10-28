"""
gui_user.py
------------
Sidebar shell + all pre-auth (Login/Register) and user-facing screens.
Admin screens live in gui_admin.py; they call build_shell() from here.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from auth import login_user, register_user
from events import list_events, search_events
from bookings import book_ticket, my_bookings, cancel_booking
from theme import (
    FONT_FAMILY, BG, BG_SIDEBAR, BG_ELEVATED, BG_HOVER, BG_ACTIVE,
    BORDER, BORDER_STRONG, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_TERTIARY,
    ACCENT, ACCENT_DARK, ACCENT_LIGHT, SUCCESS, DANGER,
    FONT_DISPLAY, FONT_H1, FONT_H2, FONT_H3, FONT_BODY, FONT_SMALL,
    FONT_TINY, FONT_LABEL, FONT_BUTTON, FONT_NAV, FONT_PRICE,
    primary_button, secondary_button, danger_button, ghost_button,
    modern_entry, category_color, category_emoji,
)


# ============================================================
# SHELL — sidebar + content
# ============================================================

def _nav_item(parent, emoji, label, command, active=False):
    bg = BG_ACTIVE if active else BG_SIDEBAR
    row = tk.Frame(parent, bg=bg, height=58)
    row.pack(fill="x", pady=1)
    row.pack_propagate(False)

    if active:
        tk.Frame(row, bg=ACCENT, width=3).pack(side="left", fill="y")

    inner = tk.Frame(row, bg=bg)
    inner.pack(fill="both", expand=True, padx=(36 if active else 39, 24))

    icon = tk.Label(inner, text=emoji, font=(FONT_FAMILY, 16), bg=bg,
                    fg=TEXT_PRIMARY if active else TEXT_SECONDARY)
    icon.pack(side="left", padx=(0, 16))

    lbl = tk.Label(inner, text=label, font=FONT_NAV, bg=bg,
                   fg=TEXT_PRIMARY if active else TEXT_SECONDARY)
    lbl.pack(side="left")

    def enter(_):
        if active:
            return
        for w in (row, inner, icon, lbl):
            w.config(bg=BG_HOVER)
        icon.config(fg=TEXT_PRIMARY)
        lbl.config(fg=TEXT_PRIMARY)

    def leave(_):
        if active:
            return
        for w in (row, inner, icon, lbl):
            w.config(bg=BG_SIDEBAR)
        icon.config(fg=TEXT_SECONDARY)
        lbl.config(fg=TEXT_SECONDARY)

    for w in (row, inner, icon, lbl):
        w.bind("<Enter>", enter)
        w.bind("<Leave>", leave)
        w.bind("<Button-1>", lambda e: command())
        w.config(cursor="hand2")


def build_shell(parent, user, app, active_nav):
    """Two-column layout: sidebar + content. Returns content frame."""
    parent.configure(bg=BG)

    sidebar = tk.Frame(parent, bg=BG_SIDEBAR, width=370)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Brand
    brand = tk.Frame(sidebar, bg=BG_SIDEBAR)
    brand.pack(fill="x", padx=39, pady=(36, 0))
    tk.Label(brand, text="🎟", font=(FONT_FAMILY, 22), bg=BG_SIDEBAR,
             fg=ACCENT).pack(side="left", padx=(0, 14))
    tk.Label(brand, text="Eventra", font=(FONT_FAMILY, 21, "bold"),
             bg=BG_SIDEBAR, fg=TEXT_PRIMARY).pack(side="left")

    tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=32, pady=28)

    # Nav items
    if user["role"] == "admin":
        items = [
            ("Events",     "📅", app.show_admin_home),
            ("Users",      "👥", app.show_admin_users),
            ("Bookings",   "🎫", app.show_admin_bookings),
            ("Reports",    "📊", app.show_reports),
        ]
    else:
        items = [
            ("Events",      "📅", app.show_user_home),
            ("My Bookings", "🎫", app.show_my_bookings),
        ]

    for label, emoji, cmd in items:
        _nav_item(sidebar, emoji, label, cmd, active=(label == active_nav))

    # Bottom: user info + sign out
    bottom = tk.Frame(sidebar, bg=BG_SIDEBAR)
    bottom.pack(side="bottom", fill="x", padx=26, pady=26)

    tk.Frame(bottom, bg=BORDER, height=1).pack(fill="x", pady=(0, 20))

    ucard = tk.Frame(bottom, bg=BG_SIDEBAR)
    ucard.pack(fill="x", padx=8, pady=(0, 6))

    icon = "🛡" if user["role"] == "admin" else "👤"
    tk.Label(ucard, text=icon, font=(FONT_FAMILY, 17), bg=BG_SIDEBAR,
             fg=TEXT_SECONDARY).pack(side="left", padx=(0, 14))

    uinfo = tk.Frame(ucard, bg=BG_SIDEBAR)
    uinfo.pack(side="left", fill="x", expand=True)
    tk.Label(uinfo, text=user["name"], font=(FONT_FAMILY, 14, "bold"),
             bg=BG_SIDEBAR, fg=TEXT_PRIMARY, anchor="w").pack(fill="x")
    tk.Label(uinfo, text="Administrator" if user["role"] == "admin" else "Member",
             font=(FONT_FAMILY, 10), bg=BG_SIDEBAR, fg=TEXT_TERTIARY,
             anchor="w").pack(fill="x", pady=(2, 0))

    signout = tk.Button(bottom, text="Sign out", font=FONT_SMALL,
                        bg=BG_SIDEBAR, fg=TEXT_SECONDARY,
                        activebackground=BG_HOVER, activeforeground=TEXT_PRIMARY,
                        relief="flat", cursor="hand2", anchor="w",
                        padx=18, pady=13, borderwidth=0, command=app.logout)
    signout.pack(fill="x", pady=(14, 0))
    signout.bind("<Enter>", lambda e: signout.config(bg=BG_HOVER,
                                                       fg=TEXT_PRIMARY))
    signout.bind("<Leave>", lambda e: signout.config(bg=BG_SIDEBAR,
                                                       fg=TEXT_SECONDARY))

    content = tk.Frame(parent, bg=BG)
    content.pack(side="right", fill="both", expand=True)
    return content


def content_header(content, title, subtitle=None):
    """Add a page header. Returns the frame so callers can add action buttons."""
    header = tk.Frame(content, bg=BG)
    header.pack(fill="x", padx=40, pady=(32, 0))
    left = tk.Frame(header, bg=BG)
    left.pack(side="left", fill="x", expand=True)
    tk.Label(left, text=title, font=FONT_H1, bg=BG,
             fg=TEXT_PRIMARY, anchor="w").pack(fill="x")
    if subtitle:
        tk.Label(left, text=subtitle, font=FONT_SMALL, bg=BG,
                 fg=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(6, 0))
    return header


# ============================================================
# EVENT CARD
# ============================================================

class EventCard(tk.Frame):
    def __init__(self, parent, event, on_book=None, on_edit=None, on_delete=None):
        super().__init__(parent, bg=BG_ELEVATED,
                         highlightbackground=BORDER, highlightthickness=1)
        color = category_color(event["category"])
        tk.Frame(self, bg=color, height=4).pack(fill="x")

        inner = tk.Frame(self, bg=BG_ELEVATED, padx=22, pady=20)
        inner.pack(fill="both", expand=True)

        # Category badge
        badge = tk.Frame(inner, bg=BG_ELEVATED)
        badge.pack(fill="x", pady=(0, 12))
        emoji_lbl = tk.Label(badge, text=category_emoji(event["category"]),
                             font=(FONT_FAMILY, 20), bg=BG_ELEVATED, fg=color)
        emoji_lbl.pack(side="left")
        tk.Label(badge, text=event["category"].upper(), font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=color).pack(side="left", padx=(10, 0),
                                                pady=6)

        tk.Label(inner, text=event["event_name"], font=FONT_H3,
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY, anchor="w",
                 wraplength=280, justify="left").pack(fill="x")

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=14)

        for icon_char, text in [
            ("📍", event["city"]),
            ("📅", f"{event['event_date']} · {event['start_time']}"),
            ("💺", f"{event['available_seats']} of {event['total_seats']} seats"),
        ]:
            r = tk.Frame(inner, bg=BG_ELEVATED)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=icon_char, font=FONT_TINY, bg=BG_ELEVATED,
                     fg=TEXT_TERTIARY, width=2, anchor="w").pack(side="left")
            tk.Label(r, text=text, font=FONT_SMALL, bg=BG_ELEVATED,
                     fg=TEXT_SECONDARY, anchor="w").pack(side="left")

        tk.Label(inner, text=f"₹{float(event['ticket_price']):.0f}",
                 font=FONT_PRICE, bg=BG_ELEVATED, fg=color, anchor="w"
                 ).pack(fill="x", pady=(16, 12))

        btn_row = tk.Frame(inner, bg=BG_ELEVATED)
        btn_row.pack(fill="x")
        if on_book:
            primary_button(btn_row, "Book now",
                           lambda: on_book(event)).pack(fill="x")
        elif on_edit and on_delete:
            secondary_button(btn_row, "Edit",
                             lambda: on_edit(event)).pack(
                                 side="left", expand=True, fill="x", padx=(0, 4))
            danger_button(btn_row, "Delete",
                          lambda: on_delete(event)).pack(
                              side="left", expand=True, fill="x", padx=(4, 0))


# ============================================================
# LOGIN / REGISTER — centered form, no card
# ============================================================

class LoginWindow:
    def __init__(self, root, app):
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        outer = tk.Frame(self.frame, bg=BG)
        outer.pack(fill="both", expand=True)
        wrap = tk.Frame(outer, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        # Brand
        tk.Label(wrap, text="🎟", font=(FONT_FAMILY, 44),
                 bg=BG, fg=ACCENT).pack()
        tk.Label(wrap, text="Eventra", font=(FONT_FAMILY, 32, "bold"),
                 bg=BG, fg=TEXT_PRIMARY).pack(pady=(8, 0))
        tk.Label(wrap, text="Event Management & Ticketing",
                 font=FONT_BODY, bg=BG, fg=TEXT_SECONDARY
                 ).pack(pady=(6, 40))

        # Heading
        tk.Label(wrap, text="Sign in", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY, anchor="w").pack(fill="x")
        tk.Label(wrap, text="Welcome back. Continue where you left off.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(6, 26))

        # Email
        tk.Label(wrap, text="EMAIL", font=FONT_LABEL,
                 bg=BG, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 6))
        self.email_wrapper, self.email_entry = modern_entry(wrap, width=36)
        self.email_wrapper.pack(fill="x", pady=(0, 18))

        # Password
        tk.Label(wrap, text="PASSWORD", font=FONT_LABEL,
                 bg=BG, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 6))
        self.pw_wrapper, self.pw_entry = modern_entry(wrap, show="•", width=36)
        self.pw_wrapper.pack(fill="x", pady=(0, 10))

        self.err = tk.Label(wrap, text="", font=FONT_SMALL,
                             bg=BG, fg=DANGER, anchor="w")
        self.err.pack(fill="x", pady=(0, 14))

        primary_button(wrap, "Sign in", self._do).pack(fill="x", pady=(0, 22))

        footer = tk.Frame(wrap, bg=BG)
        footer.pack()
        tk.Label(footer, text="Don't have an account?",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY).pack(side="left")
        link = tk.Label(footer, text="Sign up",
                        font=(FONT_FAMILY, 11, "bold"),
                        bg=BG, fg=ACCENT, cursor="hand2")
        link.pack(side="left", padx=(6, 0))
        link.bind("<Button-1>", lambda e: self.app.show_register())

        self.pw_entry.bind("<Return>", lambda e: self._do())
        self.email_entry.bind("<Return>", lambda e: self.pw_entry.focus_set())
        self.email_entry.focus_set()

    def _do(self):
        ok, res = login_user(self.email_entry.get(), self.pw_entry.get())
        if ok:
            self.app.on_login_success(res)
        else:
            self.err.config(text=f"✕  {res}")

    def destroy(self):
        self.frame.destroy()


class RegisterWindow:
    def __init__(self, root, app):
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        outer = tk.Frame(self.frame, bg=BG)
        outer.pack(fill="both", expand=True)
        wrap = tk.Frame(outer, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(wrap, text="🎟", font=(FONT_FAMILY, 36),
                 bg=BG, fg=ACCENT).pack()
        tk.Label(wrap, text="Eventra", font=(FONT_FAMILY, 26, "bold"),
                 bg=BG, fg=TEXT_PRIMARY).pack(pady=(6, 0))

        tk.Label(wrap, text="Create your account", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY, anchor="w"
                 ).pack(fill="x", pady=(24, 6))
        tk.Label(wrap, text="It only takes a minute.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 22))

        self.e = {}
        for label, key, is_pw in [
            ("FULL NAME", "name", False),
            ("EMAIL", "email", False),
            ("PHONE (10 DIGITS)", "phone", False),
            ("PASSWORD", "password", True),
            ("CONFIRM PASSWORD", "confirm", True),
        ]:
            tk.Label(wrap, text=label, font=FONT_LABEL,
                     bg=BG, fg=TEXT_SECONDARY, anchor="w"
                     ).pack(fill="x", pady=(0, 5))
            w, ent = modern_entry(wrap, show="•" if is_pw else None, width=36)
            w.pack(fill="x", pady=(0, 12))
            self.e[key] = ent

        self.err = tk.Label(wrap, text="", font=FONT_SMALL,
                             bg=BG, fg=DANGER, anchor="w")
        self.err.pack(fill="x", pady=(0, 10))

        primary_button(wrap, "Create account", self._do
                       ).pack(fill="x", pady=(0, 18))

        footer = tk.Frame(wrap, bg=BG)
        footer.pack()
        tk.Label(footer, text="Already have an account?",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY).pack(side="left")
        link = tk.Label(footer, text="Sign in",
                        font=(FONT_FAMILY, 11, "bold"),
                        bg=BG, fg=ACCENT, cursor="hand2")
        link.pack(side="left", padx=(6, 0))
        link.bind("<Button-1>", lambda e: self.app.show_login())

        self.e["name"].focus_set()

    def _do(self):
        pw = self.e["password"].get()
        if pw != self.e["confirm"].get():
            self.err.config(text="✕  Passwords do not match.", fg=DANGER)
            return
        ok, res = register_user(self.e["name"].get(), self.e["email"].get(),
                                self.e["phone"].get(), pw)
        if ok:
            self.err.config(text="✓  Account created. Redirecting...",
                             fg=SUCCESS)
            self.frame.after(1200, self.app.show_login)
        else:
            self.err.config(text=f"✕  {res}", fg=DANGER)

    def destroy(self):
        self.frame.destroy()


# ============================================================
# USER — Events dashboard
# ============================================================

class UserEventsWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        content = build_shell(self.frame, self.app.user, self.app, "Events")

        header = content_header(
            content,
            f"Welcome back, {self.app.user['name']}",
            "Browse and book events in seconds."
        )

        search_row = tk.Frame(content, bg=BG)
        search_row.pack(fill="x", padx=40, pady=(24, 18))
        self.search_var = tk.StringVar()
        sw, ent = modern_entry(search_row, width=42)
        ent.config(textvariable=self.search_var)
        sw.pack(side="left", ipady=0)
        ent.bind("<Return>", lambda e: self._search())
        ghost_button(search_row, "Search", self._search
                     ).pack(side="left", padx=(10, 4))
        ghost_button(search_row, "Reset", self._load_all).pack(side="left")

        cf = tk.Frame(content, bg=BG)
        cf.pack(fill="both", expand=True, padx=40, pady=(0, 24))

        self.canvas = tk.Canvas(cf, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.inner = tk.Frame(self.canvas, bg=BG)
        self._win = self.canvas.create_window((0, 0), window=self.inner,
                                                anchor="nw")
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
        self._render(list_events())

    def _search(self):
        kw = self.search_var.get().strip()
        self._render(search_events(kw) if kw else list_events())

    def _render(self, events):
        for w in self.inner.winfo_children():
            w.destroy()
        if not events:
            empty = tk.Frame(self.inner, bg=BG)
            empty.grid(row=0, column=0, columnspan=3, pady=100)
            tk.Label(empty, text="🎫", font=(FONT_FAMILY, 44),
                     bg=BG, fg=TEXT_TERTIARY).pack()
            tk.Label(empty, text="No events available",
                     font=FONT_H2, bg=BG, fg=TEXT_PRIMARY
                     ).pack(pady=(16, 4))
            tk.Label(empty, text="Check back later or contact admin.",
                     font=FONT_SMALL, bg=BG, fg=TEXT_TERTIARY).pack()
            return
        for i, ev in enumerate(events):
            r, c = divmod(i, 3)
            EventCard(self.inner, ev, on_book=self._book).grid(
                row=r, column=c, padx=10, pady=10, sticky="nsew")
        for c in range(3):
            self.inner.grid_columnconfigure(c, weight=1, minsize=300)

    def _book(self, event):
        BookingModal(self.root, self.app, event)

    def destroy(self):
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.frame.unbind_all(seq)
        self.frame.destroy()


# ============================================================
# BOOKING MODAL
# ============================================================

class BookingModal(tk.Toplevel):
    def __init__(self, parent, app, event):
        super().__init__(parent)
        self.app = app
        self.event = event
        self.title("Book tickets")
        self.geometry("560x720")
        self.configure(bg=BG_ELEVATED)
        self.grab_set()

        color = category_color(event["category"])
        tk.Frame(self, bg=color, height=5).pack(fill="x")

        pad = 34
        head = tk.Frame(self, bg=BG_ELEVATED)
        head.pack(fill="x", padx=pad, pady=(pad, 0))
        tk.Label(head, text=category_emoji(event["category"]),
                 font=(FONT_FAMILY, 22), bg=BG_ELEVATED, fg=color
                 ).pack(side="left", padx=(0, 12))
        col = tk.Frame(head, bg=BG_ELEVATED)
        col.pack(side="left", fill="x", expand=True)
        tk.Label(col, text=event["event_name"], font=FONT_H2,
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY, anchor="w"
                 ).pack(fill="x")
        tk.Label(col, text=event["category"].upper(), font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=color, anchor="w").pack(fill="x")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=pad, pady=20)

        info = tk.Frame(self, bg=BG_ELEVATED)
        info.pack(fill="x", padx=pad)
        for label, value in [
            ("Venue", event["venue"]),
            ("City",  event["city"]),
            ("Date",  f"{event['event_date']} at {event['start_time']}"),
            ("Price", f"₹{float(event['ticket_price']):.2f} per ticket"),
            ("Seats", f"{event['available_seats']} available"),
        ]:
            r = tk.Frame(info, bg=BG_ELEVATED)
            r.pack(fill="x", pady=5)
            tk.Label(r, text=label.upper(), font=FONT_LABEL, bg=BG_ELEVATED,
                     fg=TEXT_TERTIARY, width=8, anchor="w").pack(side="left")
            tk.Label(r, text=value, font=FONT_SMALL, bg=BG_ELEVATED,
                     fg=TEXT_PRIMARY, anchor="w").pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=pad, pady=20)

        tk.Label(self, text="NUMBER OF TICKETS", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY
                 ).pack(padx=pad, anchor="w")
        ctr = tk.Frame(self, bg=BG_ELEVATED)
        ctr.pack(padx=pad, pady=10, anchor="w")

        self.qty = tk.IntVar(value=1)
        dec = tk.Button(ctr, text="−", font=(FONT_FAMILY, 18),
                        bg=BG_HOVER, fg=TEXT_PRIMARY, relief="flat",
                        cursor="hand2", width=3, command=self._dec, bd=0)
        dec.pack(side="left")
        tk.Label(ctr, textvariable=self.qty, font=(FONT_FAMILY, 20, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY, width=4).pack(side="left")
        inc = tk.Button(ctr, text="+", font=(FONT_FAMILY, 18),
                        bg=BG_HOVER, fg=TEXT_PRIMARY, relief="flat",
                        cursor="hand2", width=3, command=self._inc, bd=0)
        inc.pack(side="left")

        self.total_lbl = tk.Label(
            self, text=f"Total: ₹{float(event['ticket_price']):.2f}",
            font=(FONT_FAMILY, 18, "bold"), bg=BG_ELEVATED, fg=color)
        self.total_lbl.pack(padx=pad, pady=(10, 20), anchor="w")

        tk.Label(self, text="PAYMENT METHOD", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY).pack(padx=pad, anchor="w")
        self.pay = tk.StringVar(value="UPI")
        pr = tk.Frame(self, bg=BG_ELEVATED)
        pr.pack(padx=pad, pady=10, anchor="w")
        for m in ["UPI", "Card", "Cash"]:
            tk.Radiobutton(pr, text=m, variable=self.pay, value=m,
                          font=FONT_SMALL, bg=BG_ELEVATED, fg=TEXT_PRIMARY,
                          activebackground=BG_ELEVATED,
                          activeforeground=TEXT_PRIMARY,
                          selectcolor=BG_ELEVATED,
                          cursor="hand2").pack(side="left", padx=(0, 22))

        self.err = tk.Label(self, text="", font=FONT_SMALL,
                             bg=BG_ELEVATED, fg=DANGER)
        self.err.pack(pady=8)

        row = tk.Frame(self, bg=BG_ELEVATED)
        row.pack(pady=14)
        primary_button(row, "Confirm booking",
                       self._confirm).pack(side="left", padx=(0, 10))
        secondary_button(row, "Cancel", self.destroy).pack(side="left")

    def _inc(self):
        if self.qty.get() < self.event["available_seats"]:
            self.qty.set(self.qty.get() + 1)
            self._update()

    def _dec(self):
        if self.qty.get() > 1:
            self.qty.set(self.qty.get() - 1)
            self._update()

    def _update(self):
        self.total_lbl.config(
            text=f"Total: ₹{float(self.event['ticket_price']) * self.qty.get():.2f}")

    def _confirm(self):
        ok, res = book_ticket(self.app.user["user_id"], self.event["event_id"],
                              self.qty.get(), self.pay.get())
        if not ok:
            self.err.config(text=f"✕  {res}")
            return
        self.destroy()
        self._show_success(res)
        self.app.show_user_home()

    def _show_success(self, info):
        win = tk.Toplevel(self.app.root)
        win.title("Booking confirmed")
        win.geometry("500x420")
        win.configure(bg=BG_ELEVATED)
        win.grab_set()

        tk.Frame(win, bg=SUCCESS, height=5).pack(fill="x")
        tk.Label(win, text="✓", font=(FONT_FAMILY, 48),
                 bg=BG_ELEVATED, fg=SUCCESS).pack(pady=(32, 8))
        tk.Label(win, text="Booking confirmed",
                 font=(FONT_FAMILY, 22, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack()

        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=44, pady=24)

        body = tk.Frame(win, bg=BG_ELEVATED)
        body.pack(padx=44)
        for label, value in [("Booking ID", f"#{info['booking_id']}"),
                              ("Transaction", info["txn_id"]),
                              ("Total paid", f"₹{info['total']:.2f}")]:
            r = tk.Frame(body, bg=BG_ELEVATED)
            r.pack(fill="x", pady=6)
            tk.Label(r, text=label, font=FONT_SMALL, bg=BG_ELEVATED,
                     fg=TEXT_TERTIARY, width=13, anchor="w").pack(side="left")
            tk.Label(r, text=value, font=(FONT_FAMILY, 12, "bold"),
                     bg=BG_ELEVATED, fg=TEXT_PRIMARY, anchor="w"
                     ).pack(side="left")

        primary_button(win, "Done", win.destroy).pack(pady=28)


# ============================================================
# USER — My Bookings
# ============================================================

class MyBookingsWindow:
    def __init__(self, root, app):
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        content = build_shell(self.frame, self.app.user, self.app, "My Bookings")
        content_header(content, "My bookings",
                        "Every booking you've made on Eventra.")

        tf = tk.Frame(content, bg=BG_ELEVATED,
                      highlightbackground=BORDER, highlightthickness=1)
        tf.pack(fill="both", expand=True, padx=40, pady=(24, 14))

        cols = ("id", "event", "qty", "total", "date", "status")
        self.tree = ttk.Treeview(tf, columns=cols, show="headings", height=15)
        heads = {"id": "Booking ID", "event": "Event", "qty": "Qty",
                 "total": "Total", "date": "Date", "status": "Status"}
        widths = {"id": 120, "event": 300, "qty": 80,
                  "total": 140, "date": 150, "status": 140}
        for c in cols:
            self.tree.heading(c, text=heads[c])
            self.tree.column(c, anchor="w", width=widths[c])
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        row = tk.Frame(content, bg=BG)
        row.pack(fill="x", padx=40, pady=(0, 32))
        danger_button(row, "Cancel selected booking",
                      self._cancel).pack(side="left")

        self._load()

    def _load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in my_bookings(self.app.user["user_id"]):
            self.tree.insert("", "end", values=(
                r["booking_id"], r["event_name"], r["num_tickets"],
                f"₹{float(r['total_amount']):.2f}",
                str(r["booking_date"])[:10], r["booking_status"]
            ))

    def _cancel(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a booking first.")
            return
        bid = self.tree.item(sel[0])["values"][0]
        if not messagebox.askyesno("Confirm", f"Cancel booking #{bid}?"):
            return
        ok, msg = cancel_booking(self.app.user["user_id"], bid)
        if ok:
            messagebox.showinfo("Cancelled", msg)
            self._load()
        else:
            messagebox.showerror("Error", msg)

    def destroy(self):
        self.frame.destroy()