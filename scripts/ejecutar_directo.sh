#!/bin/bash

echo "🚀 Ejecutando Test de Daltonismo directamente con Python"
echo "======================================================"
echo ""

# Verificar que Python3 y tkinter estén disponibles
echo "🔍 Verificando dependencias..."

if command -v python3 &> /dev/null; then
    echo "   ✅ Python3 encontrado: $(python3 --version)"
else
    echo "   ❌ Python3 no encontrado"
    echo "   💡 Instalar con: sudo apt install python3"
    exit 1
fi

if python3 -c "import tkinter" 2>/dev/null; then
    echo "   ✅ tkinter disponible"
else
    echo "   ❌ tkinter no encontrado"
    echo "   💡 Instalar con: sudo apt install python3-tk"
    exit 1
fi

echo ""
echo "🎯 Iniciando Test de Daltonismo..."
echo ""

# Ejecutar el programa
if [ -f "dalton.py" ]; then
    python3 dalton.py
else
    echo "❌ Error: No se encontró dalton.py en el directorio actual"
    echo "📍 Directorio actual: $(pwd)"
    echo "📁 Archivos disponibles:"
    ls -la *.py 2>/dev/null || echo "   No hay archivos .py"
fi
