from django.test import TestCase
from django.contrib.auth.models import User
from tracker.models import Category, Expense, UserPreference


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), 'Test Category')


class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name='Test Category')
        self.expense = Expense.objects.create(
            user=self.user,
            description='Test Expense',
            amount=100.00,
            category='Food',
        )

    def test_expense_str_representation(self):
        self.assertEqual(str(self.expense), 'Food')


class UserPreferenceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.preference = UserPreference.objects.create(
            user=self.user,
            currency='USD'
        )

    def test_preference_str_representation(self):
        self.assertEqual(str(self.preference), "testusers preferences")
