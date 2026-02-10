from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Property
from PySide6.QtGui import QPainter, QPainterPath

from config import DIAGONAL


class PanelPintura(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self._progress = 0.0
        self._pixmap = pixmap
        self.setFixedSize(pixmap.size())

    def setProgress(self, value):
        self._progress = value
        self.update()

    def getProgress(self):
        return self._progress

    progress = Property(float, getProgress, setProgress)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        visible_h = int(h * self._progress)

        max_diagonal = int(w * DIAGONAL)  # aquí controlas inclinación máxima
        diagonal_offset = int(max_diagonal * (1.0 - self._progress))  # se va a 0 al final

        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(w, 0)

        # Borde derecho con diagonal
        path.lineTo(w, max(0, visible_h - diagonal_offset))
        path.lineTo(max(0, w - diagonal_offset), visible_h)

        # Base y lado izquierdo rectos
        path.lineTo(0, visible_h)
        path.closeSubpath()

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self._pixmap)
