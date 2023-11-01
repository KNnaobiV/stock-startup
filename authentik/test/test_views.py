from django.test import TestCase, Client
from auth import views
from django.contrib.auth import get_user_model
from auth.services import forms
from django.shortcuts import reverse
from django.urls import reverse_lazy

User = get_user_model()
client = Client()
class TestUserCreation(TestCase):
    @classmethod
    def setUpTestData(cls):
        form = forms.MyUserCreationForm(data={
            'phone': 48183188758, 'first_name': 'Ekene', 'last_name': 'Nnaobi',
            'username': 'ennaobi', 'password1': 'TestpassworD1', 
            'password2': 'TestpassworD1', 'email': 'nnaobi.godson@gmail.com'
            }
        )

        invalid_form = forms.MyUserCreationForm(data={
            'phone': 48183188758, 'first_name': 'Ekene', 'last_name': 'Nnaobi',
            'username': 'ennaobi', 'password1': 'TestpassworD1', 
            'password2': 'TestpassworD1', 'email': 'nnaobi.godson@gmail.com'
            }
        )
 
    def test_register_page(self):
        response = client.get(reverse('auth:register'))
        self.assertEqual(response.status_code, 200)


class TestLoginProcess(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='ennaobi', first_name='ekene', last_name='nnaobi',
            email='nnaobi.godson@gmail.com', password='Qwerty123',
            phone=48183188758,
        )
        # urls = '/management/auth/urls'

    def test_login(self):
        response= client.login(username='ennaobi', password='Qwerty123')
        self.assertTrue(response)

    def test_unregistered_user_login(self):
        response = client.login(username='cnnaobi', password='Qwerty123')
        self.assertFalse(response)

'''    def test_login_redirects_to_profile(self):

        response = client.get(reverse('auth:login'), 
            {'username':'ennaobi', 'password':'Qwerty123'}
            )
        url = reverse('auth:profile')
        self.assertRedirects(
            response, reverse('auth:login' + f'?next={url}', kwargs={'pk': 1, 'id': 1}),
            )'''
