# 👁️ Sistema de Detección de Daltonismo - Manos Para la Vista

![Logo](img/logo.png)

Sistema profesional de detección de daltonismo para Raspberry Pi con hardware especializado y reportes automáticos vía Telegram.

## 🎯 Características

- 🎨 **Test de colores básicos** (8 rondas)
- 👁️ **Test de láminas Ishihara** (6 láminas)
- 📡 **Sensor ultrasónico HC-SR04** (detección automática de proximidad)
- 🔊 **Buzzer 3V** (feedback auditivo con pips)
- 🔄 **Servo motor MG996R** (indicador visual de resultados)
- 💡 **Tira LED RGB 5V** (feedback por colores: azul/verde/rojo)
- 📄 **Reportes PDF** automáticos
- 📱 **Envío a Telegram** de resultados
- 🖥️ **Interfaz táctil fullscreen** optimizada

---

## 🚀 Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/e1th4nUwU/manos-para-la-vista-diseno-mecatronico.git
cd manos-para-la-vista-diseno-mecatronico

# Instalar dependencias
chmod +x scripts/instalar_dependencias.sh
./scripts/instalar_dependencias.sh

# Configurar Telegram (opcional)
nano src/.env
# Agregar: TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID

# Ejecutar
python3 src/dalton.py
```

---

## 🔧 Hardware Requerido

| Componente             | Modelo         | Pin GPIO                            | Pin Físico |
| ---------------------- | -------------- | ----------------------------------- | ---------- |
| **Sensor ultrasónico** | HC-SR04        | TRIG: GPIO17<br>ECHO: GPIO27        | 11, 13     |
| **Servo motor**        | MG996R         | GPIO18                              | 12         |
| **Buzzer**             | 3V activo      | GPIO23                              | 16         |
| **LED RGB**            | 5V ánodo común | R: GPIO24<br>G: GPIO25<br>B: GPIO21 | 18, 22, 40 |

### Diagrama de Conexiones

```
┌──────────────────────────────────────────────────┐
│           Raspberry Pi GPIO Header               │
│                                                  │
│  3V3  (1) (2)  5V  ◄──── HC-SR04 VCC            │
│       (3) (4)  5V  ◄──── Servo VCC / RGB Común  │
│       (5) (6)  GND ◄──── HC-SR04 GND            │
│ GPIO17(11)(12) GPIO18 ◄──── Servo Signal        │
│ GPIO27(13)(14) GND ◄──── Servo GND              │
│       (15)(16) GPIO23 ◄──── Buzzer VCC          │
│       (17)(18) GPIO24 ◄──── RGB Red             │
│       (19)(20) GND ◄──── Buzzer GND             │
│       (21)(22) GPIO25 ◄──── RGB Green           │
│       (...)                                     │
│       (39)(40) GPIO21 ◄──── RGB Blue            │
└──────────────────────────────────────────────────┘
```

⚠️ **Importante**: 
- LED RGB es **ánodo común** (común a 5V, canales a GPIO)
- HC-SR04 requiere **5V** (no 3.3V)
- Servo puede necesitar alimentación externa

---

## 🎮 Modos de Operación

### Modo Completo (con todo el hardware)
```bash
python3 src/dalton.py
```

### Modo Sin Sensor (buzzer, servo y RGB activos)
```bash
python3 src/dalton.py --no-sensor
```

### Modo Simulación (sin hardware, para desarrollo en PC)
```bash
python3 src/dalton.py --no-hardware
```

---

## 📱 Configuración de Telegram

1. **Crear bot**: Buscar `@BotFather` en Telegram y crear un bot
2. **Obtener Chat ID**: Enviar mensaje al bot y visitar:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. **Configurar `.env`**: Editar `src/.env`:
   ```env
   TELEGRAM_BOT_TOKEN=tu_token_aqui
   TELEGRAM_CHAT_ID=tu_chat_id_aqui
   ENV=production
   ```

📖 **Guía completa**: Ver [`docs/TELEGRAM_SETUP.md`](docs/TELEGRAM_SETUP.md)

---

## 🎨 Sistema de Feedback

### 🔊 Buzzer (GPIO23)
- **1 pip**: Respuesta correcta (1200 Hz)
- **2 pips**: Respuesta incorrecta (800 Hz)
- **3 pips**: Inicio de test (1500 Hz)

### 🔄 Servo (GPIO18)
- **180°**: Visión normal (≥85%)
- **135°**: Deficiencia leve (75-84%)
- **90°**: Deficiencia moderada (65-74%)
- **0°**: Deficiencia severa (<65%)

### 💡 LED RGB (ánodo común)
- **🔵 Azul**: Sistema listo / en progreso
- **🟢 Verde**: Resultado positivo (≥75%)
- **🔴 Rojo**: Resultado negativo (<75%)

### 📡 Sensor (GPIO17/27)
- **Umbral**: 50 cm
- **Pausa automática** si el usuario se aleja
- **Continúa automáticamente** al regresar

---

## 📄 Reportes PDF

Los reportes se generan automáticamente al finalizar cada test:

**Contenido:**
- Logo del proyecto
- Fecha y hora
- Resultados detallados (Colores + Ishihara)
- Evaluación diagnóstica
- Recomendaciones

**Ubicación:** `reports/reporte_daltonismo_YYYYMMDD_HHMMSS.pdf`

**Telegram:** Si está configurado, se envía automáticamente al chat/grupo

---

## 📊 Sistema de Diagnóstico

| Puntuación | Diagnóstico            | Servo | LED        |
| ---------- | ---------------------- | ----- | ---------- |
| **≥85%**   | ✅ Visión normal        | 180°  | 🟢 Verde    |
| **75-84%** | ⚠️ Deficiencia leve     | 135°  | 🟡 Amarillo |
| **65-74%** | 🔶 Deficiencia moderada | 90°   | 🟠 Naranja  |
| **<65%**   | 🔴 Deficiencia severa   | 0°    | 🔴 Rojo     |

---

## 📁 Estructura del Proyecto

```
manos-para-la-vista-diseno-mecatronico/
├── src/
│   ├── dalton.py              # Programa principal
│   ├── lib/Notification.py    # Reportes PDF y Telegram
│   └── .env                   # Configuración Telegram
├── assets/images/             # Láminas Ishihara
├── img/logo.png               # Logo del proyecto
├── docs/                      # Documentación detallada
├── scripts/                   # Scripts de automatización
├── tests/                     # Tests automatizados
└── reports/                   # PDFs generados
```

---

## 📚 Documentación Adicional

- [`docs/MODO_SIMULACION.md`](docs/MODO_SIMULACION.md) - Guía de modos sin hardware
- [`docs/TELEGRAM_SETUP.md`](docs/TELEGRAM_SETUP.md) - Configuración de Telegram
- [`docs/OPTIMIZACIONES_RASPBERRY_PI.md`](docs/OPTIMIZACIONES_RASPBERRY_PI.md) - Tips de rendimiento
- [`CHANGELOG.md`](CHANGELOG.md) - Historial de versiones
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - Guía de contribución

---

## 🔧 Solución Rápida de Problemas

**Sensor no detecta:**
```bash
python3 src/dalton.py --no-sensor  # Usar modo sin sensor
```

**Sin hardware disponible:**
```bash
python3 src/dalton.py --no-hardware  # Modo simulación
```

**Error de módulos:**
```bash
pip3 install -r requirements.txt
```

**Permisos GPIO:**
```bash
sudo usermod -a -G gpio \$USER
# O ejecutar con sudo
```

---

## ⚠️ Disclaimer

> Este sistema es para **propósitos educativos y de screening preliminar**. NO sustituye un examen oftalmológico profesional.

**Casos de uso apropiados:**
- ✅ Proyectos educativos y ferias de ciencias
- ✅ Talleres de concientización
- ✅ Screening preliminar en escuelas
- ❌ NO para diagnósticos médicos oficiales

---

## 📜 Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

---

## 🙏 Créditos

Desarrollado por el equipo **Manos Para la Vista** - Diseño Mecatrónico

**Tecnologías:**
Python 3 • Tkinter • RPi.GPIO • Pillow • ReportLab • python-telegram-bot

**Basado en:** Láminas Ishihara (Dr. Shinobu Ishihara, 1917)

## 📞 Soporte

**Reportar bugs:** [GitHub Issues](https://github.com/e1th4nUwU/manos-para-la-vista-diseno-mecatronico/issues)

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

[![GitHub stars](https://img.shields.io/github/stars/e1th4nUwU/manos-para-la-vista-diseno-mecatronico?style=social)](https://github.com/e1th4nUwU/manos-para-la-vista-diseno-mecatronico)

### Hecho con ❤️ por el equipo Manos Para la Vista

</div>
