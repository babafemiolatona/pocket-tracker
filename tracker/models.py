from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, default=None)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    CATEGORY = [
        ('', 'Select category'),
        ('Food', 'Food'),
        ('Clothing', 'Clothing'),
        ('Personal Care', 'Personal Care'),
        ('Utilities', 'Utilities'),
        ('Travel', 'Travel'),
        ('Health care', 'Health care'),
        ('Entertainment', 'Entertainment'),
        ('Transport', 'Transport'),
        ('Miscellaneous', 'Miscellaneous'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_expense = models.DateField(default=timezone.now)
    category = models.CharField(choices=CATEGORY, default=None)

    class Meta:
        ordering = ['-date_of_expense']

    def __str__(self):
        return self.category


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, default=None)

    def __str__(self):
        return str(self.user) + 's' + ' preferences'
