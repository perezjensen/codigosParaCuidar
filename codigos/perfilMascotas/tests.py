from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from perfilMascotas import models

class VerificarNombreTest(TestCase):

    def setUp(self):
        # Crear un usuario para simular una sesión iniciada
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        # Crear un perfil asociado al usuario
        self.perfil = models.PerfilMascotas.objects.create(nombreDueno='Juan', cliente=self.user)
        self.session = self.client.session
        self.session['id_perfil'] = f'perfil/{self.perfil.id}'
        self.session.save()

    def test_verificar_nombre_correcto(self):
        """
        Verificar que cuando se introduce el nombre correcto, se redirige al perfil
        """
        nombre = 'Juan'
        response = self.client.post(reverse('verificarNombre'), {'nombre': nombre})
        self.assertRedirects(response, reverse('perfil', args=[self.perfil.id]))
        self.assertEqual(response.status_code, 302)