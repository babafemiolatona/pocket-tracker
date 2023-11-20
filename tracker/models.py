from django.db import models
from django.utils.text import slugify

class Budget(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Budget, self).save(*args, **kwargs)

    def budget_left(self):
        expense_list = Expense.objects.filter(budget=self)
        total_expense = 0
        for expense in expense_list:
            total_expense += expense.amount
        return self.budget - total_expense
    
    def total_transactions(self):
        expense_list = Expense.objects.filter(budget=self)
        return len(expense_list)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()

    class Meta:
        ordering = ('-amount',)

    def __str__(self):
        return f"{self.description} - {self.amount}"