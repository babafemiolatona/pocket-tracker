from django.test import TestCase
from django.contrib.auth.models import User
from users.forms import UserRegisterForm
from users.forms import UserUpdateForm


class TestUserRegisterForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='12345'
        )
        self.form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',
        }

    def test_form_is_valid(self):
        form = UserRegisterForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_existing_email(self):
        self.form_data['email'] = 'test@example.com'
        form = UserRegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'],
                         ['This email address is already in use. '
                          'Please use a different email address.'])

    def test_form_is_invalid_with_mismatched_passwords(self):
        self.form_data['password2'] = 'differentpassword'
        form = UserRegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_is_invalid_with_missing_password(self):
        del self.form_data['password1']
        form = UserRegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_form_is_invalid_with_missing_password2(self):
        del self.form_data['password2']
        form = UserRegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_is_invalid_with_missing_email(self):
        del self.form_data['email']
        form = UserRegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_is_invalid_with_missing_username(self):
        del self.form_data['username']
        form = UserRegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_is_invalid_with_existing_username(self):
        self.form_data['username'] = 'testuser'
        form = UserRegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'],
            ['A user with that username already exists.']
        )

    def test_form_is_invalid_with_missing_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)


class TestUserUpdateForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.form_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
        }

    def test_form_is_valid(self):
        form = UserUpdateForm(data=self.form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_existing_username(self):
        User.objects.create_user(
            username='existinguser',
            email='existinguser@example.com'
        )
        self.form_data['username'] = 'existinguser'
        form = UserUpdateForm(data=self.form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'],
            ['A user with that username already exists.']
        )

    def test_form_is_invalid_with_existing_email(self):
        User.objects.create_user(
            username='existinguser',
            email='existinguser@example.com'
        )
        self.form_data['email'] = 'existinguser@example.com'
        form = UserUpdateForm(data=self.form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'],
                         ['This email address is already in use. '
                          'Please use a different email address.'])
