# urls.py
from django.urls import path
# from .views import ExpenseListView, ExpenseDetailView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView
from .views import CreateExpenseView, ExpenseListView, expense_edit
from . import views

app_name = 'tracker'

urlpatterns = [
    path('expenses/create/', CreateExpenseView.as_view(), name='add_expense'),
    path('expenses/', ExpenseListView.as_view(), name='expenses'),
    path('edit-expense/<int:id>/', views.expense_edit, name='expense-edit'),
    # path('view/',views.expense_page,name="expense"),
    # path('expenses/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense_update'),
    # path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
    # path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense_detail'),
    # path('expenses/create/category/', views.add_expense_category, name='add_expense_category'),
]
