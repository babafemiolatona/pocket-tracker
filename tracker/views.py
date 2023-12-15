from django.shortcuts import render
from django.contrib import messages
from .models import Expense, UserPreference
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.core.paginator import Paginator
from .forms import ExpenseForm
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
from datetime import date, timedelta
from django.conf import settings
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import ExpenseForm


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'web_static/index.html'
    context_object_name = 'expenses'
    paginate_by = 5
    login_url = 'users:login'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Expense.objects.filter(
                user=self.request.user).order_by('-date_of_expense')
        else:
            return Expense.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page')
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_obj = paginator.get_page(page_number)

        if self.request.user.is_authenticated:
            try:
                currency = UserPreference.objects.get(
                    user=self.request.user).currency
            except UserPreference.DoesNotExist:
                currency = None
        else:
            currency = None

        context['page_obj'] = page_obj
        context['currency'] = currency
        return context


class CreateExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'web_static/create_expense.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('tracker:expenses')
    login_url = 'users:login'

    def form_valid(self, form):
        expense = form.save(commit=False)
        expense.user = self.request.user
        expense.save()
        messages.success(self.request, 'Expense saved successfully.')
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'web_static/edit_expense.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExpenseForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('tracker:expenses')

    def form_valid(self, form):
        messages.success(self.request, 'Expense updated successfully.')
        return super().form_valid(form)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'web_static/expense_delete.html'
    success_url = reverse_lazy('tracker:expenses')
    login_url = 'users:login'

    def form_valid(self, form):
        messages.success(self.request, 'Expense deleted successfully.')
        return super().form_valid(form)


@login_required(login_url='users:login')
def expense_category_summary(request):
    todays_date = date.today()
    one_month_ago = todays_date - timedelta(days=30)

    expenses = Expense.objects.filter(user=request.user,
                                      date_of_expense__gte=one_month_ago,
                                      date_of_expense__lte=todays_date)
    finalrep = {}

    def get_expense_category_amount(category):
        filtered_by_category = expenses.filter(category=category)
        return sum(item.amount for item in filtered_by_category)

    category_list = list(set(expense.category for expense in expenses))

    for category in category_list:
        finalrep[category] = get_expense_category_amount(category)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


@login_required(login_url='users:login')
def stats_view(request):
    return render(request, 'web_static/stats.html')


@login_required(login_url='users:login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = (Expense.objects.filter(
            amount__istartswith=search_str,
            user=request.user
        ) | Expense.objects.filter(
            date_of_expense__istartswith=search_str,
            user=request.user
        ) | Expense.objects.filter(
            description__icontains=search_str,
            user=request.user
        ) | Expense.objects.filter(
            category__icontains=search_str,
            user=request.user
        ))
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='users:login')
def preference(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'web_static/preference.html',
                      {
                        'currencies': currency_data,
                        'user_preferences': user_preferences
                      })
    else:

        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'web_static/preference.html',
                      {
                        'currencies': currency_data,
                        'user_preferences': user_preferences
                      })


@login_required(login_url='users:login')
def dashboard(request):
    """The view of the main page."""
    # Retrieve user's currency preference
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = None

    expenses = Expense.objects.filter(user=request.user)
    expenses = expenses.order_by("-date_of_expense")

    # Expenses this year
    expenses_this_year = expenses.filter(
        date_of_expense__year=datetime.now().year
    )
    total_this_year = sum(expense.amount for expense in expenses_this_year)

    # Expenses this month
    expenses_this_month = expenses.filter(
        date_of_expense__month=datetime.now().month
    )
    total_this_month = sum(expense.amount for expense in expenses_this_month)

    spent_month_count = expenses_this_month.count()
    spent_year_count = expenses_this_year.count()

    expense_short_form = ExpenseForm()

    # Quick expense addition
    if request.method == "POST":
        expense_short_form = ExpenseForm(request.POST)
        if expense_short_form.is_valid():
            expense = expense_short_form.save(commit=False)
            expense.user = request.user
            expense.save()

    context = {
        "expenses": expenses,
        "expenses_this_year": expenses_this_year,
        "expenses_this_month": expenses_this_month,
        "expense_short_form": expense_short_form,
        "total_this_year": total_this_year,
        "total_this_month": total_this_month,
        "currency": currency,
        "spent_month_count": spent_month_count,
        "spent_year_count": spent_year_count,
    }
    return render(request, "web_static/dashboard.html", context)
