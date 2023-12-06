# urls.py
from django.urls import path
# from .views import ExpenseListView, ExpenseDetailView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView
from .views import CreateExpenseView, ExpenseListView, ExpenseDeleteView, ExpenseUpdateView
# from .views import edit_expense
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'tracker'

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expenses'),
    path('expenses/create/', CreateExpenseView.as_view(), name='create-expense'),
    path('expenses/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense-edit'),
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),
    path('expense-category-summary/', views.expense_category_summary, name='expense-category-summary'),
    path('expense-summary/', views.stats_view, name='stats'),
    path('search-expenses', csrf_exempt(views.search_expenses), name='search-expenses'),
    path('preferences/', views.preference, name='preference'),
    # path('edit-expense/<int:id>/', views.expense_edit, name='expense-edit'),
    # path('view/',views.expense_page,name="expense"),
    # path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
    # path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense_detail'),
    # path('expenses/create/category/', views.add_expense_category, name='add_expense_category'),
]
