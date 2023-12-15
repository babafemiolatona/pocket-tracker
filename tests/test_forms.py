from django.test import TestCase
from tracker.forms import ExpenseForm
from tracker.models import Expense


class TestExpenseForm(TestCase):
    def setUp(self):
        self.form_data = {
            'amount': 100,
            'description': 'Test expense',
            'category': 'Food',
            'date_of_expense': '2022-01-01',
        }

    def test_form_is_valid(self):
        form = ExpenseForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_amount_field_label(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['amount'].label, 'Amount')

    def test_form_description_field_label(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['description'].label, 'Description')

    def test_form_category_field_label(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['category'].label, 'Select Category')

    def test_form_date_of_expense_field_label(self):
        form = ExpenseForm()
        self.assertEqual(
            form.fields['date_of_expense'].label,
            'Date of expense'
        )

    def test_form_amount_field_help_text(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['amount'].help_text, '')

    def test_form_description_field_help_text(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['description'].help_text, '')

    def test_form_category_field_help_text(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['category'].help_text, '')

    def test_form_date_of_expense_field_help_text(self):
        form = ExpenseForm()
        self.assertEqual(form.fields['date_of_expense'].help_text, '')
