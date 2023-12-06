from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'category', 'date_of_expense']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}), 
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date_of_expense': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    category = forms.ChoiceField(choices=Expense.CATEGORY,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
