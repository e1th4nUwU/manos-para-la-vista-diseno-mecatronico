# Makefile para Daltonismo Test System

.PHONY: help install dev-install test lint format clean build run docs

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
SRC_DIR := src
TEST_DIR := tests

help:  ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar dependencias básicas
	$(PIP) install -r requirements.txt

dev-install:  ## Configurar entorno de desarrollo
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install --upgrade pip
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt
	. $(VENV)/bin/activate && $(PIP) install -e ".[dev]"

test:  ## Ejecutar tests
	$(PYTHON) -m pytest $(TEST_DIR) -v --cov=$(SRC_DIR)

lint:  ## Ejecutar linting
	flake8 $(SRC_DIR) $(TEST_DIR)
	pylint $(SRC_DIR)

format:  ## Formatear código
	black $(SRC_DIR) $(TEST_DIR)

clean:  ## Limpiar archivos generados
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage

build:  ## Crear ejecutable con PyInstaller
	. $(VENV)/bin/activate && pyinstaller config/dalton.spec

run:  ## Ejecutar la aplicación principal
	$(PYTHON) $(SRC_DIR)/dalton.py

run-rpi:  ## Ejecutar en Raspberry Pi con privilegios GPIO
	sudo $(PYTHON) $(SRC_DIR)/dalton.py

docs:  ## Generar documentación
	@echo "Generando documentación..."
	@echo "README.md ya contiene la documentación principal"

setup-rpi:  ## Configurar Raspberry Pi (requiere sudo)
	sudo apt update
	sudo apt install -y python3-pip python3-tk python3-pil python3-pil.imagetk python3-numpy python3-rpi.gpio
	chmod +x scripts/*.sh

check:  ## Verificar configuración del sistema
	@echo "Verificando Python..."
	@$(PYTHON) --version
	@echo "Verificando dependencias..."
	@$(PYTHON) -c "import tkinter, PIL, numpy; print('✓ Dependencias básicas OK')"
	@$(PYTHON) -c "import RPi.GPIO; print('✓ RPi.GPIO disponible')" 2>/dev/null || echo "⚠ RPi.GPIO no disponible (normal en sistemas no-RPi)"

# Comandos para CI/CD
ci-test:  ## Tests para CI/CD
	$(PYTHON) -m pytest $(TEST_DIR) -v --cov=$(SRC_DIR) --cov-report=xml

ci-lint:  ## Linting para CI/CD
	flake8 $(SRC_DIR) $(TEST_DIR) --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 $(SRC_DIR) $(TEST_DIR) --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics