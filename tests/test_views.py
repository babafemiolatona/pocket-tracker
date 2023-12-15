from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tracker.models import Category, Expense, UserPreference
from datetime import datetime
from django.utils import timezone
from tracker.models import Expense
import json


class CreateExpenseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.create_expense_url = reverse('tracker:create-expense')

    def test_create_expense_view(self):
        response = self.client.get(self.create_expense_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_static/create_expense.html')

    def test_create_expense_post_request(self):
        response = self.client.post(self.create_expense_url, {
            'description': 'Test Expense',
            'amount': 100.00,
            'category': 'Food',
            'date_of_expense': timezone.now().date()
        })
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.first().description, 'Test Expense')

    def test_create_expense_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.create_expense_url)
        self.assertEqual(response.status_code, 302)


class ExpenseUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        self.expense = Expense.objects.create(
            user=self.user,
            description='Test Expense',
            amount=100.00,
            category='Food',
            date_of_expense=timezone.now().date()
        )
        self.update_expense_url = reverse(
            'tracker:expense-edit',
            kwargs={'pk': self.expense.pk}
        )

    def test_expense_update_view(self):
        response = self.client.get(self.update_expense_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_static/edit_expense.html')

    def test_expense_update_post_request(self):
        response = self.client.post(self.update_expense_url, {
            'description': 'Updated Expense',
            'amount': 200.00,
            'category': 'Travel',
            'date_of_expense': timezone.now().date()
        })
        self.expense.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.expense.description, 'Updated Expense')
        self.assertEqual(self.expense.amount, 200.00)
        self.assertEqual(self.expense.category, 'Travel')

    def test_expense_update_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.update_expense_url)
        self.assertEqual(response.status_code, 302)


class ExpenseListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.expense = Expense.objects.create(
            user=self.user,
            description='Test Expense',
            amount=100.00,
            category=self.category,
            date_of_expense=datetime.now()
        )
        self.preference = UserPreference.objects.create(
            user=self.user,
            currency='USD'
        )
        self.expense_list_url = reverse('tracker:expenses')

    def test_expense_list_view(self):
        response = self.client.get(self.expense_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_static/index.html')

    def test_expense_list_context_data(self):
        response = self.client.get(self.expense_list_url)
        self.assertEqual(response.context['expenses'].count(), 1)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
        self.assertEqual(response.context['currency'], 'USD')

    def test_expense_list_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.expense_list_url)
        self.assertEqual(response.status_code, 302)


class ExpenseDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.expense = Expense.objects.create(
            user=self.user,
            description='Test Expense',
            amount=100.00,
            category='Food',
            date_of_expense=timezone.now().date()
        )
        self.delete_expense_url = reverse(
            'tracker:expense-delete',
            kwargs={'pk': self.expense.pk}
        )

    def test_expense_delete_view(self):
        response = self.client.get(self.delete_expense_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_static/expense_delete.html')

    def test_expense_delete_post_request(self):
        response = self.client.post(self.delete_expense_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 0)

    def test_expense_delete_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.delete_expense_url)
        self.assertEqual(response.status_code, 302)


class StatsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.stats_url = reverse('tracker:stats')

    def test_stats_view(self):
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_static/stats.html')

    def test_stats_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, 302)


class SearchExpensesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.expense = Expense.objects.create(
            user=self.user,
            description='Test Expense',
            amount=100.00,
            category='Food',
            date_of_expense=timezone.now().date()
        )
        self.search_expenses_url = reverse('tracker:search-expenses')

    def test_search_expenses_view(self):
        response = self.client.post(
            self.search_expenses_url,
            json.dumps({'searchText': 'Test'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Expense')


class PreferenceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.preference_url = reverse('tracker:preference')

    def test_preference_view_get(self):
        response = self.client.get(self.preference_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_static/preference.html')

    def test_preference_view_post(self):
        response = self.client.post(self.preference_url, {'currency': 'USD'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Changes saved')


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.expense = Expense.objects.create(
            user=self.user,
            description='Test Expense',
            amount=100.00,
            category=self.category,
            date_of_expense=datetime.now()
        )
        self.preference = UserPreference.objects.create(
            user=self.user,
            currency='USD'
        )
        self.dashboard_url = reverse('tracker:dashboard')

    def test_dashboard_view(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_static/dashboard.html')

    def test_dashboard_context_data(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.context['expenses'].count(), 1)
        self.assertEqual(response.context['expenses_this_year'].count(), 1)
        self.assertEqual(response.context['expenses_this_month'].count(), 1)
        self.assertEqual(response.context['total_this_year'], 100.00)
        self.assertEqual(response.context['total_this_month'], 100.00)
        self.assertEqual(response.context['currency'], 'USD')
        self.assertEqual(response.context['spent_month_count'], 1)
        self.assertEqual(response.context['spent_year_count'], 1)

    def test_dashboard_post_request(self):
        response = self.client.post(self.dashboard_url, {
            'description': 'Test Expense 2',
            'amount': 200.00,
            'category': self.category.id,
            'date_of_expense': datetime.now()
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Expense.objects.count(), 1)
