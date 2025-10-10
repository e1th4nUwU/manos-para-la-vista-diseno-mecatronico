#!/bin/bash

echo "📦 Instalando dependencias para Test Completo de Daltonismo"
echo "=========================================================="

# Actualizar sistema
echo "🔄 Actualizando sistema..."
sudo apt update

# Instalar dependencias del sistema
echo "🔧 Instalando dependencias del sistema..."
sudo apt install -y python3-pip python3-tk python3-pil python3-pil.imagetk python3-numpy

# Instalar librerías Python adicionales
echo "🐍 Instalando librerías Python..."
pip3 install --user pillow numpy

# Si está en Raspberry Pi, instalar GPIO
if [[ $(uname -m) == arm* ]] || [[ $(uname -m) == aarch64 ]]; then
    echo "📡 Detectada Raspberry Pi - Instalando RPi.GPIO..."
    sudo apt install -y python3-rpi.gpio
    echo "✅ RPi.GPIO instalado para control del sensor"
else
    echo "⚠️ No es Raspberry Pi - El sensor será simulado"
fi

# Verificar instalaciones
echo ""
echo "🔍 Verificando instalaciones..."

if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ tkinter: OK"
else
    echo "❌ tkinter: FALTA"
fi

if python3 -c "import PIL" 2>/dev/null; then
    echo "✅ PIL (Pillow): OK"
else
    echo "❌ PIL (Pillow): FALTA"
    echo "📦 Intentando instalar Pillow..."
    pip3 install --user Pillow
fi

if python3 -c "import numpy" 2>/dev/null; then
    echo "✅ numpy: OK"
else
    echo "❌ numpy: FALTA"
    echo "📦 Intentando instalar numpy..."
    pip3 install --user numpy
fi

# Solo verificar GPIO en Raspberry Pi
if [[ $(uname -m) == arm* ]] || [[ $(uname -m) == aarch64 ]]; then
    if python3 -c "import RPi.GPIO" 2>/dev/null; then
        echo "✅ RPi.GPIO: OK"
    else
        echo "❌ RPi.GPIO: FALTA"
        echo "📦 Instalando RPi.GPIO..."
        sudo apt install -y python3-rpi.gpio
    fi
fi

echo ""
echo "✅ Instalación completada"
echo ""
echo "🚀 Para ejecutar el test completo:"
echo "   cd .."
echo "   python3 src/dalton.py"
echo ""
echo "📋 Características del test:"
echo "   ✓ Test de colores básicos (8 rondas)"
echo "   ✓ Test de láminas Ishihara (6 láminas generadas)"
echo "   ✓ Sensor de proximidad ultrasónico HC-SR04"
echo "   ✓ Diagnóstico combinado preciso"
echo "   ✓ Interfaz táctil optimizada para Raspberry Pi"
echo ""
echo "🔌 Conexiones del sensor HC-SR04:"
echo "   VCC  -> Pin 2 (5V)"
echo "   GND  -> Pin 6 (Ground)"
echo "   Trig -> Pin 11 (GPIO17)"
echo "   Echo -> Pin 13 (GPIO27)"