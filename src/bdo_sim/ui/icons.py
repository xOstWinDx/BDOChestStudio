"""Small local line icons, independent of platform fonts and emoji support."""

from functools import lru_cache
from PySide6.QtCore import QByteArray, QRectF
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt

PATHS = {
    "sound": '<path d="M3 9h4l5-4v14l-5-4H3Zm13-1a6 6 0 0 1 0 8m3-11a10 10 0 0 1 0 14"/>',
    "muted": '<path d="M3 9h4l5-4v14l-5-4H3Zm13 0 6 6m0-6-6 6"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    "basket": '<path d="m7 9 5-6 5 6M3 9h18l-2 12H5ZM9 13v4m6-4v4"/>',
    "box": '<path d="m3 7 9-4 9 4v11l-9 4-9-4Zm0 0 9 4 9-4M12 11v11M7 5l10 4"/>',
    "history": '<path d="M4 9a9 9 0 1 1 0 7M4 3v6h6m2-3v6l4 2"/>',
    "arrow": '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    "back": '<path d="M20 12H4m6-6-6 6 6 6"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "check": '<path d="m5 12 4 4L19 6"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
    "trash": '<path d="M4 6h16M9 6V3h6v3M6 6l1 15h10l1-15M10 10v7m4-7v7"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
    "palette": '<circle cx="12" cy="12" r="9"/><path d="M12 3v18M12 12h9"/>',
    "spark": '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5ZM20 2v4m-2-2h4"/>',
    "skip": '<path d="m4 5 10 7-10 7Zm13 0v14"/>',
    "stop": '<rect x="5" y="5" width="14" height="14" rx="3"/>',
    "download": '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
    "chart": '<path d="M4 3v18h17M8 16v-4m5 4V7m5 9V4"/>',
    "plus": '<path d="M5 12h14M12 5v14"/>',
    "minus": '<path d="M5 12h14"/>',
}


@lru_cache(maxsize=256)
def icon(name, color, size=20):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{PATHS[name]}</svg>'
    pixmap = QPixmap(size * 2, size * 2)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    QSvgRenderer(QByteArray(svg.encode())).render(painter, QRectF(0, 0, size * 2, size * 2))
    painter.end()
    pixmap.setDevicePixelRatio(2)
    return QIcon(pixmap)
