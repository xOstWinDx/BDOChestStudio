"""Rounded, probability-aware reel. Visual and audio effects never use the game RNG."""

import math

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap, QFont, QPainterPath, QLinearGradient, QRadialGradient
from PySide6.QtWidgets import QWidget

from ..catalog import ASSETS
from ..outcomes import outcomes, Outcome
from ..rarity import Rarity
from ..domain import BonusChest
from .audio import Audio


class Reel(QWidget):
    card_revealed = Signal(int)
    mode_changed = Signal(bool)

    def __init__(self, catalog, audio=None):
        super().__init__()
        # Qt propagates the parent background into the rounded corners.
        self.setAutoFillBackground(False)
        self.catalog = catalog
        self.name_for = lambda item: item.name
        self.items = []
        self.progress = self.celebration = 0.0
        self.target = 24
        self.accent, self.surface, self.ink = "#c8b5ff", "#211e2b", "#eee8f7"
        self.audio = audio or Audio(self)
        self.landed = False
        self.last_slot = 0
        self.winner = None
        self.reveal_mode = False
        self.rewards = []
        self.elapsed = 0
        self.revealed_count = 0
        self.duration = 2.05
        self.pixmaps = {item.icon: QPixmap(str(ASSETS / item.icon)) for item in catalog.values()}
        self.setMinimumHeight(280)

    @property
    def sound_enabled(self):
        return self.audio.enabled

    def stop_sounds(self):
        self.audio.stop()

    def play(self, name):
        self.audio.play(name)

    def prepare(self, opening):
        self.stop_sounds()
        chest = self.catalog[opening.chest_id]
        table = [o for o in outcomes(chest) if o.chance > 0]
        self.reveal_mode = isinstance(chest, (BonusChest)) or len(opening.drops) > 1
        available = list(table)
        self.rewards = []
        for drop in opening.drops:
            outcome = next((o for o in available if o.drop == drop), Outcome(drop, 100))
            self.rewards.append(outcome)
            if outcome in available:
                available.remove(outcome)
        self.elapsed = 0
        self.revealed_count = 0
        self.duration = self.reveal_end + 1.2 if self.reveal_mode else 2.05
        self.update_canvas_height()
        self.mode_changed.emit(self.reveal_mode)
        source = table or [Outcome(d, 100) for d in opening.drops]
        self.items = [source[(i + len(opening.chest_id)) % len(source)] for i in range(29)] if source else []
        # Match both identity and quantity; bonus openings can have several rewards.
        winners = [o for o in table if o.drop in opening.drops]
        self.winner = min(winners, key=lambda o: o.chance) if winners else None
        if self.winner and self.items:
            self.items[self.target] = self.winner
        self.progress = self.celebration = 0
        self.last_slot = 0
        self.landed = False
        self.update()

    @property
    def reveal_end(self):
        return max(0, len(self.rewards) - 1) * 0.4 + 0.38

    def columns(self):
        return max(1, (self.width() - 24) // 182)

    def update_canvas_height(self):
        rows = math.ceil(len(self.rewards) / self.columns()) if self.reveal_mode else 0
        self.setMinimumHeight(max(180, rows * 174 + 24) if self.reveal_mode else 280)

    def resizeEvent(self, event):
        self.update_canvas_height()
        super().resizeEvent(event)

    def advance(self, elapsed):
        self.elapsed = max(0, elapsed)
        if self.reveal_mode:
            self.progress = min(1, self.elapsed / self.reveal_end)
            count = min(len(self.rewards), int(self.elapsed / 0.4) + 1)
            if count > self.revealed_count:
                latest = self.rewards[self.revealed_count : count]
                self.play("rare" if any(o.rarity >= Rarity.EPIC for o in latest) else "land")
                self.revealed_count = count
                row = (count - 1) // self.columns()
                self.card_revealed.emit(row * 174 + 100)
            self.update()
            return
        self.progress = min(1, max(0, elapsed / 1.35))
        slot = round(self.target * (1 - (1 - self.progress) ** 4))
        if self.progress >= 1 and not self.landed:
            self.landed = True
            self.play("rare" if self.winner and self.winner.rarity >= Rarity.EPIC else "land")
        elif slot != self.last_slot and not self.landed:
            self.play("tick")
        self.last_slot = slot
        self.celebration = min(1, max(0, (elapsed - 1.35) / 0.7))
        self.update()

    def rarity_color(self, rarity):
        light = QColor(self.surface).lightnessF() > 0.5
        colors = (
            ("#8290a3", "#27834a", "#276ac5", "#987000", "#bd560e", "#ce3448")
            if light
            else ("#8290a3", "#72ca96", "#7cb4ff", "#efcf6a", "#ffac68", "#ff7187")
        )
        return QColor(colors[int(rarity)])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        area = QRectF(1, 1, self.width() - 2, self.height() - 2)
        clip = QPainterPath()
        clip.addRoundedRect(area, 24, 24)
        painter.setClipPath(clip)
        base = QColor(self.surface)
        background = base.lighter(112) if base.lightnessF() < 0.5 else base.darker(104)
        painter.fillRect(area, background)
        if self.reveal_mode:
            self.paint_rewards(painter)
            painter.end()
            return
        height = self.height()
        center, top = self.width() / 2, (height - 204) / 2
        offset = self.target * 176 * (1 - (1 - self.progress) ** 4)
        if self.winner and self.progress >= 1:
            glow = QRadialGradient(center, height / 2, 190)
            color = self.rarity_color(self.winner.rarity)
            color.setAlphaF(0.20 * (1 - self.celebration * 0.5))
            glow.setColorAt(0, color)
            color.setAlpha(0)
            glow.setColorAt(1, color)
            painter.fillRect(area, glow)
            if self.winner.rarity >= Rarity.EPIC:
                for i in range(22):
                    angle = i * math.tau / 22
                    radius = 75 + self.celebration * (80 + i % 4 * 16)
                    color = self.rarity_color(self.winner.rarity) if i % 2 else QColor(self.accent)
                    color.setAlphaF((1 - self.celebration) * 0.65)
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(color)
                    x = center + math.cos(angle) * radius
                    y = height / 2 + math.sin(angle) * radius * 0.65
                    painter.drawEllipse(QRectF(x, y, 3 + i % 3, 3 + i % 3))
        for index, outcome in enumerate(self.items):
            x = center - 80 + index * 176 - offset
            if x < -170 or x > self.width():
                continue
            item = self.catalog[outcome.drop.item_id]
            selected = abs(x + 80 - center) < 80
            rect = QRectF(x, top, 160, 204)
            color = self.rarity_color(outcome.rarity)
            painter.setBrush(base)
            painter.setPen(QPen(color, 2.5 if selected else 1.3))
            painter.drawRoundedRect(rect, 18, 18)
            pixmap = self.pixmaps[item.icon].scaled(
                100, 86, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(int(x + 80 - pixmap.width() / 2), int(top + 57 - pixmap.height() / 2), pixmap)
            painter.setPen(QColor(self.ink))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(
                QRectF(x + 10, top + 108, 140, 60),
                Qt.AlignmentFlag.AlignHCenter | Qt.TextFlag.TextWordWrap,
                self.name_for(item),
            )
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
            painter.setPen(color)
            painter.drawText(
                QRectF(x + 10, top + 177, 140, 22),
                Qt.AlignmentFlag.AlignCenter,
                f"×{outcome.drop.quantity:,}  ·  {outcome.chance:.3g}%",
            )
        # Feather the moving strip into the rounded container edges.
        for left in (True, False):
            start, end = (0, 65) if left else (self.width(), self.width() - 65)
            fade = QLinearGradient(start, 0, end, 0)
            fade.setColorAt(0, background)
            clear = QColor(background)
            clear.setAlpha(0)
            fade.setColorAt(1, clear)
            painter.fillRect(QRectF(min(start, end), 0, 65, height), fade)
        painter.setPen(QPen(QColor(self.accent), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(int(center), int(top - 20), int(center), int(top - 6))
        painter.drawLine(int(center), int(top + 211), int(center), int(top + 225))
        painter.end()

    def paint_rewards(self, painter):
        columns = self.columns()
        width = min(200, (self.width() - 24) / columns - 12)
        left = (self.width() - columns * (width + 12) + 12) / 2
        for index, outcome in enumerate(self.rewards):
            age = self.elapsed - index * 0.4
            if age <= 0:
                continue
            progress = min(1, age / 0.38)
            eased = 1 - (1 - progress) ** 3
            row, column = divmod(index, columns)
            rect = QRectF(left + column * (width + 12), 12 + row * 174 + (1 - eased) * 20, width, 160)
            painter.save()
            painter.setOpacity(eased)
            color = self.rarity_color(outcome.rarity)
            if outcome.rarity >= Rarity.EPIC and age < 1.1:
                glow = QRadialGradient(rect.center(), width * 0.7)
                glow_color = QColor(color)
                glow_color.setAlphaF(0.28 * (1 - age / 1.1))
                glow.setColorAt(0, glow_color)
                glow_color.setAlpha(0)
                glow.setColorAt(1, glow_color)
                painter.fillRect(rect.adjusted(-12, -12, 12, 12), glow)
            painter.setPen(QPen(color, 1.6))
            painter.setBrush(QColor(self.surface))
            painter.drawRoundedRect(rect, 15, 15)
            item = self.catalog[outcome.drop.item_id]
            pixmap = self.pixmaps[item.icon].scaled(
                68, 58, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(int(rect.center().x() - pixmap.width() / 2), int(rect.top() + 10), pixmap)
            painter.setPen(QColor(self.ink))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(
                QRectF(rect.x() + 8, rect.y() + 74, width - 16, 57),
                Qt.AlignmentFlag.AlignHCenter | Qt.TextFlag.TextWordWrap,
                self.name_for(item),
            )
            painter.setPen(color)
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
            painter.drawText(
                QRectF(rect.x() + 8, rect.y() + 134, width - 16, 20),
                Qt.AlignmentFlag.AlignCenter,
                f"×{outcome.drop.quantity:,}  ·  {outcome.chance:.3g}%",
            )
            painter.restore()

    def hideEvent(self, event):
        self.stop_sounds()
        super().hideEvent(event)
