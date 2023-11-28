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
        ('Food', 'Food'),
        ('Entertainment', 'Entertainment'),
        ('Transport', 'Transport'),
        ('Bills', 'Bills'),
        ('Others', 'Others'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY, default=None)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.category
