from __future__ import annotations

import csv
import secrets
import sqlite3
import time

from PySide6.QtCore import Qt, QTimer, QSettings
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QScrollArea,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..catalog import ASSETS
from ..domain import WeightedChest, BonusChest
from ..engine import Simulation
from ..outcomes import sorted_chests
from ..i18n import Translator
from .icons import icon
from .reel import Reel
from .audio import Audio
from .theme import THEMES, LEGACY_THEMES, stylesheet, palette
from .widgets import ActionButton, HoverCard, QuantitySpinBox, SelectMenu, fade_in


def label(text="", role=None):
    widget = QLabel(text)
    widget.setTextFormat(Qt.TextFormat.PlainText)
    widget.setWordWrap(True)
    if role:
        widget.setObjectName(role)
    return widget


def panel(role="card"):
    widget = HoverCard() if role == "card" else QFrame()
    widget.setObjectName(role)
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(20, 18, 20, 18)
    layout.setSpacing(12)
    return widget, layout


def artwork(item, width, height):
    widget = QLabel()
    widget.setFixedSize(width, height)
    widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap(str(ASSETS / item.icon))
    pixmap = pixmap.scaled(
        width * 2, height * 2, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
    )
    pixmap.setDevicePixelRatio(2)
    widget.setPixmap(pixmap)
    return widget


class Window(QMainWindow):
    def __init__(self, catalog, history, settings=None, translator=None):
        super().__init__()
        self.catalog, self.history = catalog, history
        self.simulation = self.report = self.current_opening = None
        self.fast = self.saved = False
        self.settings = settings if settings is not None else QSettings("PetProjects", "BDOChestStudio")
        self.audio = Audio(self, self.settings.value("sound_enabled", True, type=bool))
        self.i18n = translator or Translator(self.settings)
        self.t = self.i18n.text
        self.bindings = []
        self.cards, self.spins, self.basket_rows = [], {}, {}
        self.card_titles, self.card_modes = {}, {}
        self.count_buttons = []
        self.last_basket = {}
        self.theme_id = self.settings.value("theme", "midnight")
        self.theme_id = LEGACY_THEMES.get(self.theme_id, self.theme_id)
        if self.theme_id not in THEMES:
            self.theme_id = "midnight"
        self.setWindowIcon(QIcon(str(ASSETS / "icons/butterfly.svg")))
        self.resize(1320, 900)
        self.setMinimumSize(1080, 760)
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 20, 28, 22)
        layout.setSpacing(16)
        top = QHBoxLayout()
        brand = label("BDO  /  CHEST STUDIO", "cardTitle")
        brand.setWordWrap(False)
        top.addWidget(brand)
        top.addStretch()
        self.sound_toggle = ActionButton(symbol="sound")
        self.sound_toggle.setFixedWidth(44)
        self.sound_toggle.setCheckable(True)
        self.sound_toggle.setChecked(self.audio.enabled)
        self.sound_toggle.toggled.connect(self.set_sound_enabled)
        top.addWidget(self.sound_toggle)
        self.language = SelectMenu("globe")
        self.theme = SelectMenu("palette")
        top.addWidget(self.language)
        top.addWidget(self.theme)
        layout.addLayout(top)
        self.guide = self.tr_label("program_guide", "subtitle")
        self.guide.setContentsMargins(0, 4, 0, 6)
        layout.addWidget(self.guide)
        self.pages = QStackedWidget()
        layout.addWidget(self.pages, 1)
        self.make_catalog()
        self.make_opening()
        self.make_report()
        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self.tick)
        self.retranslate()
        self.theme.currentIndexChanged.connect(lambda _: self.apply_theme(self.theme.currentData()))
        self.language.currentIndexChanged.connect(lambda _: self.i18n.set_language(self.language.currentData()))
        self.i18n.changed.connect(self.retranslate)
        self.apply_theme(self.theme_id)

    def tr_label(self, key, role=None):
        widget = label(self.t(key), role)
        self.bindings.append((widget.setText, key))
        return widget

    def tr_button(self, key, action, symbol=None, primary=False):
        widget = ActionButton(self.t(key), action, symbol=symbol, primary=primary)
        self.bindings.append((widget.setText, key))
        return widget

    def warn(self, key, message):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle(self.t(key))
        box.setText(message)
        box.addButton(self.t("dialog_ok"), QMessageBox.ButtonRole.AcceptRole)
        box.exec()

    def retranslate(self):
        for setter, key in self.bindings:
            setter(self.t(key))
        self.setWindowTitle(self.t("app_title"))
        self.language.blockSignals(True)
        self.language.setItems([(self.t("language_ru"), "ru"), (self.t("language_en"), "en")])
        self.language.setCurrentData(self.i18n.language)
        self.language.blockSignals(False)
        self.language.setAccessibleName(self.t("language_label"))
        self.language.setToolTip(self.t("language_label"))
        self.theme.blockSignals(True)
        self.theme.setItems([(self.t("theme_" + key), key) for key in THEMES])
        self.theme.setCurrentData(self.theme_id)
        self.theme.blockSignals(False)
        self.theme.setAccessibleName(self.t("theme_label"))
        self.theme.setToolTip(self.t("theme_label"))
        self.search.setPlaceholderText(self.t("search"))
        self.search.setAccessibleName(self.t("search"))
        self.search_clear.setToolTip(self.t("search_clear"))
        self.scope.setItems([(self.t("scope_session"), "session"), (self.t("scope_global"), "global")])
        self.table_mode.setItems([(self.t("table_items"), "items"), (self.t("table_chests"), "chests")])
        self.scope.setAccessibleName(self.t("scope_session"))
        self.table_mode.setAccessibleName(self.t("table_items"))
        self.table.setHorizontalHeaderLabels([self.t(k) for k in ("column_item", "column_quantity", "column_crowns")])
        for item, _ in self.cards:
            name = self.i18n.item_name(item)
            self.card_titles[item.id].setText(name)
            mode = (
                "weighted" if isinstance(item, WeightedChest) else "bonus" if isinstance(item, BonusChest) else "chain"
            )
            self.card_modes[item.id].setText(self.t("mode_" + mode))
            self.spins[item.id].setAccessibleName(self.t("quantity", name=name))
            row, title, spin, remove = self.basket_rows[item.id]
            title.setText(name)
            title.setMinimumHeight(max(42, title.heightForWidth(155)))
            spin.setAccessibleName(self.t("quantity", name=name))
            remove.setAccessibleName(self.t("basket_remove", name=name))
            remove.setToolTip(self.t("basket_remove", name=name))
        for key, minus, plus in self.count_buttons:
            name = self.i18n.item_name(self.catalog[key])
            minus.setAccessibleName(self.t("quantity_less", name=name))
            plus.setAccessibleName(self.t("quantity_more", name=name))
        self.catalog_count.setText(self.t("catalog_count", n=len(self.cards)))
        self.update_basket(animate=False)
        self.filter_catalog(self.search.text())
        self.reel.name_for = self.i18n.item_name
        self.refresh_sound_button()
        self.reel.update()
        if self.pages.currentIndex() == 1:
            self.update_opening_text()
        elif self.pages.currentIndex() == 2:
            self.show_report(self.scope.currentData() == "global", transition=False)

    def apply_theme(self, key):
        if key not in THEMES:
            return
        self.theme_id = key
        colors = THEMES[key]
        QApplication.instance().setPalette(palette(colors))
        self.setPalette(palette(colors))
        self.setStyleSheet(stylesheet(colors))
        for widget in self.findChildren(ActionButton) + self.findChildren(HoverCard):
            widget.set_theme(colors)
        self.search_icon.setIcon(icon("search", colors.muted))
        self.search_clear.setIcon(icon("close", colors.muted))
        self.basket_icon.setPixmap(icon("basket", colors.accent, 26).pixmap(26, 26))
        self.empty_icon.setPixmap(icon("basket", colors.muted, 44).pixmap(44, 44))
        self.reel.surface, self.reel.ink, self.reel.accent = colors.surface, colors.text, colors.accent
        self.reel.update()
        self.settings.setValue("theme", key)

    def page(self):
        widget = QWidget()
        widget.setObjectName("page")
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        self.pages.addWidget(widget)
        return layout

    def navigate(self, index, animate=True):
        changed = self.pages.currentIndex() != index
        self.pages.setCurrentIndex(index)
        if changed:
            # Keep the stack opaque. An opacity effect on the whole stack
            # caches the outgoing reel together with QAbstractScrollArea's
            # independently painted header/viewport, leaving stale pixels.
            self.pages.update()
            if animate:
                title = self.pages.currentWidget().findChild(QLabel, "title")
                if title is not None:
                    fade_in(title)

    def counter(self, key, *, basket=False):
        frame = QFrame()
        frame.setObjectName("counter")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        spin = QuantitySpinBox()
        frame.setFocusProxy(spin)
        frame.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        minus = ActionButton(action=spin.stepDown, symbol="minus", compact=True)
        plus = ActionButton(action=spin.stepUp, symbol="plus", compact=True)
        minus.setFixedSize(34, 36)
        plus.setFixedSize(34, 36)
        layout.addWidget(minus)
        layout.addWidget(spin, 1)
        layout.addWidget(plus)
        self.count_buttons.append((key, minus, plus))
        if basket:
            spin.valueChanged.connect(lambda value: self.spins[key].setValue(value))
        else:
            spin.valueChanged.connect(self.update_basket)
        return frame, spin

    def make_catalog(self):
        layout = self.page()
        hero, content = panel("hero")
        self.hero_eyebrow = self.tr_label("hero_eyebrow", "eyebrow")
        content.addWidget(self.hero_eyebrow)
        content.addWidget(self.tr_label("hero_title", "title"))
        self.hero_description = self.tr_label("hero_description", "subtitle")
        content.addWidget(self.hero_description)
        layout.addWidget(hero)
        body = QHBoxLayout()
        body.setSpacing(20)
        left = QVBoxLayout()
        left.setSpacing(12)
        search_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search_icon = self.search.addAction(QIcon(), QLineEdit.ActionPosition.LeadingPosition)
        self.search_icon.setEnabled(False)
        self.search_clear = self.search.addAction(QIcon(), QLineEdit.ActionPosition.TrailingPosition)
        self.search_clear.triggered.connect(self.search.clear)
        self.search.textChanged.connect(self.filter_catalog)
        search_row.addWidget(self.search)
        left.addLayout(search_row)
        self.catalog_count = label("", "subtitle")
        left.addWidget(self.catalog_count)
        self.catalog_scroll = QScrollArea()
        self.catalog_scroll.setWidgetResizable(True)
        self.catalog_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.grid.setContentsMargins(1, 1, 10, 1)
        self.grid.setSpacing(14)
        self.catalog_scroll.setWidget(container)
        left.addWidget(self.catalog_scroll, 1)
        self.empty_search = self.tr_label("search_empty", "subtitle")
        left.addWidget(self.empty_search)
        body.addLayout(left, 1)
        sidebar, side = panel("sidebar")
        sidebar.setFixedWidth(330)
        heading = QHBoxLayout()
        self.basket_icon = QLabel()
        self.basket_icon.setFixedSize(28, 28)
        heading.addWidget(self.basket_icon)
        heading.addWidget(self.tr_label("basket_title", "cardTitle"))
        heading.addStretch()
        self.clear_button = self.tr_button("basket_clear", self.clear_basket, "trash")
        heading.addWidget(self.clear_button)
        side.addLayout(heading)
        self.basket_count = label("", "metric")
        side.addWidget(self.basket_count)
        self.basket_types = label("", "subtitle")
        side.addWidget(self.basket_types)
        self.basket_scroll = QScrollArea()
        self.basket_scroll.setWidgetResizable(True)
        self.basket_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        basket_container = QWidget()
        self.basket_layout = QVBoxLayout(basket_container)
        self.basket_layout.setContentsMargins(1, 6, 9, 6)
        self.basket_layout.setSpacing(10)
        self.basket_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.basket_empty = QWidget()
        empty_layout = QVBoxLayout(self.basket_empty)
        empty_layout.setContentsMargins(14, 28, 14, 28)
        empty_layout.setSpacing(15)
        self.empty_icon = QLabel()
        self.empty_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(self.empty_icon)
        for key, role in (("basket_empty", "cardTitle"), ("basket_empty_hint", "subtitle")):
            text = self.tr_label(key, role)
            text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(text)
        self.basket_layout.addWidget(self.basket_empty)
        self.basket_scroll.setWidget(basket_container)
        side.addWidget(self.basket_scroll, 1)
        self.basket_hint = self.tr_label("basket_auto", "subtitle")
        side.addWidget(self.basket_hint)
        self.start_button = self.tr_button("basket_open", self.start, "arrow", True)
        side.addWidget(self.start_button)
        side.addWidget(self.tr_button("history", self.show_global, "history"))
        side.addWidget(self.tr_label("footer", "eyebrow"))
        body.addWidget(sidebar)
        layout.addLayout(body, 1)
        for item in sorted_chests(self.catalog):
            card, content = panel()
            card.setMinimumWidth(230)
            art = artwork(item, 118, 90)
            content.addWidget(art, alignment=Qt.AlignmentFlag.AlignCenter)
            title = label("", "cardTitle")
            title.setMinimumHeight(44)
            content.addWidget(title)
            mode = label("", "subtitle")
            content.addWidget(mode)
            counter, spin = self.counter(item.id)
            content.addWidget(counter)
            self.spins[item.id] = spin
            self.cards.append((item, card))
            self.card_titles[item.id], self.card_modes[item.id] = title, mode
            self.make_basket_row(item)

    def make_basket_row(self, item):
        row = QFrame()
        row.setObjectName("basketRow")
        layout = QVBoxLayout(row)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        top = QHBoxLayout()
        top.setSpacing(10)
        top.addWidget(artwork(item, 42, 42))
        title = label()
        top.addWidget(title, 1)
        remove = ActionButton(action=lambda: self.spins[item.id].setValue(0), symbol="close", compact=True)
        remove.setFixedSize(30, 36)
        top.addWidget(remove)
        layout.addLayout(top)
        counter, spin = self.counter(item.id, basket=True)
        layout.addWidget(counter)
        self.basket_rows[item.id] = (row, title, spin, remove)
        self.basket_layout.addWidget(row)
        row.hide()

    def filter_catalog(self, query):
        query = query.casefold().replace("ё", "е").strip()
        self.search_clear.setVisible(bool(query))
        if not self.cards:
            return
        for _, card in self.cards:
            self.grid.removeWidget(card)
            card.hide()

        def matches(item):
            # Both names remain searchable when the interface language changes.
            names = (item.name, getattr(item, "name_en", item.name))
            return any(query in name.casefold().replace("ё", "е") for name in names)

        visible = [(item, card) for item, card in self.cards if matches(item)]
        for index, (_, card) in enumerate(visible):
            self.grid.addWidget(card, index // 2, index % 2)
            card.show()
        self.empty_search.setVisible(not visible)

    def update_basket(self, *_args, animate=True):
        basket = {key: spin.value() for key, spin in self.spins.items() if spin.value()}
        count = sum(basket.values())
        self.basket_count.setText(self.i18n.quantity(count))
        self.basket_types.setText(self.t("basket_types", n=len(basket)))
        self.basket_empty.setVisible(not basket)
        self.clear_button.setEnabled(bool(basket))
        self.start_button.setEnabled(0 < count <= 1000000)
        self.basket_hint.setText(self.t("basket_limit" if count > 1000000 else "basket_auto"))
        for item, card in self.cards:
            qty = basket.get(item.id, 0)
            card.set_selected(qty > 0)
            row, _, spin, _ = self.basket_rows[item.id]
            row.setVisible(qty > 0)
            spin.blockSignals(True)
            if spin.value() != qty:
                spin.setValue(qty)
            spin.blockSignals(False)
            if animate and qty and item.id not in self.last_basket:
                fade_in(row, 180)
        self.last_basket = basket

    def clear_basket(self):
        for spin in self.spins.values():
            spin.blockSignals(True)
            spin.setValue(0)
            spin.blockSignals(False)
        self.update_basket()

    def make_opening(self):
        layout = self.page()
        layout.addWidget(self.tr_label("opening_title", "title"))
        layout.addWidget(self.tr_label("opening_description", "subtitle"))
        hero, content = panel("hero")
        self.opening_title = label("", "badge")
        content.addWidget(self.opening_title)
        self.reel = Reel(self.catalog, self.audio)
        self.reel_scroll = QScrollArea()
        self.reel_scroll.setWidgetResizable(True)
        self.reel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.reel_scroll.setMinimumHeight(280)
        self.reel_scroll.setMaximumHeight(300)
        self.reel_scroll.setWidget(self.reel)
        self.reel.mode_changed.connect(lambda reveal: self.reel_scroll.setMinimumHeight(180 if reveal else 280))
        self.reel.card_revealed.connect(lambda y: self.reel_scroll.ensureVisible(0, y, 0, 75))
        content.addWidget(self.reel_scroll, 1)
        drop_scroll = QScrollArea()
        drop_scroll.setWidgetResizable(True)
        drop_scroll.setMinimumHeight(44)
        drop_scroll.setMaximumHeight(80)
        self.drop_text = label("", "subtitle")
        self.drop_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.drop_text.setContentsMargins(8, 8, 8, 8)
        drop_scroll.setWidget(self.drop_text)
        content.addWidget(drop_scroll)
        layout.addWidget(hero)
        self.progress_text = label("", "metric")
        layout.addWidget(self.progress_text)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        layout.addWidget(self.progress)
        layout.addWidget(self.tr_label("opening_queue", "subtitle"))
        layout.addStretch()
        actions = QHBoxLayout()
        self.skip_button = self.tr_button("opening_skip", self.skip, "skip", True)
        actions.addWidget(self.skip_button)
        actions.addWidget(self.tr_button("opening_stop", self.cancel, "stop"))
        actions.addStretch()
        layout.addLayout(actions)

    def set_sound_enabled(self, enabled):
        self.settings.setValue("sound_enabled", enabled)
        self.audio.set_enabled(enabled)
        self.refresh_sound_button()

    def refresh_sound_button(self):
        self.sound_toggle.symbol = "sound" if self.audio.enabled else "muted"
        text = self.t("sound_disable" if self.audio.enabled else "sound_enable")
        self.sound_toggle.setToolTip(text)
        self.sound_toggle.setAccessibleName(text)
        self.sound_toggle.update()

    def start(self):
        for spin in self.spins.values():
            spin.interpretText()
        basket = {k: spin.value() for k, spin in self.spins.items() if spin.value()}
        try:
            self.simulation = Simulation(self.catalog, basket, secrets.randbits(63))
        except ValueError:
            self.warn("error_basket", self.t("error_basket_detail"))
            return
        self.report = self.simulation.report
        self.fast = self.saved = False
        self.current_opening = None
        self.animated = 0
        self.skip_button.setEnabled(True)
        self.navigate(1)
        self.timer.start()
        self.tick()

    def skip(self):
        self.reel.stop_sounds()
        self.fast = True
        self.skip_button.setEnabled(False)
        self.current_opening = None

    def update_opening_text(self):
        if not self.report:
            return
        if self.fast:
            self.opening_title.setText(self.t("opening_fast"))
            self.drop_text.setText(self.t("opening_collecting"))
        elif self.current_opening:
            opening = self.current_opening
            self.opening_title.setText(self.i18n.item_name(self.catalog[opening.chest_id]))
            if self.reel.progress >= 1:
                self.drop_text.setText(
                    "  •  ".join(
                        f"{self.i18n.item_name(self.catalog[d.item_id])} ×{self.i18n.number(d.quantity)}"
                        for d in opening.drops
                    )
                    or self.t("opening_no_bonus")
                )
            else:
                self.drop_text.setText(self.t("opening_spinning"))
        self.progress_text.setText(
            self.t(
                "opening_progress",
                opened=self.i18n.number(self.report.total_opened),
                pending=self.i18n.number(self.report.pending),
            )
        )

    def tick(self):
        report = self.report
        if self.fast:
            deadline = time.perf_counter() + 0.008
            while report.status == "running" and time.perf_counter() < deadline:
                self.simulation.step()
        elif self.current_opening is not None:
            elapsed = time.perf_counter() - self.animation_started
            self.reel.advance(elapsed)
            self.update_opening_text()
            if elapsed < self.reel.duration:
                return
            self.current_opening = None
        if not self.fast and report.status == "running" and self.current_opening is None:
            if self.animated >= 12:
                self.skip()
            else:
                opening = self.simulation.step()
                if opening:
                    self.current_opening = opening
                    self.animated += 1
                    self.animation_started = time.perf_counter()
                    self.reel.prepare(opening)
                    self.reel_scroll.verticalScrollBar().setValue(0)
        self.update_opening_text()
        if report.status != "running" and self.current_opening is None:
            self.finish()

    def cancel(self):
        self.simulation.cancel()
        self.current_opening = None
        self.finish()

    def finish(self):
        self.reel.stop_sounds()
        self.timer.stop()
        if not self.saved:
            try:
                self.history.save(self.report)
                self.saved = True
            except (OSError, sqlite3.Error) as exc:
                self.warn("error_save", self.t("error_save_detail", error=exc))
        self.show_report(False)

    def make_report(self):
        layout = self.page()
        self.report_title = label("", "title")
        layout.addWidget(self.report_title)
        self.report_subtitle = label("", "subtitle")
        layout.addWidget(self.report_subtitle)
        metrics = QHBoxLayout()
        self.metrics = []
        for key in ("metric_crowns", "metric_opened", "metric_items"):
            card, content = panel("hero")
            content.addWidget(self.tr_label(key, "eyebrow"))
            value = label("0", "metric")
            content.addWidget(value)
            metrics.addWidget(card)
            self.metrics.append(value)
        layout.addLayout(metrics)
        layout.addWidget(self.tr_label("valuation_hint", "subtitle"))
        controls = QHBoxLayout()
        self.scope = SelectMenu("history")
        self.scope.currentIndexChanged.connect(lambda index: self.show_report(index == 1, transition=False))
        controls.addWidget(self.scope)
        self.table_mode = SelectMenu("box")
        self.table_mode.currentIndexChanged.connect(
            lambda _: self.show_report(self.scope.currentData() == "global", transition=False)
        )
        controls.addWidget(self.table_mode)
        controls.addStretch()
        controls.addWidget(self.tr_button("export", self.export, "download"))
        layout.addLayout(controls)
        self.table = QTableWidget(0, 3)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(True)
        self.table.setShowGrid(False)
        layout.addWidget(self.table, 1)
        self.breakdown = label("", "subtitle")
        layout.addWidget(self.breakdown)
        actions = QHBoxLayout()
        actions.addWidget(self.tr_button("back", self.back, "back", True))
        actions.addStretch()
        layout.addLayout(actions)

    def show_global(self):
        self.show_report(True)

    def show_report(self, global_stats, transition=True):
        if global_stats:
            try:
                runs, inventory, opened = self.history.totals()
            except (OSError, sqlite3.Error, ValueError) as exc:
                self.warn("error_history", str(exc))
                return
            subtitle = self.t("global_details", n=self.i18n.number(runs))
        elif self.report is not None and self.report.status != "running":
            inventory, opened = self.report.inventory, self.report.opened
            subtitle = self.t(
                "session_details",
                status=self.t("status_" + self.report.status),
                pending=self.i18n.number(self.report.pending),
                seed=self.report.seed,
            )
        else:
            inventory, opened = {}, {}
            subtitle = self.t("report_empty")
        self.scope.blockSignals(True)
        self.scope.setCurrentIndex(1 if global_stats else 0)
        self.scope.blockSignals(False)
        self.report_title.setText(self.t("report_global_title" if global_stats else "report_title"))
        self.report_subtitle.setText(subtitle)
        crowns = sum((self.catalog[k].to_crowns(v) or 0) for k, v in inventory.items() if k in self.catalog)
        for widget, value in zip(self.metrics, (crowns, sum(opened.values()), len(inventory))):
            widget.setText(self.i18n.number(value))
        values = opened if self.table_mode.currentData() == "chests" else inventory
        self.export_rows = []
        self.table.setRowCount(len(values))
        for row, (key, qty) in enumerate(sorted(values.items(), key=lambda pair: -pair[1])):
            item = self.catalog.get(key)
            crown = item.to_crowns(qty) if item else None
            name = self.i18n.item_name(item) if item else key
            self.export_rows.append((name, qty, crown if crown is not None else ""))
            for col, value in enumerate(
                (name, self.i18n.number(qty), "—" if crown is None else self.i18n.number(crown))
            ):
                cell = QTableWidgetItem(value)
                if col == 0 and item:
                    cell.setIcon(QIcon(str(ASSETS / item.icon)))
                elif col:
                    cell.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, cell)
            self.table.setRowHeight(row, 48)
        top = sorted(opened.items(), key=lambda pair: -pair[1])[:3]
        summary = " · ".join(
            f"{self.i18n.item_name(self.catalog[k]) if k in self.catalog else k} ×{self.i18n.number(v)}" for k, v in top
        )
        self.breakdown.setText(self.t("top_chests", items=summary) if top else self.t("history_empty"))
        self.navigate(2, transition)

    def export(self):
        path, _ = QFileDialog.getSaveFileName(self, self.t("export_title"), "bdo-report.csv", self.t("csv_filter"))
        if path:
            try:
                with open(path, "w", encoding="utf-8-sig", newline="") as file:
                    writer = csv.writer(file, delimiter=";")
                    writer.writerow([self.t(k) for k in ("column_item", "column_quantity", "column_crowns")])
                    writer.writerows(self.export_rows)
            except OSError as exc:
                self.warn("error_export", str(exc))

    def back(self):
        self.navigate(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "hero_description"):
            self.hero_description.setVisible(self.height() >= 820)
            self.hero_eyebrow.setVisible(self.height() >= 800)

    def closeEvent(self, event):
        if self.timer.isActive():
            self.simulation.cancel()
            self.current_opening = None
            self.finish()
        event.accept()
