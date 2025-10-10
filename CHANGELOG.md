# Changelog

Todos los cambios importantes de este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [No lanzado]

### Planeado
- Interfaz web opcional
- Soporte para múltiples idiomas
- Base de datos de resultados
- API REST para integración

## [1.0.0] - 2025-10-10

### Añadido
- Sistema completo de detección de daltonismo
- Test de colores básicos (8 rondas)
- Test de láminas Ishihara dinámicas (6 láminas)
- Integración con sensor ultrasónico HC-SR04
- Soporte para Raspberry Pi y pantallas táctiles
- Sistema de diagnóstico combinado
- Scripts de instalación automática
- Interfaz gráfica con tkinter
- Gestión de recursos GPIO
- Modo simulación para sistemas sin GPIO
- Documentación completa
- Estructura de proyecto organizada
- Configuración de desarrollo

### Características técnicas
- Detección automática de proximidad
- Pausa inteligente cuando el usuario se aleja
- Pantalla de espera con información en tiempo real
- Threading no bloqueante para sensores
- Limpieza automática de recursos
- Generación eficiente de láminas Ishihara
- Gestión optimizada de memoria
- Sistema de puntuación avanzado

### Soporte
- Python 3.8+
- Raspberry Pi OS
- Dependencias: Pillow, numpy, RPi.GPIO
- Pantallas táctiles optimizadas
- Botones grandes para interacción táctil

### Documentación
- README completo con ejemplos
- Instrucciones de instalación
- Guías de solución de problemas
- Diagramas de conexión de hardware
- Documentación de API interna

## [0.1.0] - 2025-09-22

### Añadido
- Versión inicial del proyecto
- Test básico de daltonismo
- Láminas Ishihara estáticas
- Interfaz básica con tkinter

---

## Tipos de cambios
- `Añadido` para nuevas funcionalidades
- `Cambiado` para cambios en funcionalidades existentes
- `Obsoleto` para funcionalidades que se eliminarán pronto
- `Eliminado` para funcionalidades eliminadas
- `Arreglado` para corrección de errores
- `Seguridad` en caso de vulnerabilidades