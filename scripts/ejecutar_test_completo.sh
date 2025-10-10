#!/bin/bash

echo "🎯 Test Completo de Daltonismo con Sensor Ultrasónico"
echo "====================================================="

# Verificar si está en Raspberry Pi
if [[ $(uname -m) == arm* ]] || [[ $(uname -m) == aarch64 ]]; then
    echo "✅ Raspberry Pi detectada"
    echo "📡 Modo sensor ultrasónico activado"
    SENSOR_MODE="real"
else
    echo "⚠️ No es Raspberry Pi - Modo simulación"
    SENSOR_MODE="sim"
fi

echo ""
echo "🔍 Verificando dependencias..."

# Verificar Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado"
    echo "📦 Ejecuta primero: ./instalar_dependencias.sh"
    exit 1
else
    echo "✅ Python3: $(python3 --version)"
fi

# Verificar tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ tkinter no encontrado"
    echo "📦 Ejecuta: ./instalar_dependencias.sh"
    exit 1
else
    echo "✅ tkinter: OK"
fi

# Verificar PIL
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "❌ PIL no encontrado"
    echo "📦 Instalando PIL..."
    pip3 install --user Pillow
    if ! python3 -c "import PIL" 2>/dev/null; then
        echo "❌ Error instalando PIL"
        exit 1
    fi
fi
echo "✅ PIL: OK"

# Verificar numpy
if ! python3 -c "import numpy" 2>/dev/null; then
    echo "❌ numpy no encontrado"
    echo "📦 Instalando numpy..."
    pip3 install --user numpy
    if ! python3 -c "import numpy" 2>/dev/null; then
        echo "❌ Error instalando numpy"
        exit 1
    fi
fi
echo "✅ numpy: OK"

# Verificar GPIO solo en Raspberry Pi
if [[ $SENSOR_MODE == "real" ]]; then
    if ! python3 -c "import RPi.GPIO" 2>/dev/null; then
        echo "❌ RPi.GPIO no encontrado"
        echo "📦 Instalando RPi.GPIO..."
        sudo apt install -y python3-rpi.gpio
        if ! python3 -c "import RPi.GPIO" 2>/dev/null; then
            echo "❌ Error instalando RPi.GPIO"
            echo "⚠️ Continuando en modo simulación"
        else
            echo "✅ RPi.GPIO: OK"
        fi
    else
        echo "✅ RPi.GPIO: OK"
    fi
fi

echo ""
echo "🚀 Iniciando Test Completo de Daltonismo..."
echo ""

if [[ $SENSOR_MODE == "real" ]]; then
    echo "💡 Instrucciones con sensor:"
    echo "   - Conecta el sensor HC-SR04 según el diagrama"
    echo "   - Mantente a menos de 1 metro para iniciar"
    echo "   - El test se compone de 2 partes:"
    echo "     1. Test de colores básicos (8 rondas)"
    echo "     2. Test de láminas Ishihara (6 láminas)"
    echo "   - Si te alejas mucho, el test se pausará automáticamente"
else
    echo "💡 Instrucciones en modo simulación:"
    echo "   - El sensor está simulado (siempre detecta usuario cerca)"
    echo "   - El test funciona normalmente en 2 partes:"
    echo "     1. Test de colores básicos (8 rondas)"
    echo "     2. Test de láminas Ishihara (6 láminas)"
fi

echo ""
echo "📊 Al finalizar recibirás:"
echo "   - Puntuación en test de colores"
echo "   - Puntuación en test Ishihara"
echo "   - Diagnóstico combinado"
echo "   - Recomendaciones específicas"
echo ""

# Verificar que el archivo principal existe
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MAIN_SCRIPT="$PROJECT_DIR/src/dalton.py"

if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "❌ Error: No se encuentra src/dalton.py"
    echo "📁 Verifica que estés en el directorio correcto del proyecto"
    echo "📍 Directorio actual: $(pwd)"
    echo "📍 Buscando: $MAIN_SCRIPT"
    exit 1
fi

echo "🎯 Iniciando aplicación..."
echo "⌨️ Para salir: presiona el botón 'Salir' o Ctrl+C"
echo ""

# Cambiar al directorio del proyecto y ejecutar
cd "$PROJECT_DIR"
python3 src/dalton.py