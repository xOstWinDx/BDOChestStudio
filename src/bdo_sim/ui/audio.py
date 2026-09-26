"""One sound switch and player for the whole application."""

from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import QSoundEffect

from ..catalog import ASSETS


class Audio(QObject):
    def __init__(self, parent=None, enabled=True):
        super().__init__(parent)
        self.enabled = enabled
        self.sounds = {}
        for name, volume in [("tick", 0.12), ("land", 0.18), ("rare", 0.22)]:
            sound = QSoundEffect(self)
            sound.setSource(QUrl.fromLocalFile(str(ASSETS / "sounds" / (name + ".wav"))))
            sound.setVolume(volume)
            self.sounds[name] = sound

    def set_enabled(self, enabled):
        self.enabled = enabled
        if not enabled:
            self.stop()

    def play(self, name):
        sound = self.sounds[name]
        if self.enabled and sound.status() == QSoundEffect.Status.Ready:
            sound.play()

    def stop(self):
        for sound in self.sounds.values():
            sound.stop()
