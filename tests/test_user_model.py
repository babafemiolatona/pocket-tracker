from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.profile.user.username, 'testuser')

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser Profile')

    def test_profile_delete(self):
        self.profile.delete()
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(User.objects.count(), 1)

    def test_profile_update(self):
        self.profile.user.username = 'newusername'
        self.profile.save()
        self.assertEqual(self.profile.user.username, 'newusername')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_profile_update_username(self):
        self.profile.user.username = 'newusername'
        self.profile.save()
        self.assertEqual(self.profile.user.username, 'newusername')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_profile_update_password(self):
        self.profile.user.set_password('newpassword')
        self.profile.user.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertTrue(self.profile.user.check_password('newpassword'))
        self.assertFalse(self.profile.user.check_password('testpassword'))
