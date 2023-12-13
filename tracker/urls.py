from django.urls import path
from .views import CreateExpenseView, ExpenseListView, ExpenseDeleteView, ExpenseUpdateView
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'tracker'

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expenses'),
    path('expense/create', CreateExpenseView.as_view(), name='create-expense'),
    path('expense/<int:pk>/update', ExpenseUpdateView.as_view(), name='expense-edit'),
    path('expense/<int:pk>/delete', ExpenseDeleteView.as_view(), name='expense-delete'),
    path('expense-category-summary/', views.expense_category_summary, name='expense-category-summary'),
    path('expense-summary', views.stats_view, name='stats'),
    path('search-expenses', csrf_exempt(views.search_expenses), name='search-expenses'),
    path('preferences', views.preference, name='preference'),
    path('dashboard', views.dashboard, name='dashboard'),
]
