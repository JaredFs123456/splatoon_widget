from PySide6.QtCore import Qt, QSize, QEvent, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QToolButton, QGridLayout
from PySide6.QtGui import QIcon

from config import PANEL_ANCHO, PANEL_ALTO, BOTON_ALTO


class AppIconButton(QToolButton):
    def __init__(self, parent=None, base_icon=QSize(45,45), hover_icon=QSize(52,52)):
        super().__init__(parent)
        self._base_icon = base_icon
        self._hover_icon = hover_icon

        self.setFocusPolicy(Qt.NoFocus)

        self._anim = QPropertyAnimation(self, b"iconSize", self)
        self._anim.setDuration(120)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self.iconSize())
        self._anim.setEndValue(self._hover_icon)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.stop()
        self._anim.setStartValue(self.iconSize())
        self._anim.setEndValue(self._base_icon)
        self._anim.start()
        super().leaveEvent(event)


def crear_area_iconos(panel_frame: QWidget):
    """
    Crea la zona usable de iconos (apps_area) y el grid layout.
    NO conecta lógica de abrir apps: eso se hace afuera.
    Devuelve: apps_area, grid
    """
    apps_area = QWidget(panel_frame)
    apps_area.setGeometry(0, 0, PANEL_ANCHO, PANEL_ALTO - BOTON_ALTO)
    apps_area.setAttribute(Qt.WA_TranslucentBackground, True)

    grid = QGridLayout(apps_area)
    grid.setContentsMargins(14, 14, 14, 14)
    grid.setHorizontalSpacing(12)
    grid.setVerticalSpacing(12)

    return apps_area, grid


def poblar_grid_iconos(apps_area: QWidget, grid: QGridLayout, apps: list, abrir_callback, cols: int = 3):
    """
    Crea y agrega botones al grid.
    apps = [(nombre, icono_path, target_path), ...]
    abrir_callback = función(path) que abre la app.
    """
    row = 0
    for i, (nombre, icono, target) in enumerate(apps):
        btn_app = AppIconButton(apps_area, base_icon=QSize(45,45), hover_icon=QSize(52,52))
        btn_app.setFocusPolicy(Qt.NoFocus)
        btn_app.setCursor(Qt.PointingHandCursor)
        btn_app.setToolTip(nombre)

        btn_app.setIcon(QIcon(icono))
        btn_app.setIconSize(QSize(45, 45))
        btn_app.setFixedSize(62, 62)


        base_icon = QSize(45, 45)
        hover_icon = QSize(52, 52)   # ajústalo a tu gusto (48–55 suele verse bien)

        btn_app.setIconSize(base_icon)
        btn_app.setFixedSize(62, 62)

        anim = QPropertyAnimation(btn_app, b"iconSize", btn_app)
        anim.setDuration(120)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        btn_app._hover_anim = anim  # guardar referencia para que no se destruya


        btn_app.setStyleSheet("""
            QToolButton {
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background: transparent;
                border: none;
            }
            QToolButton:pressed {
                background: transparent;
                border: none;
            }
        """)


        btn_app.clicked.connect(lambda checked=False, p=target: abrir_callback(p))

        row = i // cols
        col = i % cols
        grid.addWidget(btn_app, row, col, Qt.AlignCenter)

    # mantiene empuje hacia arriba si faltan iconos
    grid.setRowStretch(row + 1, 1)
