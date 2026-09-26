"""Reusable animated controls with predictable mouse and keyboard behavior."""

from PySide6.QtCore import (
    Qt,
    QSize,
    QRectF,
    QPoint,
    QPointF,
    QEvent,
    QVariantAnimation,
    QEasingCurve,
    Signal,
    QPropertyAnimation,
)
from PySide6.QtGui import QColor, QPainter, QPen, QPainterPath, QWheelEvent
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QFrame,
    QSpinBox,
    QAbstractSpinBox,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QGraphicsOpacityEffect,
    QAbstractItemView,
    QAbstractScrollArea,
)
from .theme import THEMES, palette
from .icons import icon


def mix(a, b, amount):
    a, b = QColor(a), QColor(b)
    return QColor.fromRgbF(*(x + (y - x) * amount for x, y in zip(a.getRgbF(), b.getRgbF())))


class ActionButton(QPushButton):
    def __init__(self, text="", action=None, *, symbol=None, primary=False, compact=False):
        super().__init__(text)
        self.symbol, self.primary, self.compact = symbol, primary, compact
        self.colors = THEMES["midnight"]
        self.hover = 0.0
        self.ripple = 1.0
        self.hover_animation = QVariantAnimation(self)
        self.hover_animation.setDuration(150)
        self.hover_animation.valueChanged.connect(self._hover_value)
        self.click_animation = QVariantAnimation(self)
        self.click_animation.setDuration(330)
        self.click_animation.valueChanged.connect(self._click_value)
        self.pressed.connect(self._pressed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(36 if compact else 44)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        if action:
            self.clicked.connect(action)

    def set_theme(self, colors):
        self.colors = colors
        self.update()

    def sizeHint(self):
        return QSize(
            self.fontMetrics().horizontalAdvance(self.text())
            + (30 if self.symbol else 0)
            + (20 if self.compact else 34),
            36 if self.compact else 44,
        )

    def _hover_value(self, value):
        self.hover = value
        self.update()

    def _click_value(self, value):
        self.ripple = value
        self.update()

    def _pressed(self):
        self.click_animation.stop()
        self.click_animation.setStartValue(0.0)
        self.click_animation.setEndValue(1.0)
        self.click_animation.start()

    def enterEvent(self, event):
        self._animate_hover(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_hover(0.0)
        super().leaveEvent(event)

    def _animate_hover(self, target):
        self.hover_animation.stop()
        self.hover_animation.setStartValue(self.hover)
        self.hover_animation.setEndValue(target)
        self.hover_animation.start()

    def paintEvent(self, event):
        t = self.colors
        active = self.isEnabled()
        background = t.accent if self.primary and active else t.raised if active else t.surface
        foreground = t.on_accent if self.primary and active else t.text if active else t.muted
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bounds = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(bounds, 10, 10)
        painter.fillPath(path, mix(background, t.text, self.hover * 0.08 if active else 0))
        painter.setPen(QPen(QColor(t.accent if self.hasFocus() else t.border), 1.5 if self.hasFocus() else 1))
        if not self.primary or self.hasFocus() or not active:
            painter.drawPath(path)
        if self.ripple < 1 and active:
            painter.save()
            painter.setClipPath(path)
            color = QColor(foreground)
            color.setAlphaF(0.13 * (1 - self.ripple))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            radius = self.width() * self.ripple
            painter.drawEllipse(bounds.center(), radius, radius)
            painter.restore()
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        content_width = text_width + (26 if self.symbol and self.text() else 20 if self.symbol else 0)
        x = max(8, (self.width() - content_width) / 2)
        y = 1 if self.isDown() else 0
        if self.symbol:
            icon(self.symbol, foreground).paint(painter, int(x), self.height() // 2 - 10 + y, 20, 20)
            x += 26
        painter.setPen(QColor(foreground))
        painter.drawText(QRectF(x, y, self.width() - x - 6, self.height()), Qt.AlignmentFlag.AlignVCenter, self.text())


class QuantitySpinBox(QSpinBox):
    """The wheel always belongs to the enclosing scroll area, even when focused."""

    def __init__(self):
        super().__init__()
        self.setRange(0, 100000)
        self.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumWidth(64)
        self.setKeyboardTracking(False)
        self.lineEdit().installEventFilter(self)

    def wheelEvent(self, event):
        parent = self.parentWidget()
        while parent is not None:
            if isinstance(parent, QAbstractScrollArea):
                viewport = parent.viewport()
                position = viewport.mapFromGlobal(event.globalPosition().toPoint())
                forwarded = QWheelEvent(
                    QPointF(position),
                    event.globalPosition(),
                    event.pixelDelta(),
                    event.angleDelta(),
                    event.buttons(),
                    event.modifiers(),
                    event.phase(),
                    event.inverted(),
                )
                QApplication.sendEvent(viewport, forwarded)
                event.accept()
                return
            parent = parent.parentWidget()
        event.ignore()

    def eventFilter(self, watched, event):
        if watched is self.lineEdit() and event.type() == QEvent.Type.Wheel:
            self.wheelEvent(event)
            return True
        return super().eventFilter(watched, event)

    def stepBy(self, steps):
        super().stepBy(steps)
        self.lineEdit().deselect()
        self.lineEdit().setCursorPosition(len(self.lineEdit().text()))


class HoverCard(QFrame):
    def __init__(self, role="card"):
        super().__init__()
        self.setObjectName(role)
        self.colors = THEMES["midnight"]
        self.amount = 0.0
        self.selected = False
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(170)
        self.animation.valueChanged.connect(self._value)

    def _value(self, value):
        self.amount = value
        self.update()

    def set_theme(self, colors):
        self.colors = colors
        self.update()

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def enterEvent(self, event):
        self.animate(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate(0.0)
        super().leaveEvent(event)

    def animate(self, value):
        self.animation.stop()
        self.animation.setStartValue(self.amount)
        self.animation.setEndValue(value)
        self.animation.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        color = mix(self.colors.border, self.colors.accent, 1 if self.selected else self.amount * 0.75)
        painter.setPen(QPen(color, 1.4))
        painter.drawRoundedRect(QRectF(self.rect()).adjusted(1, 1, -1, -1), 17, 17)


class MenuPopup(QFrame):
    """Transparent native window; only the rounded panel paints opaque pixels."""

    def __init__(self, parent):
        super().__init__(
            parent, Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint
        )
        self.colors = THEMES["midnight"]
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(self.colors.surface))
        painter.setPen(QPen(QColor(self.colors.border), 1))
        painter.drawRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), 12, 12)


class SelectMenu(ActionButton):
    """Painted trigger + explicit Qt popup, with no native combo subcontrols."""

    currentIndexChanged = Signal(int)

    def __init__(self, symbol=None):
        super().__init__(symbol=symbol)
        self.entries = []
        self.index = -1
        self.popup = MenuPopup(self)
        self.popup.setObjectName("selectPopup")
        layout = QVBoxLayout(self.popup)
        layout.setContentsMargins(7, 7, 7, 7)
        self.list = QListWidget()
        self.list.setFrameShape(QFrame.Shape.NoFrame)
        self.list.setMouseTracking(True)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.list.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        layout.addWidget(self.list)
        self.list.itemClicked.connect(self._choose)
        self.list.itemActivated.connect(self._choose)
        self.clicked.connect(self.showPopup)
        self.list.installEventFilter(self)
        self.popup_effect = QGraphicsOpacityEffect(self.popup)
        self.popup.setGraphicsEffect(self.popup_effect)
        self.popup_animation = QPropertyAnimation(self.popup_effect, b"opacity", self)
        self.popup_animation.setDuration(130)

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(size.width() + 26)
        return size

    def setItems(self, entries):
        selected = self.currentData()
        self.entries = entries
        self.list.clear()
        for title, key in entries:
            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, key)
            item.setSizeHint(QSize(220, 43))
            self.list.addItem(item)
        self.index = next((i for i, (_, key) in enumerate(entries) if key == selected), 0)
        self._refresh()

    def currentData(self):
        return self.entries[self.index][1] if 0 <= self.index < len(self.entries) else None

    def currentIndex(self):
        return self.index

    def currentText(self):
        return self.entries[self.index][0] if 0 <= self.index < len(self.entries) else ""

    def setCurrentIndex(self, index):
        if 0 <= index < len(self.entries) and index != self.index:
            self.index = index
            self._refresh()
            self.currentIndexChanged.emit(index)

    def setCurrentData(self, data):
        for index, (_, key) in enumerate(self.entries):
            if key == data:
                self.setCurrentIndex(index)
                break

    def _refresh(self):
        self.setText(self.currentText() + "    ")
        self.list.setCurrentRow(self.index)
        self.updateGeometry()
        self.update()

    def _choose(self, item):
        self.setCurrentIndex(self.list.row(item))
        self.popup.hide()
        self.setFocus(Qt.FocusReason.PopupFocusReason)

    def set_theme(self, colors):
        super().set_theme(colors)
        self.popup.colors = colors
        self.popup.setPalette(palette(colors))
        self.popup.setStyleSheet(f"""
            QFrame#selectPopup {{ background: transparent; border: none; }}
            QListWidget {{ background: {colors.surface}; color: {colors.text}; border: none; outline: none; font: 14px 'Segoe UI'; }}
            QListWidget::item {{ padding: 8px 12px; border-radius: 7px; margin: 2px; }}
            QListWidget::item:hover {{ background: {colors.raised}; }}
            QListWidget::item:selected {{ background: {colors.accent}; color: {colors.on_accent}; }}
        """)
        self.popup.update()

    def showPopup(self):
        if self.popup.isVisible():
            self.popup.hide()
            return
        self.list.setCurrentRow(self.index)
        width = max(
            self.width(), max((self.fontMetrics().horizontalAdvance(text) for text, _ in self.entries), default=0) + 54
        )
        height = len(self.entries) * 47 + 16
        screen = self.screen().availableGeometry()
        origin = self.mapToGlobal(QPoint(0, self.height() + 7))
        x = max(screen.left(), min(origin.x(), screen.right() - width))
        y = origin.y() if origin.y() + height <= screen.bottom() else self.mapToGlobal(QPoint(0, 0)).y() - height - 7
        self.popup.setGeometry(x, max(screen.top(), y), width, height)
        self.popup.show()
        self.list.setFocus(Qt.FocusReason.PopupFocusReason)
        self.popup_animation.stop()
        self.popup_animation.setStartValue(0.35)
        self.popup_animation.setEndValue(1.0)
        self.popup_animation.start()

    def eventFilter(self, watched, event):
        from PySide6.QtCore import QEvent

        if watched is self.list and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self.popup.hide()
                self.setFocus()
                return True
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
                if self.list.currentItem():
                    self._choose(self.list.currentItem())
                return True
        return super().eventFilter(watched, event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Down, Qt.Key.Key_Up):
            self.showPopup()
            event.accept()
        else:
            super().keyPressEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        icon("chevron", self.colors.muted, 16).paint(painter, self.width() - 24, self.height() // 2 - 8, 16, 16)


def fade_in(widget, duration=220):
    """Retain the effect and animation to handle rapid page changes safely."""
    if not hasattr(widget, "fade_effect"):
        widget.fade_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(widget.fade_effect)
        widget.fade_animation = QPropertyAnimation(widget.fade_effect, b"opacity", widget)
        widget.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        # Bypass the effect after the transition. Keeping an active parent
        # opacity effect can blank nested effects inside scroll viewports.
        widget.fade_animation.finished.connect(lambda: widget.fade_effect.setEnabled(False))
    widget.fade_animation.stop()
    widget.fade_effect.setEnabled(True)
    widget.fade_animation.setDuration(duration)
    widget.fade_animation.setStartValue(0.25)
    widget.fade_animation.setEndValue(1.0)
    widget.fade_animation.start()
