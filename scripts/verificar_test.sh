#!/bin/bash

echo "🧪 Verificación rápida del Test de Daltonismo"
echo "============================================="

# Verificar dependencias
echo "🔍 Verificando dependencias..."

if ! python3 -c "import tkinter, PIL, os, glob" 2>/dev/null; then
    echo "❌ Faltan dependencias. Ejecuta: ./instalar_dependencias.sh"
    exit 1
fi

# Verificar imágenes
echo "📸 Verificando imágenes Ishihara..."
IMAGES=$(ls *.jpg *.png 2>/dev/null | wc -l)
if [ $IMAGES -eq 0 ]; then
    echo "❌ No se encontraron imágenes (.jpg/.png)"
    exit 1
else
    echo "✅ Encontradas $IMAGES imágenes:"
    ls *.jpg *.png 2>/dev/null | head -5
fi

# Test sintáctico del código
echo "🔍 Verificando sintaxis del código..."
if python3 -m py_compile dalton_completo.py; then
    echo "✅ Sintaxis correcta"
else
    echo "❌ Error de sintaxis en dalton_completo.py"
    exit 1
fi

echo ""
echo "✅ Todo listo para ejecutar el test"
echo "🚀 Ejecuta: ./ejecutar_test_completo.sh"