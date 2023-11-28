from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Category, Expense
from django.views.generic import ListView
from django.core.paginator import Paginator
from .forms import ExpenseForm
from django.shortcuts import get_object_or_404

class ExpenseListView(ListView):
    model = Expense
    template_name = 'web_static/index.html'
    context_object_name = 'expenses'
    paginate_by = 5

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page')
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_obj = Paginator.get_page(paginator, page_number)
        context['page_obj'] = page_obj
        return context

class CreateExpenseView(View):
    template_name = 'web_static/create_expense.html'

    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'values': request.POST
        }
        return render(request, self.template_name, context)

    def post(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'values': request.POST
        }

        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, self.template_name, context)

        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category = request.POST.get('category')

        if not description:
            messages.error(request, 'Description is required')
            return render(request, self.template_name, context)

        Expense.objects.create(
            user=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description
        )

        messages.success(request, 'Expense saved successfully')
        return redirect('tracker:expenses')

def expense_edit(request, id):
    expense = get_object_or_404(Expense, pk=id)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully')
            return redirect('expenses')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ExpenseForm(instance=expense)

    context = {
        'form': form,
        'expense': expense,
        'categories': categories
    }

    return render(request, 'web_static/edit-expense.html', context)