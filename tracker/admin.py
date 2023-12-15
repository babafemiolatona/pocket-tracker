from django.contrib import admin
from .models import Category, Expense, UserPreference

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(UserPreference)
