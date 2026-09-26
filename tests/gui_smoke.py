"""Run with QT_QPA_PLATFORM=offscreen, exercises real Qt widgets."""

import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QSettings
from PySide6.QtTest import QTest
from bdo_sim.catalog import load_catalog
from bdo_sim.storage import History
from bdo_sim.ui.window import Window

app = QApplication([])
app.setStyle("Fusion")
# Qt's offscreen Windows backend does not enumerate installed system fonts.
if app.platformName() == "offscreen":
    for font in ("segoeui.ttf", "segoeuib.ttf"):
        QFontDatabase.addApplicationFont("C:/Windows/Fonts/" + font)
output = Path(".test-output")
output.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as folder:
    settings = QSettings(str(Path(folder) / "settings.ini"), QSettings.Format.IniFormat)
    settings.setValue("language", "ru")
    settings.setValue("theme", "midnight")
    window = Window(load_catalog(), History(Path(folder) / "history.sqlite3"), settings)
    window.show()
    app.processEvents()
    QTest.qWait(260)
    window.grab().save(str(output / "catalog.png"))
    window.search.setText("несуществующий сундук")
    assert window.empty_search.isVisible()
    window.search.clear()
    keys = list(window.spins)
    window.spins[keys[0]].setValue(5)
    window.spins[keys[5]].setValue(10)
    assert window.start_button.isEnabled()
    window.start()
    window.timer.stop()
    app.processEvents()
    assert window.current_opening is not None
    window.reel.progress = 1
    window.reel.update()
    app.processEvents()
    QTest.qWait(260)
    window.grab().save(str(output / "opening.png"))
    window.skip()
    for _ in range(10000):
        window.tick()
        if window.pages.currentIndex() == 2:
            break
    assert window.report.status == "complete"
    assert window.saved
    assert window.table.rowCount() > 0
    export_path = Path(folder) / "report.csv"
    with patch("bdo_sim.ui.window.QFileDialog.getSaveFileName", return_value=(str(export_path), "CSV (*.csv)")):
        window.export()
    assert "Эквивалент в кронах" in export_path.read_text(encoding="utf-8-sig")
    app.processEvents()
    QTest.qWait(260)
    window.grab().save(str(output / "report.png"))
    window.show_global()
    assert window.history.totals()[0] == 1
    window.table_mode.setCurrentIndex(1)
    assert window.table.rowCount() == len(window.report.opened)
    window.back()
    window.theme.setCurrentData("daylight")
    app.processEvents()
    QTest.qWait(260)
    window.grab().save(str(output / "light.png"))
    window.start()
    window.cancel()
    assert window.report.status == "cancelled"
    assert window.history.totals()[0] == 2
    window.clear_basket()
    terminal_chest = "limit_break_chest"
    window.spins[terminal_chest].setValue(1)
    window.start()
    window.timer.stop()
    assert window.report.status == "complete"
    assert window.pages.currentIndex() == 1  # Still displaying the final roll.
    window.animation_started = time.perf_counter() - 3
    window.tick()
    assert window.pages.currentIndex() == 2
    assert window.history.totals()[0] == 3
    window.theme.setCurrentData("midnight")
    window.close()
print("GUI smoke passed: basket, search, animation, skip, report, CSV, history, themes, cancel, final roll")
