"""Packaged dictionaries and persistent, system-aware language selection."""

import json
from PySide6.QtCore import QObject, QLocale, Signal
from .catalog import ASSETS


class Translator(QObject):
    changed = Signal()
    languages = ("ru", "en")

    def __init__(self, settings, system_language=None):
        super().__init__()
        self.settings = settings
        self.dictionaries = {
            code: json.loads((ASSETS / "locales" / f"{code}.json").read_text(encoding="utf-8"))
            for code in self.languages
        }
        # UI language preferences take priority over regional number/date formats.
        system = system_language or next(iter(QLocale.system().uiLanguages()), QLocale.system().name())
        default = "ru" if system.lower().startswith("ru") else "en"
        saved = settings.value("language")
        self.language = saved if saved in self.languages else default

    def set_language(self, language):
        if language not in self.languages:
            raise ValueError(language)
        self.settings.setValue("language", language)
        if language != self.language:
            self.language = language
            self.changed.emit()

    def text(self, key, **values):
        return self.dictionaries[self.language]["ui"][key].format(**values)

    def item_name(self, item):
        return getattr(item, "name_en", item.name) if self.language == "en" else item.name

    def number(self, value):
        return f"{value:,}".replace(",", " " if self.language == "ru" else ",")

    def quantity(self, value):
        if self.language == "ru":
            form = (
                "many"
                if 11 <= value % 100 <= 14
                else "one"
                if value % 10 == 1
                else "few"
                if 2 <= value % 10 <= 4
                else "many"
            )
        else:
            form = "one" if value == 1 else "many"
        return self.text("chests_" + form, n=self.number(value))
