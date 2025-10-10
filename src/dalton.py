import tkinter as tk
from tkinter import ttk
import random
import time
import threading
from PIL import Image, ImageTk
import os
import glob
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("[ATENCION] GPIO no disponible - ejecutando sin sensor")

# Configuración del sensor ultrasónico
TRIG_PIN = 17
ECHO_PIN = 27
MIN_DISTANCE = 50  # Cambiado a 50 cm

# Configuración del servo motor MG996R
SERVO_PIN = 18  # GPIO18 (Pin físico 12)

# Colores básicos
colors = {
    "Rojo": "#FF0000",
    "Verde": "#00FF00", 
    "Azul": "#0000FF",
    "Amarillo": "#FFFF00",
    "Naranja": "#FFA500",
    "Morado": "#800080"
}

class IshiharaImageLoader:
    """Cargador de láminas Ishihara reales desde archivos"""
    
    def __init__(self, image_directory="."):
        self.image_directory = image_directory
        self.test_plates = self.load_real_plates()
        
    def load_real_plates(self):
        """Carga las láminas reales y define sus respuestas correctas"""
        # Definir respuestas correctas para cada imagen
        plates_config = {
            "12": {"correct": 12, "options": [12, 17, 21, "No veo nada"], "difficulty": "easy"},
            "13": {"correct": 13, "options": [13, 15, 18, "No veo nada"], "difficulty": "easy"}, 
            "16": {"correct": 16, "options": [16, 19, 18, "No veo nada"], "difficulty": "medium"},
            "29": {"correct": 29, "options": [29, 70, 20, "No veo nada"], "difficulty": "medium"},
            "42": {"correct": 42, "options": [42, 24, 74, "No veo nada"], "difficulty": "hard"},
            "5": {"correct": 5, "options": [5, 2, 8, "No veo nada"], "difficulty": "easy"},
            "74": {"correct": 74, "options": [74, 21, 71, "No veo nada"], "difficulty": "hard"},
            "8": {"correct": 8, "options": [8, 3, 6, "No veo nada"], "difficulty": "easy"}
        }
        
        loaded_plates = []
        
        for filename, config in plates_config.items():
            # Buscar archivos con diferentes extensiones
            for ext in ['png', 'jpg', 'jpeg']:
                image_path = os.path.join(self.image_directory, f"{filename}.{ext}")
                if os.path.exists(image_path):
                    try:
                        # Cargar y redimensionar imagen - Compacto para pantalla pequeña
                        img = Image.open(image_path)
                        img = img.resize((250, 250), Image.LANCZOS)  # Tamaño compacto para pantallas pequeñas
                        
                        plate_data = {
                            "filename": filename,
                            "image": img,
                            "correct_answer": config["correct"],
                            "options": config["options"].copy(),
                            "difficulty": config["difficulty"]
                        }
                        
                        # Mezclar opciones aleatoriamente
                        random.shuffle(plate_data["options"])
                        loaded_plates.append(plate_data)
                        print(f" Cargada lámina: {filename}.{ext}")
                        break
                    except Exception as e:
                        print(f" Error cargando {filename}.{ext}: {e}")
                        
        print(f" Total de láminas cargadas: {len(loaded_plates)}")
        return loaded_plates

class TestDaltonismoCompleto:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test de Daltonismo Completo")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="white")
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Optimizaciones para Raspberry Pi
        self.root.tk_setPalette(background='white', foreground='black')
        
        # Configurar para mejor rendimiento táctil
        self.root.configure(cursor="none")  # Ocultar cursor del mouse
        
        # Configuración de threading para mejor responsividad
        self.ui_update_delay = 50  # ms - delay reducido para mejor respuesta
        
        # Optimizaciones específicas para Raspberry Pi
        self.root.option_add('*tearOff', False)  # Deshabilitar tear-off menus
        self.root.resizable(False, False)  # Evitar redimensionamiento
        
        # Variables del test de colores
        self.color_attempts = 8
        self.color_attempt = 0
        self.color_score = 0
        self.current_color_name = ""
        
        # Variables del test de Ishihara
        print("[DEBUG] Inicializando cargador de imagenes Ishihara...")
        # Obtener ruta a las imágenes desde el directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_path = os.path.join(os.path.dirname(current_dir), "assets", "images")
        self.ishihara_loader = IshiharaImageLoader(images_path)
        print(f"[DEBUG] Laminas disponibles: {len(self.ishihara_loader.test_plates)}")
        self.ishihara_plates = self.ishihara_loader.test_plates[:6]  # Usar 6 láminas
        print(f"[DEBUG] Laminas seleccionadas para el test: {len(self.ishihara_plates)}")
        self.ishihara_attempts = len(self.ishihara_plates)
        self.ishihara_attempt = 0
        self.ishihara_score = 0
        self.current_ishihara_answer = None
        self.current_options = []
        
        # Variables del sensor
        self.user_nearby = False
        self.sensor_thread = None
        self.running = True
        self.current_test = "waiting"  # waiting, colors, ishihara, results
        
        # Variables UI
        self.color_buttons = {}
        self.option_buttons = []
        self.current_photo = None
        
        # Variable para control del servo
        self.servo_pwm = None
        self.current_servo_angle = 90  # Trackear posición actual
        
        # Configurar hardware
        self.setup_gpio()
        
        # Configurar UI
        self.setup_ui()
        
        # Iniciar sensor
        self.start_sensor_monitoring()
    
    def setup_gpio(self):
        """Configuración inicial del GPIO"""
        if GPIO_AVAILABLE:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(TRIG_PIN, GPIO.OUT)
                GPIO.setup(ECHO_PIN, GPIO.IN)
                GPIO.setup(SERVO_PIN, GPIO.OUT)  # Configurar pin del servo
                GPIO.output(TRIG_PIN, False)
                
                # Inicializar PWM para el servo
                self.servo_pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
                self.servo_pwm.start(0)
                
                # Posicionar servo en centro al inicio
                self.set_servo_angle(90)
                
                print("[OK] GPIO configurado correctamente (sensor + servo)")
            except Exception as e:
                print(f"[ERROR] Error configurando GPIO: {e}")
    
    def set_servo_angle(self, angle):
        """
        Mueve el servo al ángulo especificado
        angle: 0-180 grados
        """
        if not GPIO_AVAILABLE or self.servo_pwm is None:
            print(f"[SERVO-SIM] Simulando movimiento a {angle}°")
            self.current_servo_angle = angle  # Actualizar posición simulada
            return
            
        try:
            # Convertir ángulo a duty cycle
            # 0° = 2.5% duty cycle, 90° = 7.5% duty cycle, 180° = 12.5% duty cycle
            duty_cycle = 2.5 + (angle / 180.0) * 10.0
            self.servo_pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(1.0)  # Aumentado para movimiento más suave
            self.servo_pwm.ChangeDutyCycle(0)  # Detener señal PWM
            self.current_servo_angle = angle  # Actualizar posición actual
            print(f"[SERVO] Movido a {angle}°")
        except Exception as e:
            print(f"[ERROR] Error moviendo servo: {e}")
    
    def move_servo_result(self, satisfactory=True):
        """
        Mueve el servo según el resultado del test
        satisfactory: True = 90° derecha, False = 90° izquierda desde centro
        """
        print(f"[SERVO] Resultado: {'Satisfactorio' if satisfactory else 'Insatisfactorio'}")
        
        # Solo centrar si no está ya en centro
        if self.current_servo_angle != 90:
            print("[SERVO] Posicionando en centro")
            self.set_servo_angle(90)
            time.sleep(2)  # Más tiempo para posicionamiento
        else:
            print("[SERVO] Ya está en centro")
        
        if satisfactory:
            # Resultado satisfactorio - girar 90° a la derecha desde centro (90° → 180°)
            print("[SERVO] Girando 90° a la derecha desde centro")
            self.set_servo_angle(180)
        else:
            # Resultado insatisfactorio - girar 90° a la izquierda desde centro (90° → 0°)
            print("[SERVO] Girando 90° a la izquierda desde centro")
            self.set_servo_angle(0)
        
        # Esperar 2 segundos en la posición del resultado
        time.sleep(2)
        
        # Regresar a la posición original (centro)
        print("[SERVO] Regresando a posición original (centro)")
        self.set_servo_angle(90)
    
    def setup_ui(self):
        """Configuración de la interfaz de usuario"""
        # Frame superior para indicadores - Compacto para pantalla pequeña
        self.top_frame = tk.Frame(self.root, bg="#f0f0f0", height=80)
        self.top_frame.pack(fill=tk.X)
        self.top_frame.pack_propagate(False)
        
        # Indicador de proximidad - Optimizado para pantalla pequeña
        self.proximity_indicator = tk.Label(
            self.top_frame, text=" Esperando usuario...", font=("Arial", 18, "bold"),
            bg="#f0f0f0", fg="#FF5722"
        )
        self.proximity_indicator.pack(side=tk.LEFT, padx=15, pady=15)
        
        # Indicador de test actual - Compacto
        self.test_indicator = tk.Label(
            self.top_frame, text="", font=("Arial", 16, "bold"),
            bg="#f0f0f0", fg="#2196F3"
        )
        self.test_indicator.pack(pady=15)
        
        # Frame para test de colores
        self.setup_color_test_ui()
        
        # Frame para test de Ishihara
        self.setup_ishihara_test_ui()
        
        # Mostrar pantalla de espera inicial
        self.show_waiting_screen()
    
    def setup_color_test_ui(self):
        """Configura la UI para el test de colores"""
        self.main_frame = tk.Frame(self.root, bg="white")
        
        # Título del test - Compacto para pantalla pequeña
        self.test_title = tk.Label(
            self.main_frame, text=" Test de Colores Básicos", 
            font=("Arial", 28, "bold"),
            fg="#2196F3", bg="white"
        )
        self.test_title.pack(pady=15)
        
        # Texto principal - Tamaño moderado y legible
        self.label = tk.Label(
            self.main_frame, text="", font=("Arial", 36, "bold"),
            fg="black", bg="white"
        )
        self.label.pack(pady=20)
        
        # Contador - Tamaño compacto
        self.counter_label = tk.Label(
            self.main_frame, text="", font=("Arial", 20),
            fg="gray", bg="white"
        )
        self.counter_label.pack(pady=8)
        
        # Botones de colores
        self.buttons_frame = tk.Frame(self.main_frame, bg="white")
        self.buttons_frame.pack(pady=30)
        
        self.color_buttons = {}
        for color_name, hex_code in colors.items():
            btn = tk.Button(
                self.buttons_frame, bg=hex_code, width=8, height=3,
                command=lambda c=color_name: self.check_color_answer_with_animation(c),
                bd=3, relief="raised", activebackground=hex_code,
                cursor="hand2", font=("Arial", 12, "bold"), fg="white",
                text=color_name[:3].upper()  # Mostrar las primeras 3 letras del color
            )
            btn.pack(side=tk.LEFT, padx=15, pady=15)
            self.color_buttons[color_name] = btn
            self.add_color_button_effects(btn, hex_code)
    
    def setup_ishihara_test_ui(self):
        """Configura la UI para el test de Ishihara"""
        self.ishihara_frame = tk.Frame(self.root, bg="white")
        
        # Título del test - Compacto para pantalla pequeña
        self.ishihara_title = tk.Label(
            self.ishihara_frame, text=" Test de Láminas Ishihara", 
            font=("Arial", 26, "bold"),
            fg="#FF5722", bg="white"
        )
        self.ishihara_title.pack(pady=12)
        
        # Instrucciones - Tamaño moderado
        self.ishihara_instructions = tk.Label(
            self.ishihara_frame, 
            text="¿Qué número ves?", 
            font=("Arial", 20, "bold"),
            fg="#333", bg="white"
        )
        self.ishihara_instructions.pack(pady=8)
        
        # Contador Ishihara - Compacto
        self.ishihara_counter = tk.Label(
            self.ishihara_frame, text="", font=("Arial", 18),
            fg="gray", bg="white"
        )
        self.ishihara_counter.pack(pady=8)
        
        # Frame principal horizontal (imagen izquierda, botones derecha)
        self.content_frame = tk.Frame(self.ishihara_frame, bg="white")
        self.content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Configurar el content_frame como grid
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Frame para la imagen (lado izquierdo)
        self.image_frame = tk.Frame(self.content_frame, bg="white")
        self.image_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Imagen de la lámina
        self.ishihara_image_label = tk.Label(
            self.image_frame, bg="white", relief="solid", bd=2
        )
        self.ishihara_image_label.pack(expand=True)
        
        # Frame para botones de opción múltiple (lado derecho)
        self.options_frame = tk.Frame(self.content_frame, bg="white")
        self.options_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Los botones se crearán dinámicamente para cada lámina
        self.option_buttons = []
    
    def show_waiting_screen(self):
        """Muestra pantalla de espera"""
        self.current_test = "waiting"
        self.main_frame.pack_forget()
        self.ishihara_frame.pack_forget()
        
        self.test_indicator.config(text=" Acércate al sensor para iniciar")
    
    def start_color_test(self):
        """Inicia el test de colores"""
        if not self.user_nearby:
            return
            
        self.current_test = "colors"
        self.test_indicator.config(text=" Test de Colores (Parte 1/2)")
        
        # Mostrar frame de colores
        self.ishihara_frame.pack_forget()
        self.main_frame.pack(expand=True)
        
        # Resetear variables
        self.color_attempt = 0
        self.color_score = 0
        
        # Comenzar primera ronda
        self.next_color_round()
    
    def next_color_round(self):
        """Siguiente ronda del test de colores"""
        if not self.user_nearby:
            self.show_waiting_screen()
            return
            
        if self.color_attempt >= self.color_attempts:
            # Terminar test de colores, comenzar Ishihara
            self.start_ishihara_test()
            return
        
        # Seleccionar color aleatorio
        self.current_color_name = random.choice(list(colors.keys()))
        color_hex = colors[self.current_color_name]
        
        # Actualizar UI
        self.label.config(text=f"Selecciona el color:", fg="black")
        counter_text = f"Pregunta {self.color_attempt + 1} de {self.color_attempts}"
        self.counter_label.config(text=counter_text)
        
        # Animar texto principal
        self.animate_text_fade(self.label, f"Selecciona: {self.current_color_name}")
        self.pulse_counter(self.counter_label)
    
    def start_ishihara_test(self):
        """Inicia el test de Ishihara"""
        print(f"[DEBUG] Iniciando test Ishihara...")
        print(f"[DEBUG] Cantidad de laminas cargadas: {len(self.ishihara_plates)}")
        
        if not self.ishihara_plates:
            print("[ERROR] No hay laminas Ishihara cargadas!")
            self.show_final_results()
            return
            
        print(f"[DEBUG] Cambiando a test Ishihara con {len(self.ishihara_plates)} laminas")
        self.current_test = "ishihara"
        self.test_indicator.config(text="[ISHIHARA] Test Ishihara (Parte 2/2)")
        
        # Cambiar a frame de Ishihara
        self.main_frame.pack_forget()
        self.ishihara_frame.pack(expand=True)
        
        # Resetear variables
        self.ishihara_attempt = 0
        self.ishihara_score = 0
        
        # Empezar primera lámina
        self.next_ishihara_round()
    
    def next_ishihara_round(self):
        """Siguiente ronda del test de Ishihara"""
        if not self.user_nearby:
            self.show_waiting_screen()
            return
            
        if self.ishihara_attempt >= self.ishihara_attempts:
            self.show_final_results()
            return
        
        # Actualizar contador
        counter_text = f"Lámina {self.ishihara_attempt + 1} de {self.ishihara_attempts}"
        self.ishihara_counter.config(text=counter_text)
        
        # Mostrar lámina actual
        current_plate = self.ishihara_plates[self.ishihara_attempt]
        self.current_ishihara_answer = current_plate["correct_answer"]
        self.current_options = current_plate["options"]
        
        # Mostrar imagen
        img = current_plate["image"]
        self.current_photo = ImageTk.PhotoImage(img)
        self.ishihara_image_label.config(image=self.current_photo)
        
        # Crear botones de opciones
        self.create_option_buttons()
    
    def create_option_buttons(self):
        """Crea los botones de opción múltiple para Ishihara"""
        # Limpiar botones anteriores
        for btn in self.option_buttons:
            btn.destroy()
        self.option_buttons.clear()
        
        # Limpiar el frame de opciones
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Configurar el options_frame para centrar contenido
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(2, weight=1)
        self.options_frame.grid_rowconfigure(3, weight=1)
        self.options_frame.grid_rowconfigure(4, weight=1)
        self.options_frame.grid_columnconfigure(0, weight=1)
        
        # Título para los botones
        title_label = tk.Label(
            self.options_frame, 
            text="Selecciona una opción:",
            font=("Segoe UI", 18, "bold"),
            fg="#FF5722", bg="white"
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Colores para los botones
        button_colors = ["#E3F2FD", "#E8F5E8", "#FFF3E0", "#FCE4EC"]
        
        # Crear botones compactos para pantalla pequeña
        for i, option in enumerate(self.current_options):
            btn = tk.Button(
                self.options_frame, 
                text=str(option), 
                font=("Arial", 16, "bold"),  # Tamaño moderado
                width=12, height=2,  # Botones compactos
                bg=button_colors[i % len(button_colors)], 
                fg="#1976D2" if option != "No veo nada" else "#FF5722",
                relief="raised", bd=3, cursor="hand2",
                command=lambda opt=option: self.check_ishihara_answer(opt)
            )
            btn.grid(row=i+1, column=0, pady=6, padx=10, sticky="ew")  # Espaciado compacto
            self.option_buttons.append(btn)
            
            # Añadir efectos hover
            self.add_option_button_hover(btn, button_colors[i % len(button_colors)])
    
    def add_option_button_hover(self, button, normal_color):
        """Añade efecto hover a los botones de opción"""
        def on_enter(e):
            button.config(bg="#BBDEFB", relief="solid")
        
        def on_leave(e):
            button.config(bg=normal_color, relief="raised")
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def check_ishihara_answer(self, chosen_answer):
        """Verifica respuesta del test de Ishihara"""
        if not self.user_nearby or self.current_test != "ishihara":
            return
        
        # Verificar respuesta
        if chosen_answer == self.current_ishihara_answer:
            self.ishihara_score += 1
        
        # Efecto visual en el botón seleccionado
        for btn in self.option_buttons:
            if btn['text'] == str(chosen_answer):
                if chosen_answer == self.current_ishihara_answer:
                    btn.config(bg="#4CAF50", fg="white")  # Verde para correcto
                else:
                    btn.config(bg="#F44336", fg="white")  # Rojo para incorrecto
                self.animate_button_press(btn)
                break
        
        # Avanzar a siguiente lámina
        self.ishihara_attempt += 1
        self.root.after(1500, self.next_ishihara_round)
    
    def check_color_answer_with_animation(self, chosen_color):
        """Verifica respuesta del test de colores con animación"""
        if not self.user_nearby or self.current_test != "colors":
            return
        
        # Verificar respuesta
        if chosen_color == self.current_color_name:
            self.color_score += 1
        
        # Efecto visual
        btn = self.color_buttons[chosen_color]
        original_bg = btn['bg']
        
        if chosen_color == self.current_color_name:
            btn.config(relief="solid", bd=5)
        else:
            btn.config(bg="#FF6B6B", relief="solid", bd=5)
        
        self.animate_button_press(btn)
        
        # Restaurar estado original - Más rápido para Raspberry Pi
        self.root.after(400, lambda: btn.config(bg=original_bg, relief="raised", bd=3))
        
        # Avanzar - Delay reducido para mejor fluidez
        self.color_attempt += 1
        self.root.after(600, self.next_color_round)
    
    def show_final_results(self):
        """Muestra los resultados finales"""
        self.current_test = "results"
        self.main_frame.pack_forget()
        self.ishihara_frame.pack_forget()
        
        # Frame de resultados
        results_frame = tk.Frame(self.root, bg="white")
        results_frame.pack(expand=True)
        
        # Título - Compacto para pantalla pequeña
        title = tk.Label(
            results_frame, text=" Resultados del Test", 
            font=("Arial", 32, "bold"),
            fg="#2196F3", bg="white"
        )
        title.pack(pady=20)
        
        # Resultados del test de colores - Compacto
        color_percentage = (self.color_score / self.color_attempts) * 100
        color_result = tk.Label(
            results_frame, 
            text=f" Colores: {self.color_score}/{self.color_attempts} ({color_percentage:.1f}%)",
            font=("Arial", 20, "bold"), fg="#4CAF50" if color_percentage >= 75 else "#FF5722",
            bg="white"
        )
        color_result.pack(pady=10)
        
        # Resultados del test de Ishihara - Compacto
        if self.ishihara_attempts > 0:
            ishihara_percentage = (self.ishihara_score / self.ishihara_attempts) * 100
            ishihara_result = tk.Label(
                results_frame,
                text=f" Ishihara: {self.ishihara_score}/{self.ishihara_attempts} ({ishihara_percentage:.1f}%)",
                font=("Arial", 20, "bold"), fg="#4CAF50" if ishihara_percentage >= 75 else "#FF5722",
                bg="white"
            )
            ishihara_result.pack(pady=10)
        
        # Evaluación general
        total_score = self.color_score + self.ishihara_score
        total_possible = self.color_attempts + self.ishihara_attempts
        overall_percentage = (total_score / total_possible) * 100 if total_possible > 0 else 0
        
        # CONTROL DEL SERVO SEGÚN RESULTADO
        is_satisfactory = overall_percentage >= 75  # Umbral para resultado satisfactorio
        print(f"[RESULTADO] Puntuacion: {overall_percentage:.1f}% - {'SATISFACTORIO' if is_satisfactory else 'INSATISFACTORIO'}")
        
        # Mover servo según resultado
        self.root.after(1000, lambda: self.move_servo_result(is_satisfactory))
        
        if overall_percentage >= 85:
            evaluation = "[OK] Vision cromatica normal"
            eval_color = "#4CAF50"
        elif overall_percentage >= 65:
            evaluation = "[ATENCION] Posible deficiencia leve"
            eval_color = "#FF9800"
        else:
            evaluation = "[ERROR] Se recomienda consulta oftalmologica"
            eval_color = "#F44336"
        
        # Evaluación final - Compacto pero legible
        eval_label = tk.Label(
            results_frame, text=evaluation,
            font=("Arial", 22, "bold"), fg=eval_color, bg="white"
        )
        eval_label.pack(pady=20)
        
        # Botón para reiniciar - Tamaño compacto
        restart_btn = tk.Button(
            results_frame, text=" Nuevo Test",
            font=("Arial", 18, "bold"), bg="#2196F3", fg="white",
            width=15, height=2, cursor="hand2",
            command=self.restart_test
        )
        restart_btn.pack(pady=25)
        
        # Actualizar indicador
        self.test_indicator.config(text=" Test Completado")
    
    def restart_test(self):
        """Reinicia todo el test"""
        # Resetear variables
        self.color_attempt = 0
        self.color_score = 0
        self.ishihara_attempt = 0
        self.ishihara_score = 0
        
        # Limpiar pantalla
        for widget in self.root.winfo_children():
            if widget != self.top_frame:
                widget.destroy()
        
        # Reconfigurar UI
        self.setup_color_test_ui()
        self.setup_ishihara_test_ui()
        
        # Volver a pantalla de espera
        self.show_waiting_screen()
    
    # Funciones de animación
    def animate_text_fade(self, widget, text, steps=10):
        """Anima el desvanecimiento del texto"""
        def fade_in(step=0):
            if step < steps:
                alpha = step / steps
                gray_value = int(255 * alpha)
                color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
                widget.config(fg=color, text=text)
                self.root.after(50, lambda: fade_in(step + 1))
            else:
                widget.config(fg="black")
        fade_in()
    
    def animate_button_press(self, button):
        """Anima el efecto de presión del botón - Optimizado para Raspberry Pi"""
        original_relief = button['relief']
        button.config(relief="sunken")
        self.root.after(100, lambda: button.config(relief=original_relief))  # Más rápido
    
    def pulse_counter(self, widget):
        """Efecto de pulso en el contador"""
        original_font = widget['font']
        widget.config(font=("Segoe UI", 26, "bold"))
        self.root.after(200, lambda: widget.config(font=original_font))
    
    def add_color_button_effects(self, button, color):
        """Añade efectos a los botones de colores"""
        def on_enter(e):
            button.config(relief="solid", bd=4)
        
        def on_leave(e):
            button.config(relief="raised", bd=3)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    # Funciones del sensor
    def get_distance(self):
        """Obtiene la distancia del sensor ultrasónico"""
        if not GPIO_AVAILABLE:
            return 50  # Simular usuario presente para pruebas
        
        try:
            GPIO.output(TRIG_PIN, True)
            time.sleep(0.00001)
            GPIO.output(TRIG_PIN, False)
            
            start_time = time.time()
            stop_time = time.time()
            
            while GPIO.input(ECHO_PIN) == 0:
                start_time = time.time()
            
            while GPIO.input(ECHO_PIN) == 1:
                stop_time = time.time()
            
            elapsed_time = stop_time - start_time
            distance = (elapsed_time * 34300) / 2
            
            return distance
        except:
            return 999
    
    def start_sensor_monitoring(self):
        """Inicia el monitoreo del sensor en un hilo separado"""
        def monitor():
            while self.running:
                try:
                    distance = self.get_distance()
                    was_nearby = self.user_nearby
                    self.user_nearby = distance < MIN_DISTANCE
                    
                    # Actualizar indicador de proximidad
                    if self.user_nearby != was_nearby:
                        self.root.after(0, self.update_proximity_indicator)
                    
                    # Si el usuario se acerca y estamos esperando, iniciar test
                    if self.user_nearby and not was_nearby and self.current_test == "waiting":
                        self.root.after(0, self.start_color_test)
                    
                    # Delay más corto para mejor responsividad
                    time.sleep(0.2 if self.user_nearby else 0.4)
                except:
                    time.sleep(1)
        
        if self.running:
            self.sensor_thread = threading.Thread(target=monitor, daemon=True)
            self.sensor_thread.start()
    
    def update_proximity_indicator(self):
        """Actualiza el indicador de proximidad"""
        if self.user_nearby:
            self.proximity_indicator.config(
                text=" Usuario detectado ", 
                fg="#4CAF50"
            )
        else:
            self.proximity_indicator.config(
                text=" Esperando usuario...", 
                fg="#FF5722"
            )
    
    def cleanup(self):
        """Limpia recursos al cerrar"""
        self.running = False
        if GPIO_AVAILABLE:
            # Detener PWM del servo
            if self.servo_pwm:
                self.servo_pwm.stop()
            GPIO.cleanup()
            print("[OK] GPIO y servo limpiados")
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.cleanup)
            self.root.mainloop()
        finally:
            self.cleanup()

if __name__ == "__main__":
    print(" Iniciando Test de Daltonismo Completo...")
    app = TestDaltonismoCompleto()
    app.run()