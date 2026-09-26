"""Capture reproducible README screenshots without touching the user's profile."""

import random
import tempfile
from pathlib import Path
from types import SimpleNamespace

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from bdo_sim.catalog import load_catalog
from bdo_sim.engine import Simulation
from bdo_sim.storage import History
from bdo_sim.ui.window import Window


def main():
    app = QApplication([])
    app.setStyle("Fusion")
    if app.platformName() == "offscreen":
        for name in ("segoeui.ttf", "segoeuib.ttf"):
            QFontDatabase.addApplicationFont("C:/Windows/Fonts/" + name)
    output = Path(__file__).resolve().parents[1] / "docs" / "screenshots"
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as folder:
        settings = QSettings(str(Path(folder) / "settings.ini"), QSettings.Format.IniFormat)
        settings.setValue("language", "ru")
        settings.setValue("theme", "midnight")
        settings.setValue("sound_enabled", False)
        catalog = load_catalog()
        window = Window(catalog, History(Path(folder) / "history.sqlite3"), settings)
        window.resize(1440, 1040)
        window.show()

        def capture(name):
            QTest.qWait(400)
            # Store logical pixels for a compact, DPI-independent README image.
            pixmap = window.grab()
            pixmap.toImage().scaled(
                window.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ).save(str(output / f"{name}.png"))

        basket = {"butterfly_chest": 25, "golden_treasure_chest": 10, "limit_break_chest": 5}
        for key, quantity in basket.items():
            window.spins[key].setValue(quantity)
        capture("catalog")

        window.navigate(1)
        chest = catalog["limit_break_chest"]
        drops = chest.open(random.Random(19))
        window.opening_title.setText(chest.name)
        window.reel.prepare(SimpleNamespace(chest_id=chest.id, drops=drops))
        window.reel.advance(1.55)
        window.drop_text.setText("  •  ".join(f"{catalog[d.item_id].name} ×{d.quantity}" for d in drops))
        window.progress_text.setText(window.t("opening_progress", opened="1", pending="4"))
        window.progress.setRange(0, 100)
        window.progress.setValue(20)
        capture("reel")

        chest = catalog["golden_treasure_bundle"]
        drops = chest.open(random.Random(19))
        window.opening_title.setText(chest.name)
        window.reel.prepare(SimpleNamespace(chest_id=chest.id, drops=drops))
        window.reel.advance(window.reel.duration)
        window.reel_scroll.verticalScrollBar().setValue(0)
        window.drop_text.setText("  •  ".join(f"{catalog[d.item_id].name} ×{d.quantity}" for d in drops))
        capture("rewards")

        simulation = Simulation(catalog, basket, 19)
        while simulation.report.status == "running":
            simulation.step()
        window.report = simulation.report
        window.theme.setCurrentData("daylight")
        window.show_report(False)
        capture("report")
        window.close()
    print(f"Saved four screenshots to {output}")


if __name__ == "__main__":
    main()
