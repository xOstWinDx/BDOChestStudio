"""UI regressions: wheel routing, editable quantities, popup input and live i18n."""

import csv
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from string import Formatter
from unittest.mock import patch
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import Qt, QPoint, QPointF, QSettings
from PySide6.QtGui import QFontDatabase, QWheelEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QLabel

from bdo_sim.catalog import load_catalog, ASSETS
from bdo_sim.i18n import Translator
from bdo_sim.engine import Simulation
from bdo_sim.storage import History
from bdo_sim.ui.window import Window
from bdo_sim.ui.theme import THEMES


class UiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.app.setStyle("Fusion")
        if cls.app.platformName() == "offscreen":
            for name in ("segoeui.ttf", "segoeuib.ttf"):
                QFontDatabase.addApplicationFont("C:/Windows/Fonts/" + name)
        cls.catalog = load_catalog()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)
        self.settings = QSettings(str(self.path / "settings.ini"), QSettings.Format.IniFormat)
        self.settings.setValue("language", "ru")
        self.window = Window(self.catalog, History(self.path / "history.sqlite3"), self.settings)
        self.window.show()
        QTest.qWait(30)
        self.key = next(iter(self.window.spins))

    def tearDown(self):
        for selector in (self.window.theme, self.window.language, self.window.scope, self.window.table_mode):
            selector.popup.hide()
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()
        self.temp.cleanup()

    def test_reel_selects_rarest_actual_quantity_and_plays_once(self):
        from bdo_sim.domain import Drop
        from bdo_sim.rarity import Rarity

        reel = self.window.reel
        opening = SimpleNamespace(chest_id="sweet_enhancement_chest", drops=(Drop("full_outfit", 30),))
        reel.prepare(opening)
        self.assertEqual(reel.winner.drop.quantity, 30)
        self.assertEqual(reel.winner.rarity, Rarity.MYTHIC)
        with patch.object(reel, "play") as play:
            reel.advance(1.4)
            reel.advance(1.6)
            play.assert_called_once_with("rare")
        self.window.sound_toggle.setChecked(False)
        self.assertFalse(reel.sound_enabled)
        self.assertFalse(self.settings.value("sound_enabled", True, type=bool))

    def test_bonus_canvas_reveals_every_drop_and_resets_for_reel(self):
        from bdo_sim.domain import Drop

        chest = self.catalog["golden_treasure_bundle"]
        drops = chest.open(SimpleNamespace(random=lambda: 0))
        reel = self.window.reel
        self.window.navigate(1)
        reel.prepare(SimpleNamespace(chest_id=chest.id, drops=drops))
        self.app.processEvents()
        self.assertTrue(reel.reveal_mode)
        self.assertEqual([o.drop for o in reel.rewards], list(drops))
        self.assertEqual([o.chance for o in reel.rewards[:2]], [100, 100])
        self.assertGreater(reel.duration, 2.05)
        with patch.object(reel, "play") as play:
            reel.advance(0.1)
            self.assertEqual(reel.revealed_count, 1)
            reel.advance(0.3)
            play.assert_called_once_with("land")
            reel.advance(0.5)
            self.assertEqual(reel.revealed_count, 2)
            reel.advance(0.9)
            self.assertEqual(play.call_args.args, ("rare",))
            reel.advance(reel.duration)
            self.assertEqual(reel.revealed_count, len(drops))
            self.assertEqual(reel.progress, 1)
        self.app.processEvents()
        self.assertGreater(self.window.reel_scroll.verticalScrollBar().maximum(), 0)
        self.assertGreater(self.window.reel_scroll.verticalScrollBar().value(), 0)
        reel.prepare(SimpleNamespace(chest_id="limit_break_chest", drops=(Drop("full_outfit", 50),)))
        self.app.processEvents()
        self.assertFalse(reel.reveal_mode)
        self.assertEqual(reel.duration, 2.05)
        self.assertEqual(self.window.reel_scroll.verticalScrollBar().maximum(), 0)

    def test_global_mute_stops_audio_and_works_on_catalog(self):
        self.assertEqual(self.window.pages.currentIndex(), 0)
        with patch.object(self.window.audio, "stop") as stop:
            self.window.sound_toggle.click()
            stop.assert_called_once()
        self.assertEqual(self.window.sound_toggle.symbol, "muted")
        self.assertFalse(self.window.audio.enabled)
        for sound in self.window.audio.sounds.values():
            with patch.object(sound, "play") as play:
                self.window.audio.play(next(k for k, v in self.window.audio.sounds.items() if v is sound))
                play.assert_not_called()

    def test_system_language_and_saved_override(self):
        self.settings.remove("language")
        self.assertEqual(Translator(self.settings, "ru_RU").language, "ru")
        self.assertEqual(Translator(self.settings, "en_US").language, "en")
        self.assertEqual(Translator(self.settings, "de_DE").language, "en")
        regional_ru_ui_en = SimpleNamespace(uiLanguages=lambda: ["en-GB"], name=lambda: "ru_RU")
        with patch("bdo_sim.i18n.QLocale.system", return_value=regional_ru_ui_en):
            self.assertEqual(Translator(self.settings).language, "en")
        translator = Translator(self.settings, "en_US")
        translator.set_language("ru")
        self.settings.sync()
        reopened = QSettings(str(self.path / "settings.ini"), QSettings.Format.IniFormat)
        self.assertEqual(Translator(reopened, "en_US").language, "ru")

    def test_wheel_scrolls_catalog_and_never_changes_quantity(self):
        spin = self.window.spins[self.key]
        spin.setValue(7)
        for focused in (False, True):
            self.window.catalog_scroll.verticalScrollBar().setValue(0)
            spin.setFocus() if focused else spin.clearFocus()
            position = spin.rect().center()
            event = QWheelEvent(
                QPointF(position),
                QPointF(spin.mapToGlobal(position)),
                QPoint(),
                QPoint(0, -120),
                Qt.MouseButton.NoButton,
                Qt.KeyboardModifier.NoModifier,
                Qt.ScrollPhase.NoScrollPhase,
                False,
            )
            self.app.sendEvent(spin, event)
            self.app.processEvents()
            self.assertEqual(spin.value(), 7)
            self.assertGreater(self.window.catalog_scroll.verticalScrollBar().value(), 0)

    def test_step_buttons_and_manual_entry(self):
        spin = self.window.spins[self.key]
        _, minus, plus = next(row for row in self.window.count_buttons if row[0] == self.key)
        QTest.mouseClick(plus, Qt.MouseButton.LeftButton)
        self.assertEqual(spin.value(), 1)
        self.assertFalse(spin.lineEdit().hasSelectedText())
        QTest.mouseClick(minus, Qt.MouseButton.LeftButton)
        self.assertEqual(spin.value(), 0)
        self.assertFalse(spin.lineEdit().hasSelectedText())
        # Click far to the right in the number field; there is no suffix trap.
        QTest.mouseClick(spin.lineEdit(), Qt.MouseButton.LeftButton, pos=QPoint(spin.lineEdit().width() - 5, 12))
        QTest.keyClick(spin, Qt.Key.Key_A, Qt.KeyboardModifier.ControlModifier)
        QTest.keyClicks(spin, "42")
        QTest.keyClick(spin, Qt.Key.Key_Return)
        self.assertEqual(spin.value(), 42)
        self.assertEqual(spin.suffix(), "")
        self.assertEqual(self.window.basket_rows[self.key][2].value(), 42)
        self.window.basket_rows[self.key][2].setValue(9)
        self.assertEqual(spin.value(), 9)
        QTest.mouseClick(self.window.basket_rows[self.key][3], Qt.MouseButton.LeftButton)
        self.assertEqual(spin.value(), 0)
        self.assertTrue(self.window.basket_rows[self.key][0].isHidden())

    def test_popup_keyboard_mouse_and_escape(self):
        menu = self.window.theme
        QTest.mouseClick(menu, Qt.MouseButton.LeftButton)
        QTest.qWait(160)
        self.assertTrue(menu.popup.isVisible())
        QTest.keyClick(menu.list, Qt.Key.Key_Down)
        QTest.keyClick(menu.list, Qt.Key.Key_Return)
        self.assertEqual(menu.currentData(), "ocean")
        self.assertEqual(self.window.theme_id, "ocean")
        self.assertFalse(menu.popup.isVisible())
        menu.showPopup()
        item = menu.list.item(2)
        QTest.mouseClick(menu.list.viewport(), Qt.MouseButton.LeftButton, pos=menu.list.visualItemRect(item).center())
        self.assertEqual(menu.currentData(), "ember")
        menu.showPopup()
        QTest.keyClick(menu.list, Qt.Key.Key_Escape)
        self.assertFalse(menu.popup.isVisible())
        self.assertEqual(menu.currentData(), "ember")

    def test_popup_corners_are_transparent_and_shadow_disabled(self):
        self.window.theme.setCurrentData("daylight")
        for menu in (self.window.theme, self.window.language):
            menu.showPopup()
            QTest.qWait(180)
            image = menu.popup.grab().toImage()
            for x, y in (
                (0, 0),
                (image.width() - 1, 0),
                (0, image.height() - 1),
                (image.width() - 1, image.height() - 1),
            ):
                self.assertEqual(image.pixelColor(x, y).alpha(), 0)
            self.assertEqual(image.pixelColor(image.width() // 2, image.height() // 2).alpha(), 255)
            self.assertTrue(menu.popup.windowFlags() & Qt.WindowType.NoDropShadowWindowHint)
            self.assertTrue(menu.popup.testAttribute(Qt.WidgetAttribute.WA_TranslucentBackground))
            menu.popup.hide()

    def test_guide_and_no_unit_suffixes(self):
        self.assertIn("Black Desert Online", self.window.guide.text())
        self.assertFalse(hasattr(self.window, "step_labels"))
        for lang in ("ru", "en"):
            self.window.language.setCurrentData(lang)
            self.assertFalse(any(widget.text() in ("шт.", "pcs") for widget in self.window.findChildren(QLabel)))

    def test_live_language_preserves_basket_roll_and_report(self):
        w = self.window
        w.spins[self.key].setValue(5)
        w.search.setText("butterfly")
        w.language.setCurrentData("en")
        self.assertEqual(w.spins[self.key].value(), 5)
        self.assertEqual(w.search.text(), "butterfly")
        self.assertEqual(w.card_titles[self.key].text(), "Butterfly Dream Chest")
        self.assertEqual(w.basket_count.text(), "5 chests")
        w.start()
        w.timer.stop()
        report = w.report
        snapshot = (report.total_opened, dict(report.inventory), report.pending)
        w.language.setCurrentData("ru")
        self.assertIs(w.report, report)
        self.assertEqual(snapshot, (report.total_opened, dict(report.inventory), report.pending))
        w.skip()
        while w.pages.currentIndex() != 2:
            w.tick()
        expected = Simulation(self.catalog, report.basket, report.seed)
        while expected.report.status == "running":
            expected.step()
        self.assertEqual(report.inventory, expected.report.inventory)
        w.language.setCurrentData("en")
        self.assertEqual(w.report_title.text(), "Your haul")
        self.assertEqual(w.table.horizontalHeaderItem(0).text(), "Item")
        self.assertEqual(w.history.totals()[0], 1)
        export_path = self.path / "en.csv"
        with patch("bdo_sim.ui.window.QFileDialog.getSaveFileName", return_value=(str(export_path), "")):
            w.export()
        with export_path.open(encoding="utf-8-sig", newline="") as file:
            rows = list(csv.reader(file, delimiter=";"))
        self.assertEqual(rows[0], ["Item", "Quantity", "Cron equivalent"])
        self.assertFalse(any("Крон" in row[0] for row in rows))

    def test_dictionaries_complete_and_placeholders_match(self):
        ru, en = [
            json.loads((ASSETS / "locales" / f"{code}.json").read_text(encoding="utf-8")) for code in ("ru", "en")
        ]
        self.assertEqual(set(ru["ui"]), set(en["ui"]))
        for item in self.catalog.values():
            self.assertTrue(item.name)
            self.assertTrue(item.name_en)

        def fields(text):
            return {name for _, name, _, _ in Formatter().parse(text) if name is not None}

        for key in ru["ui"]:
            self.assertEqual(fields(ru["ui"][key]), fields(en["ui"][key]), key)
        t = self.window.i18n
        self.assertEqual(
            [t.quantity(n) for n in (1, 2, 5, 11, 21, 22, 111)],
            ["1 сундук", "2 сундука", "5 сундуков", "11 сундуков", "21 сундук", "22 сундука", "111 сундуков"],
        )

    def test_report_after_final_reel_needs_no_extra_repaint(self):
        w = self.window
        for theme in ("midnight", "daylight"):
            with self.subTest(theme=theme):
                w.back()
                w.theme.setCurrentData(theme)
                w.clear_basket()
                w.spins["limit_break_chest"].setValue(3)
                w.start()
                w.timer.stop()
                # Exercise moving frames and the automatic final-roll transition,
                # without waiting two seconds for each real-time animation.
                for _ in range(30):
                    if w.pages.currentIndex() == 2:
                        break
                    for elapsed in (0.3, 0.8, 1.4, 2.1):
                        w.animation_started = time.perf_counter() - elapsed
                        w.tick()
                        QTest.qWait(10)
                        if w.pages.currentIndex() == 2:
                            break
                self.assertEqual(w.pages.currentIndex(), 2)
                QTest.qWait(300)
                # Read the actual backing window; QWidget.grab() would itself
                # repaint and hide the very stale-pixel bug being tested.
                origin = w.table.mapTo(w, QPoint(0, 0))
                rect = w.table.rect().translated(origin)
                before = w.screen().grabWindow(w.winId()).toImage().copy(rect)
                if before.isNull():
                    self.skipTest("Platform cannot capture window backing pixels")
                w.repaint()
                w.table.horizontalHeader().viewport().repaint()
                w.table.viewport().repaint()
                QTest.qWait(30)
                after = w.screen().grabWindow(w.winId()).toImage().copy(rect)
                self.assertEqual(before, after, "Report changes after forced repaint")

    def test_theme_text_contrast(self):
        def luminance(hex_color):
            rgb = [int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5)]
            rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
            return sum(c * weight for c, weight in zip(rgb, (0.2126, 0.7152, 0.0722)))

        def contrast(a, b):
            a, b = sorted((luminance(a), luminance(b)))
            return (b + 0.05) / (a + 0.05)

        for name, theme in THEMES.items():
            for background in (theme.background, theme.surface, theme.raised):
                for foreground in (theme.text, theme.muted):
                    self.assertGreaterEqual(contrast(foreground, background), 4.5, (name, foreground, background))
            self.assertGreaterEqual(contrast(theme.on_accent, theme.accent), 4.5, name)


if __name__ == "__main__":
    unittest.main()
