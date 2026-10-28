import os
import platform
import tkinter as tk
from theme import setup_styles, BG, WINDOW_W, WINDOW_H


def _setup_dpi(root):
    """Configure DPI scaling per OS so UI is sized correctly on all laptops."""
    # Manual override via env var (for tuning): EVENTRA_SCALING=1.5 python main.py
    try:
        override = float(os.environ.get("EVENTRA_SCALING", "0"))
        if override > 0:
            root.tk.call("tk", "scaling", override)
            return
    except Exception:
        pass

    _OS = platform.system()
    try:
        if _OS == "Windows":
            # Tell Windows we handle DPI ourselves (prevents double-scaling / blur)
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)  # system DPI aware
            except Exception:
                pass

            # Set Tk scaling from actual screen DPI (96 = 100%, 144 = 150%)
            dpi = root.winfo_fpixels("1i")
            root.tk.call("tk", "scaling", dpi / 72.0)

        elif _OS == "Darwin":
            # macOS handles DPI natively — leave default
            pass

        else:
            # Linux / Ubuntu — force good base scaling
            root.tk.call("tk", "scaling", 1.35)
    except Exception:
        pass


class EventraApp:
    def __init__(self):
        self.root = tk.Tk()
        _setup_dpi(self.root)

        self.root.title("Eventra — Event Management & Ticketing")

        # Launch maximized
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{sw}x{sh}+0+0")

        self.root.minsize(1000, 640)
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

    # Auth
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

    # User
    def show_user_home(self):
        self._clear()
        from gui_user import UserEventsWindow
        self.current = UserEventsWindow(self.root, self)

    def show_my_bookings(self):
        self._clear()
        from gui_user import MyBookingsWindow
        self.current = MyBookingsWindow(self.root, self)

    # Admin
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

    def logout(self):
        self.show_login()

    def run(self):
        self.show_login()
        self.root.mainloop()


if __name__ == "__main__":
    EventraApp().run()