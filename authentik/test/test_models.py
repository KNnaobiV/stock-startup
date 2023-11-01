from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class TestDefaultUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_user = User.objects.create(
            username='ennaobi', first_name='ekene', last_name='nnaobi',
            email='nnaobi.godson@gmail.com', password='Qwerty123',
            phone=2348183188758,
        )
        cls.second_user = User.objects.create(
            username='cnnaobi', first_name='Chike', last_name='nnaobi',
            email='nnaobi.godson@gmail.com', password='Qwerty123',
            phone=8183188758,
        )

    def test_user_string_method(self):
        user = User.objects.get(id=1)
        expected_result = 'ennaobi'
        self.assertEqual(expected_result, str(user))

    def test_phone_is_valid(self):
        user = User.objects.get(username='cnnaobi')
        self.assertRaises(ValidationError, user.full_clean)
