from django.test import TestCase
from auth.services.forms import UserEditForm, MyUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserCreationForm(TestCase):

    def test_user_creation_form_fields(self):
        form = MyUserCreationForm(data={
            'phone': 2348183188758, 'first_name': 'Ekene', 'last_name': 'Nnaobi',
            'username': 'ennaobi', 'password1': 'TestpassworD1', 
            'password2': 'TestpassworD1', 'email': 'nnaobi.godson@gmail.com'
            })
        print(form.errors)
        self.assertTrue(form.is_valid())
    
    def test_phone_less_than_length(self):
        form = MyUserCreationForm(data={
            'phone': 8183188758, 'first_name': 'Ekene', 'last_name': 'Nnaobi',
            'username': 'ennaobi', 'password1': 'TestpassworD1', 
            'password2': 'TestpassworD1', 'email': 'nnaobi.godson@gmail.com'
            })
        print(form.errors)
        self.assertFalse(form.is_valid())

    def test_phone_greater_than_length(self):
        form = MyUserCreationForm(data={
            'phone': 23481831887585, 'first_name': 'Ekene', 'last_name': 'Nnaobi',
            'username': 'ennaobi', 'password1': 'TestpassworD1', 
            'password2': 'TestpassworD1', 'email': 'nnaobi.godson@gmail.com'
            })
        print(form.errors)
        self.assertFalse(form.is_valid())