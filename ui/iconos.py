from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QToolButton, QGridLayout
from PySide6.QtGui import QIcon

from config import PANEL_ANCHO, PANEL_ALTO, BOTON_ALTO


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
        btn_app = QToolButton(apps_area)
        btn_app.setCursor(Qt.PointingHandCursor)
        btn_app.setToolTip(nombre)

        btn_app.setIcon(QIcon(icono))
        btn_app.setIconSize(QSize(45, 45))
        btn_app.setFixedSize(62, 62)

        btn_app.setStyleSheet("""
            QToolButton {
                background: rgba(0,0,0,0);
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QToolButton:hover {
                background: rgba(255,255,255,25);
                border-radius: 12px;
            }
        """)

        btn_app.clicked.connect(lambda checked=False, p=target: abrir_callback(p))

        row = i // cols
        col = i % cols
        grid.addWidget(btn_app, row, col, Qt.AlignCenter)

    # mantiene empuje hacia arriba si faltan iconos
    grid.setRowStretch(row + 1, 1)
