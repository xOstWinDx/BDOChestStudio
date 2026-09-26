"""Four distinct environments with independently balanced surfaces and text."""

from dataclasses import dataclass
from PySide6.QtGui import QColor, QPalette


@dataclass(frozen=True)
class Theme:
    background: str = "#10151f"
    surface: str = "#1a2230"
    raised: str = "#242f40"
    border: str = "#3a475c"
    text: str = "#f2f5fa"
    muted: str = "#b2bed0"
    accent: str = "#b3a0ff"
    on_accent: str = "#141026"


THEMES = {
    "midnight": Theme(),
    # Stable ids preserve the user's saved preference across palette revisions.
    "ocean": Theme(
        background="#10221e",
        surface="#1c342d",
        raised="#29463b",
        border="#4d6b5b",
        text="#f3f5e9",
        muted="#b4c9b8",
        accent="#b9d889",
        on_accent="#1a2a13",
    ),
    "ember": Theme(
        background="#e9dfd0",
        surface="#fff9ef",
        raised="#ead8c1",
        border="#b29b83",
        text="#34271e",
        muted="#705b49",
        accent="#aa462c",
        on_accent="#fffaf5",
    ),
    "daylight": Theme("#edf1f7", "#ffffff", "#e4eaf3", "#bdc8d8", "#152239", "#4e6078", "#245ac4", "#ffffff"),
}
LEGACY_THEMES = {
    "Лаванда · тёмная": "midnight",
    "Мята · тёмная": "ocean",
    "Лаванда · светлая": "daylight",
    "Персик · светлая": "daylight",
}


def palette(t):
    p = QPalette()
    for role, color in (
        (QPalette.ColorRole.Window, t.background),
        (QPalette.ColorRole.Base, t.surface),
        (QPalette.ColorRole.AlternateBase, t.raised),
        (QPalette.ColorRole.WindowText, t.text),
        (QPalette.ColorRole.Text, t.text),
        (QPalette.ColorRole.Button, t.raised),
        (QPalette.ColorRole.ButtonText, t.text),
        (QPalette.ColorRole.Highlight, t.accent),
        (QPalette.ColorRole.HighlightedText, t.on_accent),
        (QPalette.ColorRole.ToolTipBase, t.raised),
        (QPalette.ColorRole.ToolTipText, t.text),
        (QPalette.ColorRole.PlaceholderText, t.muted),
    ):
        p.setColor(role, QColor(color))
    return p


def stylesheet(t):
    return f"""
    QWidget {{ color: {t.text}; font-family: 'Segoe UI'; font-size: 14px; }}
    QMainWindow, QWidget#root, QWidget#page, QStackedWidget {{ background: {t.background}; }}
    QFrame#card, QFrame#sidebar, QFrame#hero {{ background: {t.surface}; border: 1px solid {t.border}; border-radius: 18px; }}
    QFrame#hero {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {t.surface},stop:1 {t.raised}); border: none; }}
    QFrame#basketRow {{ background: {t.raised}; border: none; border-radius: 12px; }}
    QFrame#counter {{ background: {t.background}; border: 1px solid {t.border}; border-radius: 11px; }}
    QLabel {{ background: transparent; border: none; }}
    QLabel#title {{ font-size: 31px; font-weight: 700; }}
    QLabel#subtitle {{ color: {t.muted}; }}
    QLabel#eyebrow {{ color: {t.muted}; font-size: 11px; font-weight: 700; }}
    QLabel#cardTitle {{ font-size: 15px; font-weight: 600; }}
    QLabel#metric {{ font-size: 28px; font-weight: 700; color: {t.text}; }}
    QLabel#badge {{ color: {t.accent}; font-size: 12px; font-weight: 600; }}
    QLineEdit {{ background: {t.surface}; border: 1px solid {t.border}; border-radius: 11px; padding: 11px; min-height: 20px; selection-background-color: {t.accent}; selection-color: {t.on_accent}; }}
    QLineEdit:focus {{ border-color: {t.accent}; }}
    QSpinBox {{ background: transparent; border: 1px solid transparent; border-radius: 7px; padding: 4px; min-height: 25px; font-weight: 600; selection-background-color: {t.accent}; selection-color: {t.on_accent}; }}
    QSpinBox:focus {{ border-color: {t.accent}; }}
    QScrollArea, QScrollArea > QWidget > QWidget {{ background: transparent; border: none; }}
    QScrollBar:vertical {{ background: transparent; width: 8px; margin: 1px; }}
    QScrollBar::handle:vertical {{ background: {t.border}; border-radius: 3px; min-height: 32px; }}
    QScrollBar::handle:vertical:hover {{ background: {t.muted}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}
    QTableWidget {{ background: {t.surface}; alternate-background-color: {t.background}; border: 1px solid {t.border}; border-radius: 12px; gridline-color: {t.border}; selection-background-color: {t.raised}; selection-color: {t.text}; }}
    QHeaderView::section {{ background: {t.raised}; color: {t.muted}; padding: 12px; border: none; font-weight: 600; }}
    QProgressBar {{ background: {t.raised}; border: none; border-radius: 4px; height: 8px; color: transparent; }}
    QProgressBar::chunk {{ background: {t.accent}; border-radius: 4px; }}
    QToolTip {{ background: {t.raised}; color: {t.text}; border: 1px solid {t.border}; padding: 8px; }}
    """
