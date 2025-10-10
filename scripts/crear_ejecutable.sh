#!/bin/bash

# Script para crear ejecutable del Test de Daltonismo para Linux/Raspberry Pi

echo "🔧 Verificando Python y dependencias..."

# Verificar Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado. Instalando..."
    sudo apt update && sudo apt install -y python3
fi

# Verificar tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ tkinter no encontrado. Instalando..."
    sudo apt install -y python3-tk
fi

# Verificar pip3
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no encontrado. Instalando..."
    sudo apt install -y python3-pip
fi

echo "✅ Dependencias del sistema verificadas"

echo "🔧 Instalando PyInstaller..."
pip3 install --user pyinstaller

# Asegurar que el PATH incluye ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"

echo "📦 Creando ejecutable..."
~/.local/bin/pyinstaller --onefile --windowed --name="TestDaltonismo" dalton.py

# Verificar si se creó correctamente
if [ -f "dist/TestDaltonismo" ]; then
    echo "✅ ¡Ejecutable creado exitosamente!"
    echo "📁 Ubicación: $(pwd)/dist/TestDaltonismo"
    echo "📏 Tamaño: $(ls -lh dist/TestDaltonismo | awk '{print $5}')"
    
    # Hacer ejecutable automáticamente
    chmod +x dist/TestDaltonismo
    echo "🔑 Permisos de ejecución aplicados"
    
    echo ""
    echo "🚀 Para ejecutar AHORA:"
    echo "   ./dist/TestDaltonismo"
    echo ""
    echo "📋 Contenido del directorio dist:"
    ls -la dist/
else
    echo "❌ Error: No se pudo crear el ejecutable"
    echo "🔍 Buscando archivos generados..."
    find . -name "*TestDaltonismo*" -type f 2>/dev/null || echo "No se encontró ningún archivo"
    echo ""
    echo "📁 Contenido del directorio actual:"
    ls -la
fi

echo ""
echo "💡 Consejo para pantalla táctil:"
echo "   El programa ya está optimizado para touch - los botones son grandes y responsivos"
