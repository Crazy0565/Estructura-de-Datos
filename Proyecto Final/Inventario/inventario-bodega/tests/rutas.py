"""Rutas del proyecto para las pruebas que necesitan los CSV de ejemplo."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EJEMPLO = RAIZ / "datos" / "ejemplo"
