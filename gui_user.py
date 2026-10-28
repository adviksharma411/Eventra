"""
gui_user.py
------------
Sidebar shell + all pre-auth (Login/Register) and user-facing screens.
Admin screens live in gui_admin.py; they call build_shell() from here.
"""

import tkinter as tk
from tkinter import ttk

from auth import login_user, register_user
from events import list_events, search_events
from bookings import book_ticket, my_bookings, cancel_booking
from theme import (
    FONT_FAMILY, BG, BG_SIDEBAR, BG_ELEVATED, BG_HOVER, BG_ACTIVE,
    BORDER, BORDER_STRONG, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_TERTIARY,
    ACCENT, ACCENT_DARK, ACCENT_LIGHT, SUCCESS, DANGER, WARNING,
    FONT_DISPLAY, FONT_H1, FONT_H2, FONT_H3, FONT_BODY, FONT_SMALL,
    FONT_TINY, FONT_LABEL, FONT_BUTTON, FONT_NAV, FONT_PRICE,
    primary_button, secondary_button, danger_button, ghost_button,
    modern_entry, category_color, category_emoji,
)


# ============================================================
# DIALOGS — custom, always on top, auto-sized
# ============================================================

def show_confirm_dialog(parent, title, message, on_confirm,
                        danger=True, confirm_label="Confirm",
                        cancel_label="Cancel"):
    """Styled confirmation dialog. Auto-sizes to content."""
    win = tk.Toplevel(parent)
    win.title(title)
    win.configure(bg=BG_ELEVATED)
    win.transient(parent)
    win.grab_set()
    win.resizable(False, False)

    accent = DANGER if danger else ACCENT

    tk.Frame(win, bg=accent, height=4).pack(fill="x")

    body = tk.Frame(win, bg=BG_ELEVATED, padx=40, pady=36)
    body.pack(fill="both", expand=True)

    header = tk.Frame(body, bg=BG_ELEVATED)
    header.pack(fill="x", pady=(0, 20))

    tk.Label(header, text="⚠" if danger else "ℹ",
             font=(FONT_FAMILY, 36), bg=BG_ELEVATED,
             fg=accent).pack(side="left", padx=(0, 20), anchor="n")

    title_col = tk.Frame(header, bg=BG_ELEVATED)
    title_col.pack(side="left", fill="x", expand=True)
    tk.Label(title_col, text=title,
             font=(FONT_FAMILY, 20, "bold"),
             bg=BG_ELEVATED, fg=TEXT_PRIMARY,
             anchor="w", justify="left",
             wraplength=420).pack(fill="x", pady=(6, 0))

    tk.Label(body, text=message,
             font=(FONT_FAMILY, 12),
             bg=BG_ELEVATED, fg=TEXT_SECONDARY,
             anchor="w", justify="left",
             wraplength=480).pack(fill="x", pady=(0, 32))

    tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=(0, 20))

    row = tk.Frame(body, bg=BG_ELEVATED)
    row.pack(fill="x")

    def do_confirm():
        win.destroy()
        on_confirm()

    def do_cancel():
        win.destroy()

    secondary_button(row, cancel_label, do_cancel).pack(side="left")

    if danger:
        danger_button(row, confirm_label, do_confirm).pack(side="right")
    else:
        primary_button(row, confirm_label, do_confirm).pack(side="right")

    win.update_idletasks()
    w = max(win.winfo_reqwidth(), 580)
    h = win.winfo_reqheight()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    win.bind("<Escape>", lambda e: do_cancel())
    win.lift()
    win.focus_force()
    win.attributes("-topmost", True)
    win.after(300, lambda: win.attributes("-topmost", False))


def show_toast(parent, message, kind="success"):
    """Auto-sized toast at the bottom of the screen. Wraps long messages."""
    colors = {
        "success": (SUCCESS, "✓"),
        "error":   (DANGER,  "✕"),
        "warning": (WARNING, "⚠"),
        "info":    (ACCENT,  "ℹ"),
    }
    color, icon = colors.get(kind, colors["info"])

    win = tk.Toplevel(parent)
    win.overrideredirect(True)
    win.configure(bg=color)
    win.attributes("-topmost", True)

    inner = tk.Frame(win, bg=BG_ELEVATED)
    inner.pack(fill="both", expand=True, padx=3, pady=3)

    tk.Label(inner, text=icon, font=(FONT_FAMILY, 22),
             bg=BG_ELEVATED, fg=color
             ).pack(side="left", padx=(24, 16))

    tk.Label(inner, text=message,
             font=(FONT_FAMILY, 12),
             bg=BG_ELEVATED, fg=TEXT_PRIMARY,
             justify="left", anchor="w",
             wraplength=640
             ).pack(side="left", padx=(0, 28), pady=18)

    win.update_idletasks()
    w = max(420, min(win.winfo_reqwidth(), 800))
    h = win.winfo_reqheight()

    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{sh - h - 80}")

    win.after(3200, win.destroy)


# ============================================================
# SHELL — sidebar + content
# ============================================================

def _nav_item(parent, emoji, label, command, active=False):
    bg = BG_ACTIVE if active else BG_SIDEBAR
    row = tk.Frame(parent, bg=bg, height=60)
    row.pack(fill="x", pady=1)
    row.pack_propagate(False)

    if active:
        tk.Frame(row, bg=ACCENT, width=3).pack(side="left", fill="y")

    inner = tk.Frame(row, bg=bg)
    inner.pack(fill="both", expand=True, padx=(40 if active else 44, 24))

    icon = tk.Label(inner, text=emoji, font=(FONT_FAMILY, 17), bg=bg,
                    fg=TEXT_PRIMARY if active else TEXT_SECONDARY)
    icon.pack(side="left", padx=(0, 18))

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

    sidebar = tk.Frame(parent, bg=BG_SIDEBAR, width=420)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    brand = tk.Frame(sidebar, bg=BG_SIDEBAR)
    brand.pack(fill="x", padx=44, pady=(38, 0))
    tk.Label(brand, text="🎟", font=(FONT_FAMILY, 24), bg=BG_SIDEBAR,
             fg=ACCENT).pack(side="left", padx=(0, 16))
    tk.Label(brand, text="Eventra", font=(FONT_FAMILY, 22, "bold"),
             bg=BG_SIDEBAR, fg=TEXT_PRIMARY).pack(side="left")

    tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=36, pady=30)

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

    bottom = tk.Frame(sidebar, bg=BG_SIDEBAR)
    bottom.pack(side="bottom", fill="x", padx=28, pady=28)

    tk.Frame(bottom, bg=BORDER, height=1).pack(fill="x", pady=(0, 22))

    ucard = tk.Frame(bottom, bg=BG_SIDEBAR)
    ucard.pack(fill="x", padx=10, pady=(0, 6))

    icon = "🛡" if user["role"] == "admin" else "👤"
    tk.Label(ucard, text=icon, font=(FONT_FAMILY, 18), bg=BG_SIDEBAR,
             fg=TEXT_SECONDARY).pack(side="left", padx=(0, 16))

    uinfo = tk.Frame(ucard, bg=BG_SIDEBAR)
    uinfo.pack(side="left", fill="x", expand=True)
    tk.Label(uinfo, text=user["name"], font=(FONT_FAMILY, 14, "bold"),
             bg=BG_SIDEBAR, fg=TEXT_PRIMARY, anchor="w",
             wraplength=300, justify="left").pack(fill="x")
    tk.Label(uinfo, text="Administrator" if user["role"] == "admin" else "Member",
             font=(FONT_FAMILY, 10), bg=BG_SIDEBAR, fg=TEXT_TERTIARY,
             anchor="w").pack(fill="x", pady=(3, 0))

    signout = tk.Button(bottom, text="Sign out", font=FONT_SMALL,
                        bg=BG_SIDEBAR, fg=TEXT_SECONDARY,
                        activebackground=BG_HOVER, activeforeground=TEXT_PRIMARY,
                        relief="flat", cursor="hand2", anchor="w",
                        padx=20, pady=14, borderwidth=0, command=app.logout)
    signout.pack(fill="x", pady=(16, 0))
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

        # Bottom section packed FIRST — always sticks to bottom
        bottom = tk.Frame(self, bg=BG_ELEVATED, padx=24, pady=20)
        bottom.pack(side="bottom", fill="x")

        tk.Label(bottom, text=f"₹{float(event['ticket_price']):.0f}",
                 font=FONT_PRICE, bg=BG_ELEVATED, fg=color, anchor="w"
                 ).pack(fill="x", pady=(0, 14))

        btn_row = tk.Frame(bottom, bg=BG_ELEVATED)
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

        # Content fills space above bottom
        inner = tk.Frame(self, bg=BG_ELEVATED, padx=24, pady=22)
        inner.pack(fill="both", expand=True)

        badge = tk.Frame(inner, bg=BG_ELEVATED)
        badge.pack(fill="x", pady=(0, 14))
        emoji_lbl = tk.Label(badge, text=category_emoji(event["category"]),
                             font=(FONT_FAMILY, 22), bg=BG_ELEVATED, fg=color)
        emoji_lbl.pack(side="left")
        tk.Label(badge, text=event["category"].upper(), font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=color).pack(side="left", padx=(12, 0), pady=6)

        tk.Label(inner, text=event["event_name"], font=FONT_H3,
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY, anchor="w",
                 wraplength=360, justify="left").pack(fill="x")

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=16)

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
                     fg=TEXT_SECONDARY, anchor="w",
                     wraplength=320, justify="left").pack(side="left")


# ============================================================
# LOGIN / REGISTER
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

        tk.Label(wrap, text="🎟", font=(FONT_FAMILY, 44),
                 bg=BG, fg=ACCENT).pack()
        tk.Label(wrap, text="Eventra", font=(FONT_FAMILY, 32, "bold"),
                 bg=BG, fg=TEXT_PRIMARY).pack(pady=(8, 0))
        tk.Label(wrap, text="Event Management & Ticketing",
                 font=FONT_BODY, bg=BG, fg=TEXT_SECONDARY
                 ).pack(pady=(6, 40))

        tk.Label(wrap, text="Sign in", font=FONT_H1,
                 bg=BG, fg=TEXT_PRIMARY, anchor="w").pack(fill="x")
        tk.Label(wrap, text="Welcome back. Continue where you left off.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(6, 26))

        tk.Label(wrap, text="EMAIL", font=FONT_LABEL,
                 bg=BG, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 6))
        self.email_wrapper, self.email_entry = modern_entry(wrap, width=36)
        self.email_wrapper.pack(fill="x", pady=(0, 18))

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

        content_header(
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
            self.inner.grid_columnconfigure(c, weight=1, minsize=340)

    def _book(self, event):
        BookingModal(self.root, self.app, event)

    def destroy(self):
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.frame.unbind_all(seq)
        self.frame.destroy()


# ============================================================
# SCROLLABLE MODAL HELPERS
# ============================================================

def _modal_scroll(win, stripe_color):
    """Fullscreen modal wrapper: fixed stripe on top, scrollable centered content."""
    tk.Frame(win, bg=stripe_color, height=6).pack(fill="x")

    outer = tk.Frame(win, bg=BG_ELEVATED)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer, bg=BG_ELEVATED, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    content = tk.Frame(canvas, bg=BG_ELEVATED)
    win_id = canvas.create_window((0, 0), window=content, anchor="nw")

    def _resize(_=None):
        ch = content.winfo_reqheight()
        cvh = canvas.winfo_height()
        cvw = canvas.winfo_width()
        total = max(ch + 60, cvh)
        canvas.itemconfigure(win_id, width=cvw, height=total)
        canvas.configure(scrollregion=(0, 0, cvw, total))

    content.bind("<Configure>", _resize)
    canvas.bind("<Configure>", _resize)

    inner = tk.Frame(content, bg=BG_ELEVATED)
    inner.pack(expand=True, pady=30)

    win.bind_all("<MouseWheel>",
                 lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
    win.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-2, "units"))
    win.bind_all("<Button-5>", lambda e: canvas.yview_scroll(2, "units"))

    def _cleanup(e):
        if e.widget == win:
            try:
                win.unbind_all("<MouseWheel>")
                win.unbind_all("<Button-4>")
                win.unbind_all("<Button-5>")
            except Exception:
                pass

    win.bind("<Destroy>", _cleanup)
    return inner


# ============================================================
# BOOKING SUCCESS
# ============================================================

def show_booking_success(parent, info):
    win = tk.Toplevel(parent)
    win.title("Booking confirmed")
    win.configure(bg=BG_ELEVATED)
    win.attributes("-fullscreen", True)
    win.bind("<Escape>", lambda e: win.destroy())
    win.grab_set()

    wrap = _modal_scroll(win, SUCCESS)

    tk.Label(wrap, text="✓", font=(FONT_FAMILY, 72),
             bg=BG_ELEVATED, fg=SUCCESS).pack(pady=(0, 12))
    tk.Label(wrap, text="Booking confirmed",
             font=(FONT_FAMILY, 30, "bold"),
             bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack()

    tk.Frame(wrap, bg=BORDER, height=1).pack(fill="x", pady=28)

    body = tk.Frame(wrap, bg=BG_ELEVATED)
    body.pack()
    for label, value in [("Booking ID", f"#{info['booking_id']}"),
                          ("Transaction", info["txn_id"]),
                          ("Total paid", f"₹{info['total']:.2f}")]:
        r = tk.Frame(body, bg=BG_ELEVATED)
        r.pack(fill="x", pady=6)
        tk.Label(r, text=label, font=(FONT_FAMILY, 12), bg=BG_ELEVATED,
                 fg=TEXT_TERTIARY, width=13, anchor="w").pack(side="left")
        tk.Label(r, text=value, font=(FONT_FAMILY, 15, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY, anchor="w"
                 ).pack(side="left")

    primary_button(wrap, "Done", win.destroy).pack(pady=32)


# ============================================================
# BOOKING MODAL
# ============================================================

class BookingModal(tk.Toplevel):
    def __init__(self, parent, app, event):
        super().__init__(parent)
        self.app = app
        self.event = event
        self.title("Book tickets")
        self.configure(bg=BG_ELEVATED)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())
        self.grab_set()
        self._build()

    def _build(self):
        color = category_color(self.event["category"])
        wrap = _modal_scroll(self, color)

        head = tk.Frame(wrap, bg=BG_ELEVATED)
        head.pack(fill="x")
        tk.Label(head, text=category_emoji(self.event["category"]),
                 font=(FONT_FAMILY, 24), bg=BG_ELEVATED, fg=color
                 ).pack(side="left", padx=(0, 14))
        col = tk.Frame(head, bg=BG_ELEVATED)
        col.pack(side="left", fill="x", expand=True)
        tk.Label(col, text=self.event["event_name"],
                 font=(FONT_FAMILY, 22, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY, anchor="w",
                 wraplength=560, justify="left").pack(fill="x")
        tk.Label(col, text=self.event["category"].upper(), font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=color, anchor="w").pack(fill="x")

        tk.Frame(wrap, bg=BORDER, height=1).pack(fill="x", pady=16)

        info = tk.Frame(wrap, bg=BG_ELEVATED)
        info.pack(fill="x")
        for label, value in [
            ("Venue", self.event["venue"]),
            ("City",  self.event["city"]),
            ("Date",  f"{self.event['event_date']} at {self.event['start_time']}"),
            ("Price", f"₹{float(self.event['ticket_price']):.2f} per ticket"),
            ("Seats", f"{self.event['available_seats']} available"),
        ]:
            r = tk.Frame(info, bg=BG_ELEVATED)
            r.pack(fill="x", pady=4)
            tk.Label(r, text=label.upper(), font=FONT_LABEL, bg=BG_ELEVATED,
                     fg=TEXT_TERTIARY, width=8, anchor="w").pack(side="left")
            tk.Label(r, text=value, font=FONT_SMALL, bg=BG_ELEVATED,
                     fg=TEXT_PRIMARY, anchor="w",
                     wraplength=520, justify="left").pack(side="left")

        tk.Frame(wrap, bg=BORDER, height=1).pack(fill="x", pady=16)

        tk.Label(wrap, text="NUMBER OF TICKETS", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY).pack(anchor="w")
        ctr = tk.Frame(wrap, bg=BG_ELEVATED)
        ctr.pack(pady=8, anchor="w")

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
            wrap, text=f"Total: ₹{float(self.event['ticket_price']):.2f}",
            font=(FONT_FAMILY, 16, "bold"), bg=BG_ELEVATED, fg=color)
        self.total_lbl.pack(pady=(8, 16), anchor="w")

        tk.Label(wrap, text="PAYMENT METHOD", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY
                 ).pack(anchor="w", pady=(0, 10))

        self.pay = tk.StringVar(value="UPI")
        pay_row = tk.Frame(wrap, bg=BG_ELEVATED)
        pay_row.pack(pady=(0, 14), anchor="w")

        self._pay_tiles = {}

        def make_tile(value, emoji, label):
            container = tk.Frame(pay_row, bg=BORDER_STRONG, padx=1, pady=1)
            container.pack(side="left", padx=(0, 12))

            tile = tk.Frame(container, bg=BG_ELEVATED, padx=22, pady=12)
            tile.pack(fill="both", expand=True)

            emoji_lbl = tk.Label(tile, text=emoji, font=(FONT_FAMILY, 22),
                                 bg=BG_ELEVATED, fg=TEXT_SECONDARY)
            emoji_lbl.pack()
            text_lbl = tk.Label(tile, text=label,
                                font=(FONT_FAMILY, 10, "bold"),
                                bg=BG_ELEVATED, fg=TEXT_SECONDARY)
            text_lbl.pack(pady=(4, 0))

            def select(e=None):
                self.pay.set(value)
                for v, (c, t, el, tl) in self._pay_tiles.items():
                    if v == value:
                        c.config(bg=ACCENT)
                        el.config(fg=ACCENT)
                        tl.config(fg=TEXT_PRIMARY)
                    else:
                        c.config(bg=BORDER_STRONG)
                        el.config(fg=TEXT_SECONDARY)
                        tl.config(fg=TEXT_SECONDARY)

            def enter(e):
                if self.pay.get() != value:
                    tile.config(bg=BG_HOVER)
                    emoji_lbl.config(bg=BG_HOVER)
                    text_lbl.config(bg=BG_HOVER)

            def leave(e):
                if self.pay.get() != value:
                    tile.config(bg=BG_ELEVATED)
                    emoji_lbl.config(bg=BG_ELEVATED)
                    text_lbl.config(bg=BG_ELEVATED)

            for w in (container, tile, emoji_lbl, text_lbl):
                w.bind("<Button-1>", select)
                w.config(cursor="hand2")
            for w in (tile, emoji_lbl, text_lbl):
                w.bind("<Enter>", enter)
                w.bind("<Leave>", leave)

            self._pay_tiles[value] = (container, tile, emoji_lbl, text_lbl)

        make_tile("UPI", "📱", "UPI")
        make_tile("Card", "💳", "Card")
        make_tile("Cash", "💵", "Cash")

        self._pay_tiles["UPI"][0].config(bg=ACCENT)
        self._pay_tiles["UPI"][2].config(fg=ACCENT)
        self._pay_tiles["UPI"][3].config(fg=TEXT_PRIMARY)

        self.err = tk.Label(wrap, text="", font=FONT_SMALL,
                             bg=BG_ELEVATED, fg=DANGER)
        self.err.pack(pady=8)

        row = tk.Frame(wrap, bg=BG_ELEVATED)
        row.pack(pady=12)
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
        mode = self.pay.get()
        if mode == "Cash":
            self._do_cash_booking()
            return
        app, event, qty = self.app, self.event, self.qty.get()
        self.destroy()
        if mode == "UPI":
            UpiPaymentWindow(app.root, app, event, qty)
        else:
            CardPaymentWindow(app.root, app, event, qty)

    def _do_cash_booking(self):
        ok, res = book_ticket(self.app.user["user_id"], self.event["event_id"],
                              self.qty.get(), "Cash")
        if not ok:
            self.err.config(text=f"✕  {res}")
            return
        self.destroy()
        show_booking_success(self.app.root, res)
        self.app.show_user_home()


# ============================================================
# UPI PAYMENT
# ============================================================

class UpiPaymentWindow(tk.Toplevel):
    def __init__(self, parent, app, event, qty):
        super().__init__(parent)
        self.app = app
        self.event = event
        self.qty = qty
        self.amount = float(event["ticket_price"]) * qty
        self.title("UPI Payment")
        self.configure(bg=BG_ELEVATED)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())
        self.grab_set()
        self._build()

    def _build(self):
        wrap = _modal_scroll(self, ACCENT)

        tk.Label(wrap, text="📱", font=(FONT_FAMILY, 56),
                 bg=BG_ELEVATED, fg=ACCENT).pack()
        tk.Label(wrap, text="Pay with UPI", font=(FONT_FAMILY, 26, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(pady=(8, 4))
        tk.Label(wrap,
                 text=f"{self.event['event_name']}  ·  {self.qty} ticket(s)",
                 font=FONT_SMALL, bg=BG_ELEVATED, fg=TEXT_SECONDARY).pack()

        tk.Label(wrap, text=f"₹{self.amount:.2f}",
                 font=(FONT_FAMILY, 40, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(pady=(16, 22))

        tk.Label(wrap, text="YOUR UPI ID", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 8))
        self.upi_wrap, self.upi_entry = modern_entry(wrap, width=32)
        self.upi_wrap.pack(fill="x", pady=(0, 6))
        self.upi_entry.insert(0, "advik@okhdfc")

        self.err = tk.Label(wrap, text="", font=FONT_SMALL,
                             bg=BG_ELEVATED, fg=DANGER)
        self.err.pack(pady=(6, 14))

        row = tk.Frame(wrap, bg=BG_ELEVATED)
        row.pack()
        primary_button(row, f"Pay ₹{self.amount:.2f}",
                       self._pay).pack(side="left", padx=(0, 10))
        secondary_button(row, "Cancel", self.destroy).pack(side="left")

        tk.Label(wrap,
                 text="This is a simulated payment. No real money is charged.",
                 font=FONT_TINY, bg=BG_ELEVATED, fg=TEXT_TERTIARY
                 ).pack(pady=(24, 0))

        self.upi_entry.focus_set()
        self.upi_entry.bind("<Return>", lambda e: self._pay())

    def _pay(self):
        upi = self.upi_entry.get().strip()
        if "@" not in upi or len(upi) < 5:
            self.err.config(text="✕  Enter a valid UPI ID (e.g. name@bank)")
            return
        self._show_processing()

    def _show_processing(self):
        self.unbind("<Escape>")
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        for w in self.winfo_children():
            w.destroy()

        wrap = _modal_scroll(self, ACCENT)
        tk.Label(wrap, text="⏳", font=(FONT_FAMILY, 64),
                 bg=BG_ELEVATED, fg=ACCENT).pack()
        tk.Label(wrap, text="Processing payment...",
                 font=(FONT_FAMILY, 24, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(pady=(16, 8))
        tk.Label(wrap, text="Do not close this window.",
                 font=FONT_SMALL, bg=BG_ELEVATED, fg=TEXT_SECONDARY).pack()

        self.after(1800, self._complete)

    def _complete(self):
        ok, res = book_ticket(self.app.user["user_id"], self.event["event_id"],
                              self.qty, "UPI")
        if not ok:
            self.destroy()
            show_toast(self.app.root, res, "error")
            return
        self.destroy()
        show_booking_success(self.app.root, res)
        self.app.show_user_home()


# ============================================================
# CARD PAYMENT
# ============================================================

class CardPaymentWindow(tk.Toplevel):
    def __init__(self, parent, app, event, qty):
        super().__init__(parent)
        self.app = app
        self.event = event
        self.qty = qty
        self.amount = float(event["ticket_price"]) * qty
        self.title("Card Payment")
        self.configure(bg=BG_ELEVATED)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())
        self.grab_set()
        self._build()

    def _build(self):
        wrap = _modal_scroll(self, ACCENT)

        tk.Label(wrap, text="💳", font=(FONT_FAMILY, 56),
                 bg=BG_ELEVATED, fg=ACCENT).pack()
        tk.Label(wrap, text="Pay with Card", font=(FONT_FAMILY, 26, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(pady=(8, 4))
        tk.Label(wrap,
                 text=f"{self.event['event_name']}  ·  {self.qty} ticket(s)",
                 font=FONT_SMALL, bg=BG_ELEVATED, fg=TEXT_SECONDARY).pack()

        tk.Label(wrap, text=f"₹{self.amount:.2f}",
                 font=(FONT_FAMILY, 40, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(pady=(16, 20))

        tk.Label(wrap, text="CARD NUMBER", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 6))
        self.num_wrap, self.num_entry = modern_entry(wrap, width=34)
        self.num_wrap.pack(fill="x", pady=(0, 12))
        self.num_entry.insert(0, "4242 4242 4242 4242")

        tk.Label(wrap, text="NAME ON CARD", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 6))
        self.name_wrap, self.name_entry = modern_entry(wrap, width=34)
        self.name_wrap.pack(fill="x", pady=(0, 12))
        self.name_entry.insert(0, self.app.user["name"].upper())

        row = tk.Frame(wrap, bg=BG_ELEVATED)
        row.pack(fill="x", pady=(0, 12))

        left = tk.Frame(row, bg=BG_ELEVATED)
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Label(left, text="EXPIRY (MM/YY)", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 6))
        self.exp_wrap, self.exp_entry = modern_entry(left, width=14)
        self.exp_wrap.pack(fill="x")
        self.exp_entry.insert(0, "12/28")

        right = tk.Frame(row, bg=BG_ELEVATED)
        right.pack(side="left", fill="x", expand=True, padx=(8, 0))
        tk.Label(right, text="CVV", font=FONT_LABEL,
                 bg=BG_ELEVATED, fg=TEXT_SECONDARY, anchor="w"
                 ).pack(fill="x", pady=(0, 6))
        self.cvv_wrap, self.cvv_entry = modern_entry(right, show="•", width=10)
        self.cvv_wrap.pack(fill="x")

        self.err = tk.Label(wrap, text="", font=FONT_SMALL,
                             bg=BG_ELEVATED, fg=DANGER)
        self.err.pack(pady=(6, 12))

        row = tk.Frame(wrap, bg=BG_ELEVATED)
        row.pack()
        primary_button(row, f"Pay ₹{self.amount:.2f}",
                       self._pay).pack(side="left", padx=(0, 10))
        secondary_button(row, "Cancel", self.destroy).pack(side="left")

        tk.Label(wrap,
                 text="This is a simulated payment. No real money is charged.",
                 font=FONT_TINY, bg=BG_ELEVATED, fg=TEXT_TERTIARY
                 ).pack(pady=(24, 0))

        self.num_entry.focus_set()

    def _pay(self):
        card = self.num_entry.get().replace(" ", "").strip()
        name = self.name_entry.get().strip()
        exp = self.exp_entry.get().strip()
        cvv = self.cvv_entry.get().strip()

        if not (card.isdigit() and len(card) == 16):
            self.err.config(text="✕  Card number must be 16 digits.")
            return
        if not name:
            self.err.config(text="✕  Cardholder name is required.")
            return
        if not (len(exp) == 5 and exp[2] == "/"
                and exp[:2].isdigit() and exp[3:].isdigit()):
            self.err.config(text="✕  Expiry must be in MM/YY format.")
            return
        if not (cvv.isdigit() and len(cvv) == 3):
            self.err.config(text="✕  CVV must be 3 digits.")
            return
        self._show_processing()

    def _show_processing(self):
        self.unbind("<Escape>")
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        for w in self.winfo_children():
            w.destroy()

        wrap = _modal_scroll(self, ACCENT)
        tk.Label(wrap, text="🔒", font=(FONT_FAMILY, 64),
                 bg=BG_ELEVATED, fg=ACCENT).pack()
        tk.Label(wrap, text="Verifying card...",
                 font=(FONT_FAMILY, 24, "bold"),
                 bg=BG_ELEVATED, fg=TEXT_PRIMARY).pack(pady=(16, 8))
        tk.Label(wrap, text="Do not close this window.",
                 font=FONT_SMALL, bg=BG_ELEVATED, fg=TEXT_SECONDARY).pack()

        self.after(2000, self._complete)

    def _complete(self):
        ok, res = book_ticket(self.app.user["user_id"], self.event["event_id"],
                              self.qty, "Card")
        if not ok:
            self.destroy()
            show_toast(self.app.root, res, "error")
            return
        self.destroy()
        show_booking_success(self.app.root, res)
        self.app.show_user_home()


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
        widths = {"id": 120, "event": 320, "qty": 80,
                  "total": 140, "date": 160, "status": 150}
        for c in cols:
            self.tree.heading(c, text=heads[c])
            self.tree.column(c, anchor="w", width=widths[c])
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<Double-1>", lambda e: self._cancel())

        row = tk.Frame(content, bg=BG)
        row.pack(fill="x", padx=40, pady=(0, 32))
        danger_button(row, "Cancel selected booking",
                      self._cancel).pack(side="left")

        self._load()

    def _load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in my_bookings(self.app.user["user_id"]):
            status = r["booking_status"]
            tag = "cancelled" if status == "Cancelled" else "confirmed"
            self.tree.insert("", "end", values=(
                r["booking_id"], r["event_name"], r["num_tickets"],
                f"₹{float(r['total_amount']):.2f}",
                str(r["booking_date"])[:10], status
            ), tags=(tag,))
        self.tree.tag_configure("cancelled", foreground=TEXT_TERTIARY)
        self.tree.tag_configure("confirmed", foreground=TEXT_PRIMARY)

    def _cancel(self):
        sel = self.tree.selection()
        if not sel:
            show_toast(self.app.root, "Select a booking first.", "warning")
            return

        values = self.tree.item(sel[0])["values"]
        try:
            bid = int(values[0])
        except (ValueError, IndexError):
            show_toast(self.app.root, "Could not identify that booking.", "error")
            return
        event_name = values[1]
        status = values[5]

        if status == "Cancelled":
            show_toast(self.app.root,
                       "This booking is already cancelled.", "warning")
            return

        def do_cancel():
            ok, msg = cancel_booking(self.app.user["user_id"], bid)
            if ok:
                show_toast(self.app.root, msg, "success")
                self._load()
            else:
                show_toast(self.app.root, msg, "error")

        show_confirm_dialog(
            self.app.root,
            "Cancel this booking?",
            f"You're about to cancel booking #{bid} for '{event_name}'.\n\n"
            f"The seats will be released back to the event and a refund "
            f"will be processed.",
            do_cancel,
            danger=True,
            confirm_label="Yes, cancel booking",
            cancel_label="Keep booking",
        )

    def destroy(self):
        self.frame.destroy()