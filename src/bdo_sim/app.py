"""Desktop entry point; resources are resolved relative to the package."""

import os
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths, QTimer, QSettings
from PySide6.QtWidgets import QApplication, QMessageBox

from bdo_sim.catalog import load_catalog
from bdo_sim.storage import History
from bdo_sim.ui.window import Window
from bdo_sim.i18n import Translator


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("PetProjects")
    app.setApplicationName("BDOChestStudio")
    app.setStyle("Fusion")
    settings = QSettings("PetProjects", "BDOChestStudio")
    translator = Translator(settings)
    try:
        data = Path(
            os.environ.get("BDO_SIM_DATA_DIR")
            or QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        )
        window = Window(load_catalog(), History(data / "history.sqlite3"), settings, translator)
    except Exception as exc:
        QMessageBox.critical(None, translator.text("app_title"), translator.text("error_startup", error=exc))
        return 1
    window.show()
    if "--smoke-test" in sys.argv:
        QTimer.singleShot(400, app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
