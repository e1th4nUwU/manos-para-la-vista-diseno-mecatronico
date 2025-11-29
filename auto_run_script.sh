#!/bin/bash
## Script para ejecutar el programa automáticamente al iniciar la Raspberry Pi
# Coloca este script en ~/.xsessionrc o en /etc/xdg/lxsession/LXDE-pi/autostart
# Asegúrate de que el script tenga permisos de ejecución: chmod +x auto_run_script.sh

# Ejecutar el programa
@python3 <ruta-al-repo>/src/dalton.py