# Configuración de Reportes PDF y Telegram

Este documento explica cómo configurar el sistema de reportes PDF automáticos que se envían a Telegram al finalizar cada test de daltonismo.

## Características

- ✅ Generación automática de PDF con los resultados del test
- ✅ Envío automático a un grupo/chat de Telegram
- ✅ Reporte profesional con:
  - Fecha y hora del test
  - ID del paciente
  - Resultados detallados (Test de Colores e Ishihara)
  - Porcentajes de acierto
  - Evaluación y recomendaciones

## Requisitos

Instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```

Esto instalará:
- `python-telegram-bot==20.7` - Para enviar mensajes y documentos a Telegram
- `reportlab>=4.0.0` - Para generar PDFs
- `python-dotenv>=1.0.0` - Para manejar variables de entorno

## Configuración Paso a Paso

### 1. Crear un Bot de Telegram

1. Abre Telegram y busca `@BotFather`
2. Envía el comando `/newbot`
3. Sigue las instrucciones para darle un nombre y username a tu bot
4. Guarda el **token** que te proporciona (algo como: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Obtener el Chat ID

#### Opción A: Para un chat personal
1. Busca tu bot en Telegram y envíale cualquier mensaje
2. Visita en tu navegador:
   ```
   https://api.telegram.org/bot<TU_BOT_TOKEN>/getUpdates
   ```
   Reemplaza `<TU_BOT_TOKEN>` con el token que obtuviste de BotFather
3. Busca el campo `"chat":{"id":123456789}`
4. Ese número es tu Chat ID

#### Opción B: Para un grupo
1. Agrega tu bot al grupo de Telegram
2. Envía un mensaje en el grupo (puede ser cualquier cosa)
3. Visita en tu navegador:
   ```
   https://api.telegram.org/bot<TU_BOT_TOKEN>/getUpdates
   ```
4. Busca el `"chat":{"id":-123456789}` (nota el guión negativo para grupos)
5. Ese número es tu Chat ID del grupo

### 3. Configurar el archivo .env

Edita el archivo `src/.env` y agrega tus credenciales:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Environment (development o production)
ENV=production
```

**Importante:**
- En modo `development`, los PDFs se generan pero **NO** se envían a Telegram (solo se imprime en consola)
- En modo `production`, los PDFs se generan y **SÍ** se envían automáticamente a Telegram

### 4. Verificar la Instalación

Para probar que todo funciona, ejecuta:

```bash
python3 -c "from lib.Notification import DaltonismReportGenerator; print('✅ Módulo de notificaciones cargado correctamente')"
```

Si ves el mensaje de éxito, la configuración está lista.

## Uso

Una vez configurado, el sistema funcionará automáticamente:

1. Cuando un usuario complete el test de daltonismo
2. Se generará automáticamente un PDF con los resultados
3. El PDF se enviará al chat/grupo de Telegram configurado
4. El mensaje incluirá:
   - 📊 Icono indicativo
   - 📅 Fecha y hora del test
   - 📈 Puntuación general
   - 👤 ID del test
   - 📄 PDF adjunto con reporte completo

## Estructura del PDF

El PDF generado incluye:

### Sección de Información
- Fecha y hora del test
- ID del paciente/test

### Sección de Resultados
Tabla con:
- Test de Colores (correctas/total/porcentaje)
- Test de Ishihara (correctas/total/porcentaje)
- Total general

### Sección de Evaluación
- Diagnóstico según puntuación:
  - ≥85%: "Visión cromática normal" (verde)
  - 65-84%: "Posible deficiencia leve" (naranja)
  - <65%: "Se recomienda consulta oftalmológica" (rojo)
- Recomendaciones específicas

## Solución de Problemas

### El PDF no se envía a Telegram

1. Verifica que `ENV=production` en el archivo `.env`
2. Revisa que el token y chat ID sean correctos
3. Verifica que el bot tenga permisos para enviar mensajes al grupo
4. Revisa los logs en la consola para más detalles

### Error: "Notification module not available"

Instala las dependencias:
```bash
pip install python-telegram-bot reportlab python-dotenv
```

### El bot no responde

1. Asegúrate de haber iniciado el bot con `/start`
2. Si es un grupo, verifica que el bot sea administrador (o que el grupo permita que bots envíen mensajes)
3. Verifica que el token sea válido visitando:
   ```
   https://api.telegram.org/bot<TU_BOT_TOKEN>/getMe
   ```

## Seguridad

⚠️ **IMPORTANTE:**
- **NUNCA** compartas tu archivo `.env` 
- **NUNCA** subas el `.env` a GitHub u otros repositorios públicos
- El archivo `.env` está en `.gitignore` por defecto
- Si accidentalmente expones tu token, revócalo en @BotFather con `/revoke`

## Personalización

Puedes personalizar el PDF editando la función `generate_pdf_report()` en `src/lib/Notification.py`:

- Cambiar colores (líneas con `colors.HexColor('#XXXXXX')`)
- Modificar el diseño de la tabla
- Agregar más secciones
- Cambiar los umbrales de evaluación
- Modificar el estilo del texto

## Ejemplos de Uso

### Cambiar el umbral de evaluación

Edita en `Notification.py`:

```python
if overall_percentage >= 85:  # Cambiar este número
    evaluation = "Visión cromática normal"
```

### Agregar logo al PDF

En `generate_pdf_report()`, después del título:

```python
# Agregar logo
logo_path = "assets/images/logo.png"
if os.path.exists(logo_path):
    logo = Image(logo_path, width=2*inch, height=1*inch)
    story.append(logo)
    story.append(Spacer(1, 0.2*inch))
```

## Soporte

Si tienes problemas con la configuración:
1. Revisa los logs en la consola
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que el archivo `.env` esté en la ruta correcta (`src/.env`)
