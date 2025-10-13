from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Categoria

User = get_user_model()

class HiloTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="coke", password="1234", is_active=True)
        self.categoria = Categoria.objects.create(nombre="Bugs")
        self.client.force_authenticate(user=self.user)

    def crear_hilo(self, titulo="Título válido", categoria_id=None):
        if categoria_id is None:
            categoria_id = self.categoria.id
        data = {
            "titulo": titulo,
            "contenido": "Contenido del hilo",
            "usuario": self.user.id,
            "categoria": categoria_id
        }
        return self.client.post("/api/hilos/", data, format="json")

    def test_crear_hilo_valido(self):
        response = self.crear_hilo()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["titulo"], "Título válido")
        self.assertEqual(response.data["usuario"], self.user.id)
        self.assertEqual(response.data["categoria"], self.categoria.id)

    def test_crear_hilo_invalido(self):
        response = self.crear_hilo(titulo="Título inválido", categoria_id="")
        self.assertEqual(response.status_code, 400)
        self.assertIn("categoria", response.data)

    def test_cambiar_categoria(self):
        hilo_response = self.crear_hilo(titulo="Hilo para cambiar categoría")
        hilo_id = hilo_response.data["id"]

        nueva_categoria = Categoria.objects.create(nombre="Sugerencias")
        url = f"/api/hilos/{hilo_id}/cambiar-categoria/"
        
        response = self.client.put(url, {"categoria_id": nueva_categoria.id}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["categoria"], nueva_categoria.id)
        self.assertEqual(response.data["categoria_info"]["nombre"], "Sugerencias")

        response_invalid = self.client.put(url, {"categoria_id": 9999}, format="json")
        self.assertEqual(response_invalid.status_code, 404)
