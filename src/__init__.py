"""
Sistema de Test de Daltonismo para Raspberry Pi.

Este paquete contiene módulos para realizar tests de daltonismo
combinando pruebas de colores básicos y láminas Ishihara con
detección de proximidad mediante sensor ultrasónico.
"""

__version__ = "1.0.0"
__author__ = "Developer Team"
__email__ = "dev@example.com"

# Importaciones principales
try:
    from .dalton import TestDaltonismoCompleto, IshiharaImageLoader
except ImportError:
    # En caso de que las dependencias no estén disponibles
    pass