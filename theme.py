import platform
import tkinter as tk
from tkinter import ttk

_OS = platform.system()
if _OS == "Windows":
    FONT_FAMILY = "Segoe UI"
elif _OS == "Darwin":
    FONT_FAMILY = "SF Pro Text"
else:
    FONT_FAMILY = "Ubuntu"


# ============================================================
# COLORS — dark theme with violet accent
# ============================================================

BG            = "#09090B"    # page — near black
BG_SIDEBAR    = "#050507"    # sidebar — darkest
BG_ELEVATED   = "#18181B"    # cards / rows
BG_HOVER      = "#27272A"    # hover state
BG_ACTIVE     = "#1E1B4B"    # active nav — dark violet
BORDER        = "#27272A"    # subtle divider
BORDER_STRONG = "#3F3F46"    # visible border (inputs)

TEXT_PRIMARY   = "#FAFAFA"
TEXT_SECONDARY = "#A1A1AA"
TEXT_TERTIARY  = "#71717A"

ACCENT        = "#8B5CF6"
ACCENT_DARK   = "#7C3AED"
ACCENT_LIGHT  = "#A78BFA"

SUCCESS = "#10B981"
DANGER  = "#EF4444"
WARNING = "#F59E0B"

CATEGORY_COLORS = {
    "Music":   "#EC4899",
    "Tech":    "#06B6D4",
    "Food":    "#F59E0B",
    "Sports":  "#10B981",
    "Theatre": "#8B5CF6",
}

CATEGORY_EMOJI = {
    "Music":   "🎵",
    "Tech":    "💻",
    "Food":    "🍔",
    "Sports":  "🏃",
    "Theatre": "🎭",
}


# ============================================================
# TYPE SCALE — generous for Ubuntu DPI
# ============================================================

FONT_DISPLAY = (FONT_FAMILY, 34, "bold")
FONT_H1      = (FONT_FAMILY, 26, "bold")
FONT_H2      = (FONT_FAMILY, 17, "bold")
FONT_H3      = (FONT_FAMILY, 14, "bold")
FONT_BODY    = (FONT_FAMILY, 12)
FONT_SMALL   = (FONT_FAMILY, 11)
FONT_TINY    = (FONT_FAMILY, 10)
FONT_LABEL   = (FONT_FAMILY, 9, "bold")
FONT_BUTTON  = (FONT_FAMILY, 12, "bold")
FONT_NAV     = (FONT_FAMILY, 12)
FONT_PRICE   = (FONT_FAMILY, 22, "bold")

WINDOW_W = 1280
WINDOW_H = 820


# ============================================================
# UI SCALE — makes fixed-pixel sizes follow the screen size
# ============================================================
# Fonts are in points (they follow Tk's "scaling"), but paddings, widths and
# heights are in pixels. main.py sets UI_SCALE once at startup (1.0 = the
# original 1920x1080 design) so both grow/shrink together on any screen.

UI_SCALE = 1.0


def set_ui_scale(value):
    global UI_SCALE
    UI_SCALE = value


def S(px):
    """Scale a pixel measurement by the current UI scale."""
    return max(1, int(round(px * UI_SCALE)))


# ============================================================
# ttk STYLES
# ============================================================

def setup_styles(root):
    s = ttk.Style(root)
    s.theme_use("clam")

    s.configure("Treeview",
                background=BG_ELEVATED,
                fieldbackground=BG_ELEVATED,
                foreground=TEXT_PRIMARY,
                rowheight=S(46),
                font=FONT_BODY,
                borderwidth=0)
    s.configure("Treeview.Heading",
                background=BG_SIDEBAR,
                foreground=TEXT_SECONDARY,
                font=FONT_LABEL,
                relief="flat",
                padding=(S(16), S(14)))
    s.map("Treeview.Heading", background=[("active", BG_HOVER)])
    s.map("Treeview",
          background=[("selected", BG_ACTIVE)],
          foreground=[("selected", TEXT_PRIMARY)])

    s.configure("TNotebook", background=BG, borderwidth=0)
    s.configure("TNotebook.Tab",
                font=FONT_SMALL,
                padding=(S(20), S(14)),
                background=BG_ELEVATED,
                foreground=TEXT_SECONDARY,
                borderwidth=0)
    s.map("TNotebook.Tab",
          background=[("selected", BG_ACTIVE)],
          foreground=[("selected", TEXT_PRIMARY)])


# ============================================================
# WIDGET FACTORIES
# ============================================================

def primary_button(parent, text, command, width=None):
    b = tk.Button(parent, text=text, command=command,
                  bg=ACCENT, fg="white", font=FONT_BUTTON,
                  activebackground=ACCENT_DARK, activeforeground="white",
                  relief="flat", cursor="hand2", pady=S(11), padx=S(22),
                  borderwidth=0)
    b.bind("<Enter>", lambda e: b.config(bg=ACCENT_DARK))
    b.bind("<Leave>", lambda e: b.config(bg=ACCENT))
    if width:
        b.config(width=width)
    return b


def secondary_button(parent, text, command, width=None):
    b = tk.Button(parent, text=text, command=command,
                  bg=BG_HOVER, fg=TEXT_PRIMARY, font=FONT_BUTTON,
                  activebackground=BORDER_STRONG, activeforeground=TEXT_PRIMARY,
                  relief="flat", cursor="hand2", pady=S(11), padx=S(22),
                  borderwidth=0)
    b.bind("<Enter>", lambda e: b.config(bg=BORDER_STRONG))
    b.bind("<Leave>", lambda e: b.config(bg=BG_HOVER))
    if width:
        b.config(width=width)
    return b


def danger_button(parent, text, command, width=None):
    b = tk.Button(parent, text=text, command=command,
                  bg=BG_ELEVATED, fg=DANGER, font=FONT_BUTTON,
                  activebackground="#2A1A1A", activeforeground=DANGER,
                  relief="solid", cursor="hand2", pady=S(10), padx=S(20),
                  borderwidth=1, highlightbackground="#7F1D1D")
    b.bind("<Enter>", lambda e: b.config(bg="#2A1A1A"))
    b.bind("<Leave>", lambda e: b.config(bg=BG_ELEVATED))
    if width:
        b.config(width=width)
    return b


def ghost_button(parent, text, command):
    b = tk.Button(parent, text=text, command=command,
                  bg=BG, fg=TEXT_SECONDARY, font=FONT_BODY,
                  activebackground=BG_HOVER, activeforeground=TEXT_PRIMARY,
                  relief="flat", cursor="hand2", padx=S(14), pady=S(9),
                  borderwidth=0)
    b.bind("<Enter>", lambda e: b.config(bg=BG_HOVER, fg=TEXT_PRIMARY))
    b.bind("<Leave>", lambda e: b.config(bg=BG, fg=TEXT_SECONDARY))
    return b


def modern_entry(parent, show=None, width=36):
    wrapper = tk.Frame(parent, bg=BORDER_STRONG, padx=1, pady=1)
    entry = tk.Entry(wrapper, font=FONT_BODY, width=width, bd=0,
                     relief="flat", bg=BG_ELEVATED, fg=TEXT_PRIMARY,
                     insertbackground=TEXT_PRIMARY, highlightthickness=0)
    if show:
        entry.config(show=show)
    entry.pack(fill="x", ipady=S(10), padx=S(14))
    entry.bind("<FocusIn>", lambda e: wrapper.config(bg=ACCENT))
    entry.bind("<FocusOut>", lambda e: wrapper.config(bg=BORDER_STRONG))
    return wrapper, entry


def category_color(category):
    return CATEGORY_COLORS.get(category, ACCENT)


def category_emoji(category):
    return CATEGORY_EMOJI.get(category, "🎉")

def center_window(win, w, h):
    """Center a Toplevel window on the screen."""
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")