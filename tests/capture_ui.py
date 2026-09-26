"""Visual review at normal/minimum window sizes, with populated basket and menus."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from PySide6.QtCore import QSettings
from PySide6.QtGui import QFontDatabase
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from bdo_sim.catalog import load_catalog
from bdo_sim.storage import History
from bdo_sim.ui.window import Window

app = QApplication([])
app.setStyle("Fusion")
if app.platformName() == "offscreen":
    for name in ("segoeui.ttf", "segoeuib.ttf"):
        QFontDatabase.addApplicationFont("C:/Windows/Fonts/" + name)
out = Path(".test-output")
out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as folder:
    settings = QSettings(str(Path(folder) / "settings.ini"), QSettings.Format.IniFormat)
    settings.setValue("language", "ru")
    window = Window(load_catalog(), History(Path(folder) / "history.sqlite3"), settings)
    window.show()
    keys = list(window.spins)
    for key, qty in zip((keys[0], keys[5], keys[4]), (5, 10, 100000)):
        window.spins[key].setValue(qty)
    QTest.qWait(300)
    for theme_id in ("midnight", "ocean", "ember", "daylight"):
        window.theme.setCurrentData(theme_id)
        QTest.qWait(180)
        window.grab().save(str(out / f"theme-{theme_id}.png"))
    window.theme.setCurrentData("midnight")
    window.grab().save(str(out / "redesign-ru.png"))
    window.theme.showPopup()
    QTest.qWait(200)
    window.theme.popup.grab().save(str(out / "theme-popup.png"))
    window.theme.popup.hide()
    window.language.setCurrentData("en")
    window.theme.setCurrentData("ocean")
    QTest.qWait(300)
    window.grab().save(str(out / "redesign-en.png"))
    window.resize(1080, 760)
    QTest.qWait(200)
    window.grab().save(str(out / "redesign-minimum.png"))
    window.theme.setCurrentData("daylight")
    window.theme.showPopup()
    QTest.qWait(200)
    window.theme.popup.grab().save(str(out / "theme-popup-light.png"))
    window.theme.popup.hide()
    window.close()
print("Captured RU, EN, minimum size, dark/light popup")
