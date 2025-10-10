#!/bin/bash

echo "🔍 Diagnóstico del ejecutable - Test de Daltonismo"
echo "================================================="
echo ""

echo "📍 Directorio actual:"
pwd
echo ""

echo "🔍 Buscando ejecutables de TestDaltonismo:"
find . -name "*TestDaltonismo*" -type f 2>/dev/null | while read file; do
    echo "   ✅ Encontrado: $file"
    echo "      Tamaño: $(ls -lh "$file" | awk '{print $5}')"
    echo "      Permisos: $(ls -l "$file" | awk '{print $1}')"
    echo ""
done

echo "🔍 Buscando carpeta dist:"
if [ -d "dist" ]; then
    echo "   ✅ Carpeta dist encontrada"
    echo "   📂 Contenido de dist/:"
    ls -la dist/
else
    echo "   ❌ No se encontró la carpeta dist"
fi
echo ""

echo "🔍 Buscando carpeta build:"
if [ -d "build" ]; then
    echo "   ✅ Carpeta build encontrada"
    echo "   📂 Contenido de build/:"
    ls -la build/
else
    echo "   ❌ No se encontró la carpeta build"
fi
echo ""

echo "🔍 Archivos .spec encontrados:"
find . -name "*.spec" -type f 2>/dev/null | while read file; do
    echo "   📄 $file"
done
echo ""

echo "🔍 Logs de PyInstaller (si existen):"
find . -name "*.log" -type f 2>/dev/null | while read file; do
    echo "   📋 $file"
    echo "      Últimas líneas:"
    tail -5 "$file" | sed 's/^/         /'
done
echo ""

echo "📁 Contenido completo del directorio actual:"
ls -la
echo ""

echo "💡 Si no encuentras el ejecutable, intenta:"
echo "   1. Ejecutar: python3 dalton.py (sin compilar)"
echo "   2. Revisar errores: cat build/TestDaltonismo/warn-TestDaltonismo.txt"
echo "   3. Compilar de nuevo con: ./crear_ejecutable.sh"
