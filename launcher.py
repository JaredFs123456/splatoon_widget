import os
from PySide6.QtCore import QProcess


def abrir_app(path: str):
    try:
        # Esto abre .lnk, .exe, carpetas, etc. en Windows
        os.startfile(path)
    except Exception:
        # Fallback (por si algo falla)
        QProcess.startDetached(path)
