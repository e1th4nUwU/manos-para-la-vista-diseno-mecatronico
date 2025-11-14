#!/usr/bin/env python3
"""
Test script para buzzer de 3V conectado a Raspberry Pi GPIO

Conexión del Buzzer:
- Pin positivo (+) del buzzer -> GPIO Pin especificado (por defecto GPIO 23, Pin físico 16)
- Pin negativo (-) del buzzer -> GND (cualquier pin GND, ej: Pin físico 14)

Uso:
    python3 test_buzzer.py
    
Controles:
    - Presiona 1: Tono de éxito (agradable)
    - Presiona 2: Tono de fallo (descendente)
    - Presiona 3: Tono de alerta (intermitente)
    - Presiona 4: Tono continuo (prueba básica)
    - Presiona q: Salir
"""

import time
import sys

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("[ADVERTENCIA] RPi.GPIO no disponible - ejecutando en modo simulación")

# Configuración del buzzer
BUZZER_PIN = 23  # GPIO23 (Pin físico 16) - Cambia esto según tu conexión

class BuzzerTester:
    def __init__(self, pin=BUZZER_PIN):
        self.pin = pin
        self.pwm = None
        self.setup()
    
    def setup(self):
        """Configura el GPIO para el buzzer"""
        global GPIO_AVAILABLE
        if GPIO_AVAILABLE:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.pin, GPIO.OUT)
                self.pwm = GPIO.PWM(self.pin, 1000)  # Frecuencia base de 1000Hz
                print(f"✓ GPIO configurado correctamente en pin {self.pin}")
                print(f"  (Pin físico aproximado: {self.get_physical_pin()})")
            except Exception as e:
                print(f"✗ Error configurando GPIO: {e}")
                GPIO_AVAILABLE = False
        else:
            print("✓ Modo simulación activado")
    
    def get_physical_pin(self):
        """Obtiene el número de pin físico aproximado"""
        # Mapeo simplificado BCM -> Pin físico
        pin_map = {
            23: 16, 24: 18, 25: 22, 8: 24, 7: 26,
            12: 32, 16: 36, 20: 38, 21: 40
        }
        return pin_map.get(self.pin, "?")
    
    def beep(self, frequency, duration):
        """Emite un beep a una frecuencia específica por cierto tiempo"""
        if GPIO_AVAILABLE and self.pwm:
            try:
                self.pwm.ChangeFrequency(frequency)
                self.pwm.start(50)  # 50% duty cycle
                time.sleep(duration)
                self.pwm.stop()
            except Exception as e:
                print(f"✗ Error en beep: {e}")
        else:
            print(f"♪ BEEP: {frequency}Hz por {duration}s (simulado)")
            time.sleep(duration)
    
    def success_tone(self):
        """Tono de éxito - Melodía ascendente agradable"""
        print("▶ Reproduciendo tono de ÉXITO...")
        frequencies = [523, 659, 784, 1047]  # Do, Mi, Sol, Do alto
        for freq in frequencies:
            self.beep(freq, 0.15)
            time.sleep(0.05)
    
    def failure_tone(self):
        """Tono de fallo - Melodía descendente"""
        print("▶ Reproduciendo tono de FALLO...")
        frequencies = [800, 600, 400, 250]  # Descendente
        for freq in frequencies:
            self.beep(freq, 0.2)
            time.sleep(0.05)
    
    def alert_tone(self):
        """Tono de alerta - Beeps intermitentes"""
        print("▶ Reproduciendo tono de ALERTA...")
        for _ in range(3):
            self.beep(1500, 0.1)
            time.sleep(0.1)
    
    def continuous_tone(self, duration=2.0):
        """Tono continuo para prueba básica"""
        print(f"▶ Reproduciendo tono CONTINUO ({duration}s)...")
        self.beep(1000, duration)
    
    def cleanup(self):
        """Limpia los recursos GPIO"""
        if GPIO_AVAILABLE:
            if self.pwm:
                self.pwm.stop()
            GPIO.cleanup()
            print("\n✓ GPIO limpiado correctamente")

def print_menu():
    """Muestra el menú de opciones"""
    print("\n" + "="*50)
    print("     TEST DE BUZZER DE 3V - RASPBERRY PI")
    print("="*50)
    print(f"\nPin GPIO configurado: {BUZZER_PIN} (Pin físico ~16)")
    print("\nOpciones:")
    print("  [1] Tono de ÉXITO (melodía ascendente agradable)")
    print("  [2] Tono de FALLO (melodía descendente)")
    print("  [3] Tono de ALERTA (beeps intermitentes)")
    print("  [4] Tono CONTINUO (prueba básica de 2s)")
    print("  [q] SALIR")
    print("-"*50)

def main():
    """Función principal del test"""
    print("\n🔊 Iniciando test de buzzer...")
    print("\nConexiones requeridas:")
    print(f"  • Buzzer (+) -> GPIO {BUZZER_PIN} (Pin físico ~16)")
    print("  • Buzzer (-) -> GND (ej: Pin físico 14)")
    
    buzzer = BuzzerTester(BUZZER_PIN)
    
    try:
        while True:
            print_menu()
            choice = input("\nSelecciona una opción: ").strip().lower()
            
            if choice == '1':
                buzzer.success_tone()
            elif choice == '2':
                buzzer.failure_tone()
            elif choice == '3':
                buzzer.alert_tone()
            elif choice == '4':
                buzzer.continuous_tone(2.0)
            elif choice == 'q':
                print("\n👋 Saliendo del test...")
                break
            else:
                print("✗ Opción no válida. Intenta de nuevo.")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupción detectada (Ctrl+C)")
    
    finally:
        buzzer.cleanup()
        print("✓ Test finalizado\n")

if __name__ == "__main__":
    main()
