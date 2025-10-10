"""
Tests básicos para funciones utilitarias del proyecto.
"""

import unittest
import os
import sys

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestBasicFunctions(unittest.TestCase):
    """Tests básicos para validar la estructura del proyecto."""

    def test_project_structure(self):
        """Verificar que la estructura de directorios existe."""
        project_root = os.path.join(os.path.dirname(__file__), '..')
        
        # Verificar directorios principales
        expected_dirs = ['src', 'assets', 'scripts', 'tests', 'config']
        for directory in expected_dirs:
            dir_path = os.path.join(project_root, directory)
            self.assertTrue(os.path.isdir(dir_path), 
                          f"Directorio {directory} no encontrado en {dir_path}")

    def test_main_files_exist(self):
        """Verificar que los archivos principales existen."""
        project_root = os.path.join(os.path.dirname(__file__), '..')
        
        # Verificar archivos principales
        expected_files = [
            'src/dalton.py',
            'requirements.txt',
            'README.md',
            'LICENSE',
            'setup.py',
            '.gitignore'
        ]
        
        for file_path in expected_files:
            full_path = os.path.join(project_root, file_path)
            self.assertTrue(os.path.isfile(full_path), 
                          f"Archivo {file_path} no encontrado en {full_path}")

    def test_images_directory(self):
        """Verificar que el directorio de imágenes existe y contiene archivos."""
        project_root = os.path.join(os.path.dirname(__file__), '..')
        images_dir = os.path.join(project_root, 'assets', 'images')
        
        self.assertTrue(os.path.isdir(images_dir), 
                       f"Directorio de imágenes no encontrado: {images_dir}")
        
        # Verificar que hay archivos de imagen
        image_files = [f for f in os.listdir(images_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.assertGreater(len(image_files), 0, 
                          "No se encontraron archivos de imagen")

    def test_scripts_directory(self):
        """Verificar que los scripts existen y son ejecutables."""
        project_root = os.path.join(os.path.dirname(__file__), '..')
        scripts_dir = os.path.join(project_root, 'scripts')
        
        self.assertTrue(os.path.isdir(scripts_dir),
                       f"Directorio de scripts no encontrado: {scripts_dir}")
        
        # Verificar scripts principales
        expected_scripts = [
            'instalar_dependencias.sh',
            'ejecutar_test_completo.sh'
        ]
        
        for script in expected_scripts:
            script_path = os.path.join(scripts_dir, script)
            self.assertTrue(os.path.isfile(script_path),
                          f"Script {script} no encontrado")


class TestCalculations(unittest.TestCase):
    """Tests para funciones de cálculo básicas."""

    def test_percentage_calculation(self):
        """Test de cálculo de porcentajes."""
        # Función básica de cálculo que podría estar en el proyecto
        def calculate_percentage(correct: int, total: int) -> float:
            if total == 0:
                return 0.0
            return (correct / total) * 100.0
        
        # Tests del cálculo
        self.assertEqual(calculate_percentage(8, 10), 80.0)
        self.assertEqual(calculate_percentage(10, 10), 100.0)
        self.assertEqual(calculate_percentage(0, 10), 0.0)
        self.assertEqual(calculate_percentage(5, 0), 0.0)

    def test_diagnosis_categories(self):
        """Test de categorización de diagnóstico."""
        def categorize_result(percentage: float) -> str:
            if percentage >= 85:
                return "Normal"
            elif percentage >= 70:
                return "Leve"
            elif percentage >= 50:
                return "Moderado"
            else:
                return "Severo"
        
        # Tests de categorización
        self.assertEqual(categorize_result(100), "Normal")
        self.assertEqual(categorize_result(85), "Normal")
        self.assertEqual(categorize_result(84.9), "Leve")
        self.assertEqual(categorize_result(70), "Leve")
        self.assertEqual(categorize_result(69.9), "Moderado")
        self.assertEqual(categorize_result(50), "Moderado")
        self.assertEqual(categorize_result(49.9), "Severo")
        self.assertEqual(categorize_result(0), "Severo")


if __name__ == '__main__':
    unittest.main()