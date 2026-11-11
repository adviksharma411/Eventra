# import os
# import platform
# import tkinter as tk
# from theme import setup_styles, BG, WINDOW_W, WINDOW_H


# # ============================================================
# # DPI / SCALING
# # ============================================================

# def _detect_windows_dpi():
#     """Query real DPI from Windows API (more reliable than Tk on Windows)."""
#     try:
#         from ctypes import windll
#         hdc = windll.user32.GetDC(0)
#         dpi = windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
#         windll.user32.ReleaseDC(0, hdc)
#         if dpi and dpi > 0:
#             return dpi
#     except Exception:
#         pass
#     return 96  # fallback: standard 100%


# def _setup_dpi(root):
#     """Configure DPI scaling per OS. Ensures comfortable font size everywhere."""
#     # Manual override via env var: EVENTRA_SCALING=1.75 python main.py
#     try:
#         override = float(os.environ.get("EVENTRA_SCALING", "0"))
#         if override > 0:
#             root.tk.call("tk", "scaling", override)
#             return
#     except Exception:
#         pass

#     _OS = platform.system()
#     try:
#         if _OS == "Windows":
#             # Tell Windows we handle DPI (prevents blurry text)
#             try:
#                 from ctypes import windll
#                 try:
#                     windll.shcore.SetProcessDpiAwareness(2)  # per-monitor (Win 8.1+)
#                 except Exception:
#                     windll.user32.SetProcessDPIAware()       # legacy fallback
#             except Exception:
#                 pass

#             dpi = _detect_windows_dpi()
#             scaling = dpi / 72.0
#             # Floor at 1.5 so text is never tiny on Windows laptops
#             root.tk.call("tk", "scaling", max(scaling, 1.5))

#         elif _OS == "Darwin":
#             # macOS handles DPI natively — leave default
#             pass

#         else:
#             # Linux / Ubuntu
#             root.tk.call("tk", "scaling", 1.35)
#     except Exception:
#         pass


# # ============================================================
# # APP
# # ============================================================

# class EventraApp:
#     def __init__(self):
#         self.root = tk.Tk()
#         _setup_dpi(self.root)

#         self.root.title("Eventra — Event Management & Ticketing")

#         # Launch maximized
#         sw = self.root.winfo_screenwidth()
#         sh = self.root.winfo_screenheight()
#         self.root.geometry(f"{sw}x{sh}+0+0")

#         self.root.minsize(1000, 640)
#         self.root.configure(bg=BG)
#         setup_styles(self.root)

#         self.current = None
#         self.user = None

#     def _clear(self):
#         if self.current:
#             try:
#                 self.current.destroy()
#             except Exception:
#                 pass
#             self.current = None

#     # ---- Auth ----
#     def show_login(self):
#         self._clear()
#         self.user = None
#         from gui_user import LoginWindow
#         self.current = LoginWindow(self.root, self)

#     def show_register(self):
#         self._clear()
#         from gui_user import RegisterWindow
#         self.current = RegisterWindow(self.root, self)

#     def on_login_success(self, user):
#         self.user = user
#         if user["role"] == "admin":
#             self.show_admin_home()
#         else:
#             self.show_user_home()

#     # ---- User ----
#     def show_user_home(self):
#         self._clear()
#         from gui_user import UserEventsWindow
#         self.current = UserEventsWindow(self.root, self)

#     def show_my_bookings(self):
#         self._clear()
#         from gui_user import MyBookingsWindow
#         self.current = MyBookingsWindow(self.root, self)

#     # ---- Admin ----
#     def show_admin_home(self):
#         self._clear()
#         from gui_admin import AdminEventsWindow
#         self.current = AdminEventsWindow(self.root, self)

#     def show_add_event(self):
#         self._clear()
#         from gui_admin import AddEditEventForm
#         self.current = AddEditEventForm(self.root, self, mode="add")

#     def show_edit_event(self, event):
#         self._clear()
#         from gui_admin import AddEditEventForm
#         self.current = AddEditEventForm(self.root, self, mode="edit", event=event)

#     def show_admin_users(self):
#         self._clear()
#         from gui_admin import UsersWindow
#         self.current = UsersWindow(self.root, self)

#     def show_admin_bookings(self):
#         self._clear()
#         from gui_admin import AllBookingsWindow
#         self.current = AllBookingsWindow(self.root, self)

#     def show_reports(self):
#         self._clear()
#         from gui_admin import ReportsWindow
#         self.current = ReportsWindow(self.root, self)

#     # ---- Misc ----
#     def logout(self):
#         self.show_login()

#     def run(self):
#         self.show_login()
#         self.root.mainloop()


# if __name__ == "__main__":
#     EventraApp().run()


import os
import platform
import tkinter as tk
import theme
from theme import setup_styles, BG


_OS = platform.system()

# The UI was designed on Ubuntu with Tk scaling 1.35 at roughly 1920x1080.
BASE_SCALING = 1.35
REF_W, REF_H = 1920, 1000   # reference usable area (1080p minus taskbar/title bar)


# ============================================================
# DPI / SCALING
# ============================================================

def _enable_windows_dpi_awareness():
    """Must be called BEFORE tk.Tk() — Windows ignores it afterwards."""
    if _OS != "Windows":
        return
    try:
        from ctypes import windll
        try:
            windll.shcore.SetProcessDpiAwareness(2)  # per-monitor (Win 8.1+)
        except Exception:
            windll.user32.SetProcessDPIAware()       # legacy fallback
    except Exception:
        pass


def _setup_dpi(root):
    """
    Pick a Tk font scaling and a UI scale (for pixel sizes) that match the
    screen, so the layout looks the same on every laptop.

    Overrides:
      EVENTRA_SCALING=1.75   force Tk font scaling directly
      EVENTRA_UI_SCALE=0.8   force the pixel-size scale (Windows)
    """
    try:
        override = float(os.environ.get("EVENTRA_SCALING", "0"))
        if override > 0:
            root.tk.call("tk", "scaling", override)
            theme.set_ui_scale(override / BASE_SCALING)
            return
    except Exception:
        pass

    try:
        if _OS == "Windows":
            sw = root.winfo_screenwidth()
            sh = root.winfo_screenheight()
            ui = min(sw / REF_W, (sh - 80) / REF_H, 1.5)
            ui = max(0.7, ui)
            try:
                ui = float(os.environ.get("EVENTRA_UI_SCALE", ui))
            except ValueError:
                pass
            # Same pixel size for a "12pt" font as on the Ubuntu laptop,
            # shrunk/grown with the screen. Independent of Windows' 125%/150%.
            root.tk.call("tk", "scaling", BASE_SCALING * ui)
            theme.set_ui_scale(ui)

        elif _OS == "Darwin":
            pass  # macOS handles DPI natively

        else:
            root.tk.call("tk", "scaling", BASE_SCALING)  # Linux / Ubuntu
    except Exception:
        pass


# ============================================================
# APP
# ============================================================

class EventraApp:
    def __init__(self):
        _enable_windows_dpi_awareness()
        self.root = tk.Tk()
        _setup_dpi(self.root)

        self.root.title("Eventra — Event Management & Ticketing")

        # Launch maximized
        if _OS == "Windows":
            # "zoomed" respects the taskbar and title bar; a manual
            # screen-sized geometry pushes the bottom of the window off-screen.
            self.root.state("zoomed")
        else:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}+0+0")

        self.root.minsize(900, 600)
        self.root.configure(bg=BG)
        setup_styles(self.root)

        self.current = None
        self.user = None

    def _clear(self):
        if self.current:
            try:
                self.current.destroy()
            except Exception:
                pass
            self.current = None

    # ---- Auth ----
    def show_login(self):
        self._clear()
        self.user = None
        from gui_user import LoginWindow
        self.current = LoginWindow(self.root, self)

    def show_register(self):
        self._clear()
        from gui_user import RegisterWindow
        self.current = RegisterWindow(self.root, self)

    def on_login_success(self, user):
        self.user = user
        if user["role"] == "admin":
            self.show_admin_home()
        else:
            self.show_user_home()

    # ---- User ----
    def show_user_home(self):
        self._clear()
        from gui_user import UserEventsWindow
        self.current = UserEventsWindow(self.root, self)

    def show_my_bookings(self):
        self._clear()
        from gui_user import MyBookingsWindow
        self.current = MyBookingsWindow(self.root, self)

    # ---- Admin ----
    def show_admin_home(self):
        self._clear()
        from gui_admin import AdminEventsWindow
        self.current = AdminEventsWindow(self.root, self)

    def show_add_event(self):
        self._clear()
        from gui_admin import AddEditEventForm
        self.current = AddEditEventForm(self.root, self, mode="add")

    def show_edit_event(self, event):
        self._clear()
        from gui_admin import AddEditEventForm
        self.current = AddEditEventForm(self.root, self, mode="edit", event=event)

    def show_admin_users(self):
        self._clear()
        from gui_admin import UsersWindow
        self.current = UsersWindow(self.root, self)

    def show_admin_bookings(self):
        self._clear()
        from gui_admin import AllBookingsWindow
        self.current = AllBookingsWindow(self.root, self)

    def show_reports(self):
        self._clear()
        from gui_admin import ReportsWindow
        self.current = ReportsWindow(self.root, self)

    # ---- Misc ----
    def logout(self):
        self.show_login()

    def run(self):
        self.show_login()
        self.root.mainloop()


if __name__ == "__main__":
    EventraApp().run()