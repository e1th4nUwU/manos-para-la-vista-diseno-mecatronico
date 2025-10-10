"""
Configuración de pytest para el proyecto de Test de Daltonismo.
"""

import sys
import os

# Añadir el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configuración para tests que requieren GUI
import pytest
import tkinter as tk

@pytest.fixture(scope="session")
def tk_root():
    """Fixture para crear una instancia de Tkinter root para tests de GUI."""
    try:
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana
        yield root
        root.destroy()
    except tk.TclError:
        # Si no hay display disponible (CI), usar mock
        pytest.skip("No hay display disponible para tests de GUI")