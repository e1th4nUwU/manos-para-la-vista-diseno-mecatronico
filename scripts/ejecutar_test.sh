#!/bin/bash

echo "🚀 EJECUTOR DIRECTO - Test de Daltonismo"
echo "========================================"
echo ""

# Verificar dependencias del sistema
echo "🔍 Verificando dependencias..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado. Instalando..."
    sudo apt update && sudo apt install -y python3
else
    echo "✅ Python3: $(python3 --version)"
fi

if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ tkinter no encontrado. Instalando..."
    sudo apt install -y python3-tk
else
    echo "✅ tkinter disponible"
fi

echo ""
echo "🎯 Lanzando Test de Daltonismo..."
echo "💡 Para salir: presiona el botón 'Salir' o Ctrl+C"
echo ""

# Ejecutar en pantalla completa
python3 dalton.py
