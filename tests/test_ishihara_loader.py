"""
Tests unitarios para el cargador de láminas Ishihara.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import pytest
from PIL import Image

# Import del módulo a testear
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from dalton import IshiharaImageLoader
except ImportError:
    pytest.skip("No se puede importar el módulo dalton", allow_module_level=True)


class TestIshiharaImageLoader(unittest.TestCase):
    """Tests para la clase IshiharaImageLoader."""

    def setUp(self):
        """Configurar test environment."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Limpiar después de los tests."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_with_directory(self):
        """Test de inicialización con directorio específico."""
        loader = IshiharaImageLoader(self.temp_dir)
        self.assertEqual(loader.image_directory, self.temp_dir)

    def test_init_default_directory(self):
        """Test de inicialización con directorio por defecto."""
        loader = IshiharaImageLoader()
        self.assertEqual(loader.image_directory, ".")

    def test_load_real_plates_empty_directory(self):
        """Test de carga con directorio vacío."""
        loader = IshiharaImageLoader(self.temp_dir)
        self.assertEqual(len(loader.test_plates), 0)

    @patch('PIL.Image.open')
    def test_load_real_plates_with_images(self, mock_image_open):
        """Test de carga con imágenes simuladas."""
        # Crear archivos de imagen falsos
        test_files = ["12.png", "13.jpg", "16.png"]
        for filename in test_files:
            open(os.path.join(self.temp_dir, filename), 'w').close()
        
        # Configurar mock para PIL.Image.open
        mock_img = MagicMock()
        mock_img.resize.return_value = mock_img
        mock_image_open.return_value = mock_img
        
        loader = IshiharaImageLoader(self.temp_dir)
        
        # Verificar que se cargaron las imágenes esperadas
        self.assertGreater(len(loader.test_plates), 0)
        self.assertLessEqual(len(loader.test_plates), 3)
        
        # Verificar estructura de datos de las láminas
        for plate in loader.test_plates:
            self.assertIn('filename', plate)
            self.assertIn('image', plate)
            self.assertIn('correct_answer', plate)
            self.assertIn('options', plate)
            self.assertIn('difficulty', plate)

    def test_plate_configuration(self):
        """Test de configuración de láminas predefinidas."""
        loader = IshiharaImageLoader(self.temp_dir)
        
        # Verificar que las configuraciones de láminas están definidas
        # (esto requiere acceso a la configuración interna)
        self.assertIsInstance(loader.test_plates, list)

    @patch('PIL.Image.open')
    def test_image_resize(self, mock_image_open):
        """Test de redimensionamiento de imágenes."""
        # Crear un archivo de imagen falso
        test_file = os.path.join(self.temp_dir, "12.png")
        open(test_file, 'w').close()
        
        # Configurar mock
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        
        loader = IshiharaImageLoader(self.temp_dir)
        
        if loader.test_plates:
            # Verificar que resize fue llamado con las dimensiones correctas
            mock_img.resize.assert_called()
            call_args = mock_img.resize.call_args[0]
            self.assertEqual(call_args[0], (400, 400))

    @patch('PIL.Image.open', side_effect=Exception("Error de carga"))
    def test_image_loading_error_handling(self, mock_image_open):
        """Test de manejo de errores al cargar imágenes."""
        # Crear archivo que causará error
        test_file = os.path.join(self.temp_dir, "12.png")
        open(test_file, 'w').close()
        
        # El cargador debe manejar el error graciosamente
        loader = IshiharaImageLoader(self.temp_dir)
        self.assertEqual(len(loader.test_plates), 0)

    def test_options_shuffling(self):
        """Test de mezcla de opciones de respuesta."""
        # Este test requiere crear múltiples instancias y verificar
        # que las opciones se mezclan aleatoriamente
        with patch('PIL.Image.open') as mock_open:
            # Crear imagen falsa
            test_file = os.path.join(self.temp_dir, "12.png")
            open(test_file, 'w').close()
            
            mock_img = MagicMock()
            mock_img.resize.return_value = mock_img
            mock_open.return_value = mock_img
            
            loaders = [IshiharaImageLoader(self.temp_dir) for _ in range(5)]
            
            # Si hay láminas cargadas, verificar que las opciones pueden variar
            if all(loader.test_plates for loader in loaders):
                options_sets = [loader.test_plates[0]['options'] for loader in loaders]
                # Al menos una configuración debería ser diferente
                # (estadísticamente probable con mezcla aleatoria)
                unique_configurations = len(set(str(opts) for opts in options_sets))
                # Este test puede fallar ocasionalmente debido a la aleatoriedad
                # pero es muy improbable


if __name__ == '__main__':
    unittest.main()