# Guía de Contribución

¡Gracias por tu interés en contribuir al Sistema de Test de Daltonismo! Esta guía te ayudará a empezar.

## 📋 Proceso de Contribución

### 1. Fork y Clonar
```bash
# Fork el repositorio en GitHub, luego clona tu fork
git clone https://github.com/tu-usuario/daltonismo-test.git
cd daltonismo-test
```

### 2. Configurar Entorno de Desarrollo
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o en Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install -e ".[dev]"

# O usar Makefile
make dev-install
```

### 3. Crear Rama de Trabajo
```bash
# Crear rama para tu funcionalidad
git checkout -b feature/descripcion-breve
# o para correcciones de bugs
git checkout -b fix/descripcion-del-problema
```

### 4. Desarrollar y Probar
```bash
# Ejecutar tests
make test
# o manualmente
python -m pytest tests/ -v

# Verificar formato de código
make lint
make format
```

### 5. Commit y Push
```bash
# Hacer commits descriptivos
git add .
git commit -m "feat: añadir nueva funcionalidad X"
git push origin feature/descripcion-breve
```

### 6. Crear Pull Request
- Ve a GitHub y crea un Pull Request
- Describe claramente los cambios realizados
- Incluye screenshots si hay cambios en la UI
- Asegúrate de que los tests pasen

## 🎯 Tipos de Contribución

### 🐛 Reportar Bugs
- Usa el template de issue para bugs
- Incluye información del sistema (OS, Python version, etc.)
- Proporciona pasos para reproducir el problema
- Incluye logs de error si es posible

### ✨ Proponer Nuevas Funcionalidades
- Abre un issue describiendo la funcionalidad
- Explica el problema que resuelve
- Proporciona ejemplos de uso
- Discute la implementación antes de empezar a codificar

### 📚 Mejorar Documentación
- Corrige errores tipográficos
- Añade ejemplos de uso
- Mejora explicaciones técnicas
- Traduce documentación

### 🧪 Añadir Tests
- Tests unitarios para nuevas funcionalidades
- Tests de integración para flujos completos
- Tests de rendimiento para optimizaciones

## 📝 Estándares de Código

### Estilo Python
- Sigue PEP 8
- Usa `black` para formatear código
- Usa `flake8` para linting
- Añade docstrings a funciones y clases

```python
def calcular_puntuacion(respuestas_correctas: int, total_preguntas: int) -> float:
    """
    Calcula el porcentaje de aciertos en el test.
    
    Args:
        respuestas_correctas: Número de respuestas correctas
        total_preguntas: Número total de preguntas
        
    Returns:
        Porcentaje de aciertos (0.0 a 100.0)
        
    Raises:
        ValueError: Si total_preguntas es 0 o negativo
    """
    if total_preguntas <= 0:
        raise ValueError("El total de preguntas debe ser mayor a 0")
    
    return (respuestas_correctas / total_preguntas) * 100.0
```

### Mensajes de Commit
Usa el formato [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(alcance): descripción breve

Descripción más detallada si es necesario.

- Lista de cambios específicos
- Otro cambio importante
```

**Tipos de commit:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (sin cambios de lógica)
- `refactor`: Refactoring de código
- `test`: Añadir o modificar tests
- `chore`: Mantenimiento general

**Ejemplos:**
```
feat(ui): añadir botón de reiniciar test
fix(sensor): corregir detección de proximidad en RPi 4
docs(readme): actualizar instrucciones de instalación
test(ishihara): añadir tests para carga de láminas
```

## 🧪 Tests

### Ejecutar Tests
```bash
# Todos los tests
make test

# Tests específicos
python -m pytest tests/test_ishihara.py -v

# Con coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Escribir Tests
- Un test por funcionalidad específica
- Nombres descriptivos para los tests
- Usa fixtures para setup común
- Mock dependencias externas (GPIO, archivos)

```python
def test_calcular_puntuacion_casos_normales():
    """Test casos normales de cálculo de puntuación."""
    assert calcular_puntuacion(8, 10) == 80.0
    assert calcular_puntuacion(10, 10) == 100.0
    assert calcular_puntuacion(0, 10) == 0.0

def test_calcular_puntuacion_division_por_cero():
    """Test que se lance excepción con total_preguntas = 0."""
    with pytest.raises(ValueError):
        calcular_puntuacion(5, 0)
```

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios
- `src/`: Código fuente principal
- `tests/`: Tests automatizados
- `assets/`: Recursos (imágenes, etc.)
- `docs/`: Documentación adicional
- `scripts/`: Scripts de automatización
- `config/`: Archivos de configuración

### Componentes Principales
- `dalton.py`: Aplicación principal con UI
- `stats.py`: Cálculos estadísticos
- `test.py`: Lógica de tests

### Patrones de Diseño
- Separación de responsabilidades
- Inyección de dependencias para testabilidad
- Manejo de errores con excepciones específicas

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] Interfaz web opcional
- [ ] Soporte multiidioma
- [ ] Base de datos de resultados
- [ ] API REST para integración
- [ ] Tests de accesibilidad

### Mejoras Técnicas
- [ ] Migrar a Poetry para gestión de dependencias
- [ ] Añadir CI/CD con GitHub Actions
- [ ] Dockerizar la aplicación
- [ ] Añadir métricas de rendimiento

## 🆘 Obtener Ayuda

### Canales de Comunicación
- **Issues de GitHub**: Para bugs y solicitudes de funcionalidades
- **Discussions**: Para preguntas generales y ideas
- **Email**: [dev@example.com] para consultas privadas

### Recursos Útiles
- [Documentación de tkinter](https://docs.python.org/3/library/tkinter.html)
- [Raspberry Pi GPIO](https://raspberrypi.github.io/gpio/)
- [Pillow (PIL) docs](https://pillow.readthedocs.io/)

## 📄 Licencia

Al contribuir a este proyecto, aceptas que tus contribuciones se licencien bajo la misma licencia MIT que el proyecto.

---

¡Gracias por contribuir al Test de Daltonismo! 🎨👁️