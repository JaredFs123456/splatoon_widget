import sys
from PySide6.QtWidgets import QApplication

from Calamar_Desplegable import CalamarDesplegable


def main():
    app = QApplication(sys.argv)
    w = CalamarDesplegable()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
