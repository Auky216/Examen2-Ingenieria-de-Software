import unittest
import json
from app import app, get_db_connection

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Se ejecuta una vez antes de todas las pruebas."""
        cls.app = app.test_client()
        cls.app.testing = True

    @classmethod
    def tearDownClass(cls):
        """Se ejecuta una vez después de todas las pruebas."""
        pass

    # Prueba de éxito para obtener los contactos de un usuario
    def test_get_contactos_success(self):
        """Caso de prueba: Obtener los contactos de un usuario"""
        response = self.app.get('/mensajeria/contactos?mialias=cpaz')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('lmunoz', data)  # Asegurarse que lmunoz esté en los contactos
        self.assertIn('mgrau', data)   # Asegurarse que mgrau esté en los contactos

    # Prueba de éxito para agregar un nuevo contacto
    def test_add_contact_success(self):
        """Caso de prueba: Agregar un contacto correctamente"""
        payload = {
            'contacto': 'juanperez',
            'nombre': 'Juan Pérez'
        }
        response = self.app.post('/mensajeria/contactos/cpaz', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Contacto añadido correctamente")

    # Prueba de éxito para enviar un mensaje
    def test_send_message_success(self):
        """Caso de prueba: Enviar un mensaje correctamente"""
        payload = {
            'usuario': 'cpaz',
            'contacto': 'lmunoz',
            'mensaje': 'Hola Luisa'
        }
        response = self.app.post('/mensajeria/enviar', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Mensaje enviado correctamente")

    # Prueba de éxito para obtener los mensajes recibidos
    def test_get_received_messages_success(self):
        """Caso de prueba: Obtener los mensajes recibidos correctamente"""
        response = self.app.get('/mensajeria/recibidos?mialias=lmunoz')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)  # Debería haber al menos un mensaje

    # Caso de error: Falta el parámetro 'mialias' al obtener contactos
    def test_get_contactos_error_missing_mialias(self):
        """Caso de prueba: Error al obtener contactos, falta 'mialias'"""
        response = self.app.get('/mensajeria/contactos')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Falta el parámetro 'mialias'")

    # Caso de error: Intentar agregar un contacto sin el parámetro 'contacto'
    def test_add_contact_error_missing_contact(self):
        """Caso de prueba: Error al agregar contacto, falta 'contacto'"""
        payload = {
            'nombre': 'Juan Pérez'
        }
        response = self.app.post('/mensajeria/contactos/cpaz', json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Falta el parámetro 'contacto'")

    # Caso de error: Intentar enviar un mensaje sin parámetros correctos
    def test_send_message_error_missing_params(self):
        """Caso de prueba: Error al enviar mensaje, falta un parámetro"""
        payload = {
            'usuario': 'cpaz',
            'mensaje': 'Hola'
        }
        response = self.app.post('/mensajeria/enviar', json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Faltan parámetros")

if __name__ == '__main__':
    unittest.main()
