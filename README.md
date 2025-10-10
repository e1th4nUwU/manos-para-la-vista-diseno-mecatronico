# Test Completo de Daltonismo con Sensor Ultrasónico

## 🎯 Descripción
Sistema completo de detección de daltonismo que combina:
- **Test de colores básicos** (8 rondas)
- **Test de láminas Ishihara** generadas dinámicamente (6 láminas)
- **Sensor ultrasónico HC-SR04** para detección de proximidad
- **Diagnóstico combinado** con alta precisión

## 🚀 Instalación Rápida

### 1. Instalar dependencias automáticamente:
```bash
chmod +x instalar_dependencias.sh
./instalar_dependencias.sh
```

### 2. Ejecutar el test:
```bash
chmod +x ejecutar_test_completo.sh
./ejecutar_test_completo.sh
```

## 🔌 Conexiones del Sensor HC-SR04

```
Raspberry Pi          HC-SR04
Pin 2 (5V)     -----> VCC
Pin 6 (GND)    -----> GND  
Pin 11 (GPIO17)-----> Trig
Pin 13 (GPIO27)-----> Echo
```

### Diagrama visual:
```
    ┌─────────────┐
    │   HC-SR04   │
    │             │
    │ VCC GND Trig Echo │
    │  │   │   │    │ │
    └──┼───┼───┼────┼─┘
       │   │   │    │
       │   │   │    └── Pin 13 (GPIO27)
       │   │   └─────── Pin 11 (GPIO17)  
       │   └─────────── Pin 6 (GND)
       └─────────────── Pin 2 (5V)
```

## 📋 Características del Test

### 🎨 Test de Colores Básicos
- **8 rondas** de identificación
- Colores: Rojo, Verde, Azul, Amarillo, Naranja, Morado
- Detección de confusiones básicas de color
- Interfaz táctil optimizada

### 👁️ Test de Láminas Ishihara
- **6 láminas** generadas automáticamente
- Números del 0-9 para responder
- Diferentes tipos de daltonismo:
  - **Protanopia** (dificultad rojo-verde)
  - **Deuteranopia** (dificultad verde-rojo)  
  - **Tritanopia** (dificultad azul-amarillo)
- Opción "No veo ningún número"

### 📡 Sensor de Proximidad
- **Detección automática** a menos de 1 metro
- **Pausa inteligente** si el usuario se aleja
- **Pantalla de espera** con información en tiempo real
- **Modo simulación** en sistemas sin GPIO

## 📊 Sistema de Diagnóstico

### Puntuación combinada:
- **≥85%**: ✅ Visión de colores normal
- **70-84%**: ⚠️ Posible daltonismo leve
- **50-69%**: 🔶 Probable daltonismo moderado  
- **<50%**: 🔴 Probable daltonismo severo

### Recomendaciones automáticas:
- Normal: Sin signos de daltonismo
- Leve: Consulta con especialista recomendada
- Moderado: Evaluación oftalmológica necesaria
- Severo: Consulta urgente requerida

## 🛠️ Instalación Manual

### Dependencias del sistema:
```bash
sudo apt update
sudo apt install -y python3-pip python3-tk python3-pil python3-pil.imagetk python3-numpy python3-rpi.gpio
```

### Librerías Python:
```bash
pip3 install --user pillow numpy
```

## 🚀 Uso

### Ejecución directa:
```bash
python3 dalton_completo.py
```

### Con script completo:
```bash
./ejecutar_test_completo.sh
```

## 💡 Optimizaciones para Raspberry Pi

### Pantalla táctil:
- ✅ Botones grandes (optimizados para dedos)
- ✅ Efectos hover compatibles con touch
- ✅ Interfaz fullscreen automática
- ✅ Navegación intuitiva

### Rendimiento:
- ✅ Generación eficiente de láminas Ishihara
- ✅ Gestión optimizada de memoria
- ✅ Threading para sensor no bloqueante
- ✅ Limpieza automática de recursos GPIO

## 🔧 Configuración Avanzada

### Ajustar distancia del sensor:
```python
# En dalton_completo.py línea 15
MIN_DISTANCE = 100  # Cambiar a distancia deseada en cm
```

### Modificar cantidad de tests:
```python
# En la clase TestDaltonismoCompleto
self.color_attempts = 8      # Rondas de colores
self.ishihara_attempts = 6   # Láminas Ishihara
```

### Cambiar pines GPIO:
```python
# En dalton_completo.py líneas 13-14
TRIG_PIN = 17  # Pin Trigger
ECHO_PIN = 27  # Pin Echo
```

## 🐛 Solución de Problemas

### Error "No module named 'PIL'":
```bash
pip3 install --user Pillow
```

### Error "No module named 'RPi.GPIO'":
```bash
sudo apt install python3-rpi.gpio
```

### Sensor no funciona:
1. Verificar conexiones físicas
2. Comprobar voltaje (5V para VCC)
3. Revisar permisos GPIO
4. Ejecutar como sudo si es necesario

### Problemas de interfaz:
```bash
sudo apt install python3-tk python3-pil.imagetk
```

## 📁 Estructura del Proyecto

```
daltonismo-test/
├── src/                        # Código fuente principal
│   ├── dalton.py              # Programa principal del test
│   ├── stats.py               # Análisis estadístico
│   ├── test.py                # Módulo de pruebas
│   └── data.csv               # Datos de prueba
├── assets/                     # Recursos del proyecto
│   └── images/                # Láminas Ishihara y capturas
│       ├── 12.jpg, 13.png, etc.
│       └── Screenshot_*.png
├── scripts/                    # Scripts de automatización
│   ├── instalar_dependencias.sh
│   ├── ejecutar_test_completo.sh
│   ├── crear_ejecutable.sh
│   ├── ejecutar_test.sh
│   └── verificar_test.sh
├── config/                     # Archivos de configuración
│   ├── dalton.spec            # Configuración PyInstaller
│   └── TestDaltonismo.spec
├── docs/                       # Documentación del proyecto
├── tests/                      # Tests automatizados
├── build/                      # Archivos de compilación (ignorado)
├── dist/                       # Distribución (ignorado)
├── venv/                       # Entorno virtual (ignorado)
├── requirements.txt            # Dependencias Python
├── setup.py                    # Configuración de instalación
├── LICENSE                     # Licencia del proyecto
├── CHANGELOG.md               # Registro de cambios
├── .gitignore                 # Archivos ignorados por Git
└── README.md                  # Este archivo
```

## 🎉 Características Especiales

### � Reinicio inteligente:
- Mantiene configuración de sensor
- Limpia recursos correctamente
- Resetea variables de estado

### 🎨 Animaciones suaves:
- Transiciones de pantalla fluidas
- Efectos visuales para feedback
- Indicadores de progreso animados

### 📱 Interfaz adaptativa:
- Responsive para diferentes resoluciones
- Optimizada para pantallas táctiles
- Navegación por botones grandes

### 🛡️ Gestión de errores:
- Manejo robusto de excepciones GPIO
- Fallback a modo simulación
- Recuperación automática de errores

## � Desarrollo

### Configurar entorno de desarrollo:

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd daltonismo-test

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o en Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt

# Ejecutar tests
python -m pytest tests/

# Formatear código
black src/
flake8 src/
```

### Estructura de desarrollo:
- `src/`: Código fuente principal
- `tests/`: Tests unitarios y de integración
- `docs/`: Documentación técnica
- `scripts/`: Scripts de automatización y deployment
- `config/`: Archivos de configuración

### Contribuir:
1. Fork del repositorio
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## �📞 Información Adicional

Este sistema está diseñado específicamente para uso médico/educativo en Raspberry Pi con pantallas táctiles. La combinación de tests de colores básicos y láminas Ishihara proporciona una evaluación más completa y precisa del daltonismo.

**⚠️ Nota importante**: Este test es para propósitos educativos y de screening. Para diagnósticos médicos oficiales, siempre consulte con un profesional de la salud visual.
