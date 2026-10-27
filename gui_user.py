"""
gui_user.py
------------
Notion/Obsidian-inspired minimal UI.
Theme + Login + Register + User event grid + Booking modal + My Bookings.
Admin screens live in gui_admin.py and inherit the theme from here.
"""

import platform
import tkinter as tk
from tkinter import ttk, messagebox

from auth import login_user, register_user
from events import list_events, search_events
from bookings import book_ticket, my_bookings, cancel_booking


# ============================================================
# THEME — warm neutrals, restrained type, one accent
# ============================================================

_OS = platform.system()
if _OS == "Windows":
    FONT_FAMILY = "Segoe UI"
elif _OS == "Darwin":
    FONT_FAMILY = "SF Pro Text"
else:
    FONT_FAMILY = "Ubuntu"

# Notion-style warm neutrals
BG            = "#FBFBFA"   # page background (warm off-white)
CARD_BG       = "#FFFFFF"   # cards, panels
BG_SUBTLE     = "#F7F7F5"   # sidebar / muted areas
BG_HOVER      = "#F1F1EF"
BORDER        = "#E9E9E7"   # subtle divider
BORDER_STRONG = "#D3D1CB"   # inputs, visible divider

TEXT_PRIMARY   = "#37352F"  # near-black, Notion's signature
TEXT_SECONDARY = "#6B6B6B"
TEXT_TERTIARY  = "#9B9A97"

# One accent, used sparingly
PRIMARY      = "#5B4BDB"
PRIMARY_DARK = "#4A3DB8"
PRIMARY_TINT = "#F0EDFE"

ACCENT        = "#D94A4A"
ACCENT_DARK   = "#B83A3A"
ACCENT_LIGHT  = "#FEE2E2"

SUCCESS       = "#0F7B6C"

# Backwards-compat aliases used by gui_admin.py
TEXT_DARK  = TEXT_PRIMARY
TEXT_LIGHT = TEXT_SECONDARY

# Restrained type scale
FONT_LOGO      = (FONT_FAMILY, 13, "bold")
FONT_H1        = (FONT_FAMILY, 20, "bold")
FONT_H2        = (FONT_FAMILY, 13, "bold")
FONT_BODY      = (FONT_FAMILY, 10)
FONT_SMALL     = (FONT_FAMILY, 9)
FONT_TINY      = (FONT_FAMILY, 8)
FONT_LABEL     = (FONT_FAMILY, 8, "bold")
FONT_BUTTON    = (FONT_FAMILY, 10, "bold")
FONT_BUTTON_SM = (FONT_FAMILY, 9, "bold")
FONT_PRICE     = (FONT_FAMILY, 15, "bold")

# Aliases used by gui_admin.py
FONT_TITLE   = FONT_H1
FONT_SECTION = FONT_H2

WINDOW_W = 1100
WINDOW_H = 720


def setup_styles(root):
    s = ttk.Style(root)
    s.theme_use("clam")

    s.configure("Treeview", background=CARD_BG, fieldbackground=CARD_BG,
                foreground=TEXT_PRIMARY, rowheight=34, font=FONT_BODY,
                borderwidth=0)
    s.configure("Treeview.Heading", background=BG_SUBTLE,
                foreground=TEXT_SECONDARY, font=FONT_LABEL,
                relief="flat", padding=(12, 10))
    s.map("Treeview.Heading", background=[("active", BG_HOVER)])
    s.map("Treeview",
          background=[("selected", PRIMARY_TINT)],
          foreground=[("selected", TEXT_PRIMARY)])

    s.configure("TNotebook", background=BG, borderwidth=0)
    s.configure("TNotebook.Tab", font=FONT_SMALL, padding=(16, 10),
                background=BG, foreground=TEXT_SECONDARY)
    s.map("TNotebook.Tab",
          background=[("selected", CARD_BG)],
          foreground=[("selected", TEXT_PRIMARY)])


# ============================================================
# BUTTONS
# ============================================================

def primary_button(parent, text, command, width=None):
    b = tk.Button(parent, text=text, command=command,
                  bg=PRIMARY, fg="white", font=FONT_BUTTON,
                  activebackground=PRIMARY_DARK, activeforeground="white",
                  relief="flat", cursor="hand2", pady=8, padx=16, borderwidth=0)
    b.bind("<Enter>", lambda e: b.config(bg=PRIMARY_DARK))
    b.bind("<Leave>", lambda e: b.config(bg=PRIMARY))
    if width:
        b.config(width=width)
    return b


def secondary_button(parent, text, command, width=None):
    b = tk.Button(parent, text=text, command=command,
                  bg=BG_SUBTLE, fg=TEXT_PRIMARY, font=FONT_BUTTON,
                  activebackground=BG_HOVER, activeforeground=TEXT_PRIMARY,
                  relief="flat", cursor="hand2", pady=8, padx=16, borderwidth=0)
    b.bind("<Enter>", lambda e: b.config(bg=BG_HOVER))
    b.bind("<Leave>", lambda e: b.config(bg=BG_SUBTLE))
    if width:
        b.config(width=width)
    return b


def accent_button(parent, text, command, width=None):
    """Outlined red — for destructive actions (Delete, Cancel)."""
    b = tk.Button(parent, text=text, command=command,
                  bg=CARD_BG, fg=ACCENT, font=FONT_BUTTON,
                  activebackground=ACCENT_LIGHT, activeforeground=ACCENT_DARK,
                  relief="solid", cursor="hand2", pady=8, padx=16,
                  borderwidth=1, highlightbackground=BORDER_STRONG)
    b.bind("<Enter>", lambda e: b.config(bg=ACCENT_LIGHT))
    b.bind("<Leave>", lambda e: b.config(bg=CARD_BG))
    if width:
        b.config(width=width)
    return b


def ghost_button(parent, text, command):
    b = tk.Button(parent, text=text, command=command,
                  bg=BG, fg=TEXT_SECONDARY, font=FONT_BODY,
                  activebackground=BG_HOVER, activeforeground=TEXT_PRIMARY,
                  relief="flat", cursor="hand2", padx=10, pady=6, borderwidth=0)
    b.bind("<Enter>", lambda e: b.config(bg=BG_HOVER, fg=TEXT_PRIMARY))
    b.bind("<Leave>", lambda e: b.config(bg=BG, fg=TEXT_SECONDARY))
    return b


# ============================================================
# INPUT — white with thin border, focus ring in accent color
# ============================================================

def modern_entry(parent, show=None, width=36):
    wrapper = tk.Frame(parent, bg=BORDER_STRONG, padx=1, pady=1)
    entry = tk.Entry(wrapper, font=FONT_BODY, width=width, bd=0, relief="flat",
                     bg=CARD_BG, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
                     highlightthickness=0)
    if show:
        entry.config(show=show)
    entry.pack(fill="x", ipady=7, padx=11)
    entry.bind("<FocusIn>",  lambda e: wrapper.config(bg=PRIMARY))
    entry.bind("<FocusOut>", lambda e: wrapper.config(bg=BORDER_STRONG))
    return wrapper, entry


# ============================================================
# NAVBAR — white bar, bottom border, small brand, plain links
# ============================================================

def make_navbar(parent, user, app):
    nav = tk.Frame(parent, bg=CARD_BG, height=52)
    nav.pack(fill="x")
    nav.pack_propagate(False)
    tk.Frame(nav, bg=BORDER, height=1).place(x=0, y=51, relwidth=1)

    # Left: small logo + wordmark
    brand = tk.Frame(nav, bg=CARD_BG)
    brand.pack(side="left", padx=20)
    tk.Label(brand, text="🎟", font=(FONT_FAMILY, 14), bg=CARD_BG,
             fg=PRIMARY).pack(side="left", padx=(0, 7))
    tk.Label(brand, text="Eventra", font=FONT_LOGO, bg=CARD_BG,
             fg=TEXT_PRIMARY).pack(side="left")

    # Right: links + username + sign out
    right = tk.Frame(nav, bg=CARD_BG)
    right.pack(side="right", padx=16)

    if user["role"] == "admin":
        links = [("Events",    app.show_admin_home),
                 ("Users",     app.show_admin_users),
                 ("Bookings",  app.show_admin_bookings),
                 ("Reports",   app.show_reports)]
    else:
        links = [("Events",       app.show_user_home),
                 ("My bookings",  app.show_my_bookings)]

    for label, cmd in links:
        b = tk.Button(right, text=label, font=FONT_BODY,
                      bg=CARD_BG, fg=TEXT_SECONDARY,
                      activebackground=BG_HOVER, activeforeground=TEXT_PRIMARY,
                      relief="flat", cursor="hand2", padx=10, pady=6,
                      borderwidth=0, command=cmd)
        b.bind("<Enter>", lambda e, btn=b: btn.config(bg=BG_HOVER, fg=TEXT_PRIMARY))
        b.bind("<Leave>", lambda e, btn=b: btn.config(bg=CARD_BG, fg=TEXT_SECONDARY))
        b.pack(side="left", padx=1, pady=8)

    tk.Label(right, text=user["name"], font=FONT_SMALL,
             bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(16, 10))
    tk.Frame(right, bg=BORDER, width=1, height=18).pack(side="left", pady=12)

    out = tk.Button(right, text="Sign out", font=FONT_SMALL,
                    bg=CARD_BG, fg=TEXT_TERTIARY,
                    activebackground=BG_HOVER, activeforeground=TEXT_PRIMARY,
                    relief="flat", cursor="hand2", padx=10, pady=6,
                    borderwidth=0, command=app.logout)
    out.bind("<Enter>", lambda e: out.config(bg=BG_HOVER, fg=TEXT_PRIMARY))
    out.bind("<Leave>", lambda e: out.config(bg=CARD_BG, fg=TEXT_TERTIARY))
    out.pack(side="left", padx=(6, 0), pady=8)


# ============================================================
# EVENT CARD — text-first, thin border, neutral palette
# ============================================================

class EventCard(tk.Frame):
    def __init__(self, parent, event, on_book=None, on_edit=None, on_delete=None):
        super().__init__(parent, bg=CARD_BG,
                         highlightbackground=BORDER, highlightthickness=1)
        inner = tk.Frame(self, bg=CARD_BG, padx=18, pady=16)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text=event["event_name"], font=FONT_H2,
                 bg=CARD_BG, fg=TEXT_PRIMARY, anchor="w",
                 wraplength=260, justify="left").pack(fill="x")
        tk.Label(inner, text=event["category"], font=FONT_SMALL,
                 bg=CARD_BG, fg=TEXT_TERTIARY, anchor="w"
                 ).pack(fill="x", pady=(2, 12))

        for icon_char, text in [
            ("📍", event["city"]),
            ("📅", f"{event['event_date']} · {event['start_time']}"),
            ("💺", f"{event['available_seats']} of {event['total_seats']} seats"),
        ]:
            row = tk.Frame(inner, bg=CARD_BG)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=icon_char, font=FONT_TINY, bg=CARD_BG,
                     fg=TEXT_TERTIARY, width=2, anchor="w").pack(side="left")
            tk.Label(row, text=text, font=FONT_SMALL, bg=CARD_BG,
                     fg=TEXT_SECONDARY, anchor="w").pack(side="left")

        tk.Label(inner, text=f"₹{float(event['ticket_price']):.0f}",
                 font=FONT_PRICE, bg=CARD_BG, fg=TEXT_PRIMARY, anchor="w"
                 ).pack(fill="x", pady=(14, 10))

        btn_row = tk.Frame(inner, bg=CARD_BG)
        btn_row.pack(fill="x")
        if on_book:
            primary_button(btn_row, "Book now",
                           lambda: on_book(event)).pack(fill="x")
        elif on_edit and on_delete:
            secondary_button(btn_row, "Edit",
                             lambda: on_edit(event)).pack(
                                 side="left", expand=True, fill="x", padx=(0, 4))
            accent_button(btn_row, "Delete",
                          lambda: on_delete(event)).pack(
                              side="left", expand=True, fill="x", padx=(4, 0))


# ============================================================
# LOGIN — Notion-minimal: floating centered form, small logo
# ============================================================

class LoginWindow:
    def __init__(self, root, app):
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        wrap = tk.Frame(self.frame, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        # Small logo + wordmark
        logo_row = tk.Frame(wrap, bg=BG)
        logo_row.pack(pady=(0, 30))
        tk.Label(logo_row, text="🎟", font=(FONT_FAMILY, 22),
                 bg=BG, fg=PRIMARY).pack(side="left", padx=(0, 8))
        tk.Label(logo_row, text="Eventra", font=(FONT_FAMILY, 16, "bold"),
                 bg=BG, fg=TEXT_PRIMARY).pack(side="left")

        # Heading
        tk.Label(wrap, text="Sign in to Eventra", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(wrap, text="Welcome back. Enter your details to continue.",
                 font=FONT_BODY, bg=BG, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(6, 26))

        # Email
        tk.Label(wrap, text="EMAIL", font=FONT_LABEL,
                 bg=BG, fg=TEXT_SECONDARY).pack(anchor="w", pady=(0, 6))
        self.email_wrapper, self.email_entry = modern_entry(wrap, width=34)
        self.email_wrapper.pack(fill="x", pady=(0, 16))

        # Password
        tk.Label(wrap, text="PASSWORD", font=FONT_LABEL,
                 bg=BG, fg=TEXT_SECONDARY).pack(anchor="w", pady=(0, 6))
        self.pw_wrapper, self.pw_entry = modern_entry(wrap, show="•", width=34)
        self.pw_wrapper.pack(fill="x", pady=(0, 8))

        # Error
        self.err = tk.Label(wrap, text="", font=FONT_SMALL,
                             bg=BG, fg=ACCENT)
        self.err.pack(anchor="w", pady=(0, 12))

        # Primary button
        primary_button(wrap, "Continue", self._do, width=34
                       ).pack(fill="x", pady=(0, 20))

        # Footer link
        footer = tk.Frame(wrap, bg=BG)
        footer.pack()
        tk.Label(footer, text="Don't have an account?", font=FONT_SMALL,
                 bg=BG, fg=TEXT_SECONDARY).pack(side="left")
        link = tk.Label(footer, text="Sign up", font=(FONT_FAMILY, 9, "bold"),
                        bg=BG, fg=PRIMARY, cursor="hand2")
        link.pack(side="left", padx=(4, 0))
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
        wrap = tk.Frame(self.frame, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        logo_row = tk.Frame(wrap, bg=BG)
        logo_row.pack(pady=(0, 24))
        tk.Label(logo_row, text="🎟", font=(FONT_FAMILY, 20),
                 bg=BG, fg=PRIMARY).pack(side="left", padx=(0, 8))
        tk.Label(logo_row, text="Eventra", font=(FONT_FAMILY, 15, "bold"),
                 bg=BG, fg=TEXT_PRIMARY).pack(side="left")

        tk.Label(wrap, text="Create your account", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(wrap, text="It only takes a minute.",
                 font=FONT_BODY, bg=BG, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(6, 22))

        self.e = {}
        for label, key, is_pw in [
            ("FULL NAME", "name", False),
            ("EMAIL", "email", False),
            ("PHONE (10 DIGITS)", "phone", False),
            ("PASSWORD", "password", True),
            ("CONFIRM PASSWORD", "confirm", True),
        ]:
            tk.Label(wrap, text=label, font=FONT_LABEL,
                     bg=BG, fg=TEXT_SECONDARY).pack(anchor="w", pady=(0, 5))
            w, ent = modern_entry(wrap, show="•" if is_pw else None, width=34)
            w.pack(fill="x", pady=(0, 12))
            self.e[key] = ent

        self.err = tk.Label(wrap, text="", font=FONT_SMALL,
                             bg=BG, fg=ACCENT)
        self.err.pack(anchor="w", pady=(0, 10))

        primary_button(wrap, "Create account", self._do, width=34
                       ).pack(fill="x", pady=(0, 16))

        footer = tk.Frame(wrap, bg=BG)
        footer.pack()
        tk.Label(footer, text="Already have an account?",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY).pack(side="left")
        link = tk.Label(footer, text="Sign in",
                        font=(FONT_FAMILY, 9, "bold"),
                        bg=BG, fg=PRIMARY, cursor="hand2")
        link.pack(side="left", padx=(4, 0))
        link.bind("<Button-1>", lambda e: self.app.show_login())

        self.e["name"].focus_set()

    def _do(self):
        pw = self.e["password"].get()
        if pw != self.e["confirm"].get():
            self.err.config(text="✕  Passwords do not match.", fg=ACCENT)
            return
        ok, res = register_user(self.e["name"].get(), self.e["email"].get(),
                                self.e["phone"].get(), pw)
        if ok:
            self.err.config(text="✓  Account created. Redirecting...",
                             fg=SUCCESS)
            self.frame.after(1200, self.app.show_login)
        else:
            self.err.config(text=f"✕  {res}", fg=ACCENT)

    def destroy(self):
        self.frame.destroy()


# ============================================================
# USER EVENT GRID
# ============================================================

class UserEventsWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        make_navbar(self.frame, self.app.user, self.app)

        # Page header
        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=32, pady=(28, 4))
        tk.Label(header, text="Upcoming events", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(header, text="Browse and book your tickets in seconds.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(4, 0))

        # Search row
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

        # Scrollable card grid
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
        self._render(list_events())

    def _search(self):
        kw = self.search_var.get().strip()
        self._render(search_events(kw) if kw else list_events())

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
            EventCard(self.inner, ev, on_book=self._book).grid(
                row=r, column=c, padx=8, pady=8, sticky="nsew")
        for c in range(3):
            self.inner.grid_columnconfigure(c, weight=1, minsize=300)

    def _book(self, event):
        BookingModal(self.root, self.app, event)

    def destroy(self):
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.frame.unbind_all(seq)
        self.frame.destroy()


# ============================================================
# BOOKING MODAL + SUCCESS POPUP
# ============================================================

class BookingModal(tk.Toplevel):
    def __init__(self, parent, app, event):
        super().__init__(parent)
        self.app = app
        self.event = event
        self.title("Book tickets")
        self.geometry("480x600")
        self.configure(bg=CARD_BG)
        self.grab_set()
        self._build()

    def _build(self):
        pad = 32
        tk.Label(self, text=self.event["event_name"], font=(FONT_FAMILY, 16, "bold"),
                 bg=CARD_BG, fg=TEXT_PRIMARY).pack(pady=(pad, 2),
                                                    padx=pad, anchor="w")
        tk.Label(self, text=self.event["category"], font=FONT_SMALL,
                 bg=CARD_BG, fg=TEXT_TERTIARY).pack(padx=pad, anchor="w")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=pad, pady=18)

        info = tk.Frame(self, bg=CARD_BG)
        info.pack(fill="x", padx=pad)
        for label, value in [
            ("Venue", self.event["venue"]),
            ("City",  self.event["city"]),
            ("Date",  f"{self.event['event_date']} at {self.event['start_time']}"),
            ("Price", f"₹{float(self.event['ticket_price']):.2f} per ticket"),
            ("Seats", f"{self.event['available_seats']} available"),
        ]:
            row = tk.Frame(info, bg=CARD_BG)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label, font=FONT_SMALL, bg=CARD_BG,
                     fg=TEXT_TERTIARY, width=8, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=FONT_SMALL, bg=CARD_BG,
                     fg=TEXT_PRIMARY, anchor="w").pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=pad, pady=18)

        tk.Label(self, text="NUMBER OF TICKETS", font=FONT_LABEL,
                 bg=CARD_BG, fg=TEXT_SECONDARY).pack(padx=pad, anchor="w")
        counter = tk.Frame(self, bg=CARD_BG)
        counter.pack(padx=pad, pady=8, anchor="w")

        self.qty = tk.IntVar(value=1)
        dec = tk.Button(counter, text="−", font=(FONT_FAMILY, 14),
                        bg=BG_SUBTLE, fg=TEXT_PRIMARY, relief="flat",
                        cursor="hand2", width=3, command=self._dec, bd=0)
        dec.pack(side="left")
        tk.Label(counter, textvariable=self.qty, font=(FONT_FAMILY, 15, "bold"),
                 bg=CARD_BG, fg=TEXT_PRIMARY, width=4).pack(side="left")
        inc = tk.Button(counter, text="+", font=(FONT_FAMILY, 14),
                        bg=BG_SUBTLE, fg=TEXT_PRIMARY, relief="flat",
                        cursor="hand2", width=3, command=self._inc, bd=0)
        inc.pack(side="left")

        self.total_lbl = tk.Label(
            self, text=f"Total: ₹{float(self.event['ticket_price']):.2f}",
            font=(FONT_FAMILY, 14, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
        self.total_lbl.pack(padx=pad, pady=(8, 16), anchor="w")

        tk.Label(self, text="PAYMENT METHOD", font=FONT_LABEL,
                 bg=CARD_BG, fg=TEXT_SECONDARY).pack(padx=pad, anchor="w")
        self.pay = tk.StringVar(value="UPI")
        pr = tk.Frame(self, bg=CARD_BG)
        pr.pack(padx=pad, pady=8, anchor="w")
        for m in ["UPI", "Card", "Cash"]:
            tk.Radiobutton(pr, text=m, variable=self.pay, value=m,
                          font=FONT_SMALL, bg=CARD_BG, fg=TEXT_PRIMARY,
                          activebackground=CARD_BG, selectcolor=CARD_BG,
                          cursor="hand2").pack(side="left", padx=(0, 18))

        self.err = tk.Label(self, text="", font=FONT_SMALL,
                             bg=CARD_BG, fg=ACCENT)
        self.err.pack(pady=6)

        row = tk.Frame(self, bg=CARD_BG)
        row.pack(pady=14)
        primary_button(row, "Confirm booking",
                       self._confirm).pack(side="left", padx=(0, 8))
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
        win.geometry("420x320")
        win.configure(bg=CARD_BG)
        win.grab_set()

        tk.Label(win, text="✓", font=(FONT_FAMILY, 36),
                 bg=CARD_BG, fg=SUCCESS).pack(pady=(28, 8))
        tk.Label(win, text="Booking confirmed", font=(FONT_FAMILY, 16, "bold"),
                 bg=CARD_BG, fg=TEXT_PRIMARY).pack()

        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=36, pady=20)

        body = tk.Frame(win, bg=CARD_BG)
        body.pack(padx=36)
        for label, value in [("Booking ID", f"#{info['booking_id']}"),
                              ("Transaction", info["txn_id"]),
                              ("Total paid", f"₹{info['total']:.2f}")]:
            row = tk.Frame(body, bg=CARD_BG)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label, font=FONT_SMALL, bg=CARD_BG,
                     fg=TEXT_TERTIARY, width=13, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=(FONT_FAMILY, 10, "bold"),
                     bg=CARD_BG, fg=TEXT_PRIMARY, anchor="w").pack(side="left")

        primary_button(win, "Done", win.destroy).pack(pady=24)


# ============================================================
# MY BOOKINGS
# ============================================================

class MyBookingsWindow:
    def __init__(self, root, app):
        self.app = app
        self.frame = tk.Frame(root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        make_navbar(self.frame, self.app.user, self.app)

        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=32, pady=(28, 4))
        tk.Label(header, text="My bookings", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY).pack(anchor="w")
        tk.Label(header, text="Every booking you've made on Eventra.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(4, 0))

        tf = tk.Frame(self.frame, bg=BG)
        tf.pack(fill="both", expand=True, padx=32, pady=(20, 12))

        cols = ("id", "event", "qty", "total", "date", "status")
        self.tree = ttk.Treeview(tf, columns=cols, show="headings", height=15)
        heads = {"id": "Booking ID", "event": "Event", "qty": "Qty",
                 "total": "Total", "date": "Date", "status": "Status"}
        for c in cols:
            self.tree.heading(c, text=heads[c])
            self.tree.column(c, anchor="w", width=150)
        self.tree.pack(fill="both", expand=True)

        row = tk.Frame(self.frame, bg=BG)
        row.pack(fill="x", padx=32, pady=(0, 24))
        accent_button(row, "Cancel selected booking",
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
            messagebox.showwarning("No selection",
                                    "Select a booking first.")
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