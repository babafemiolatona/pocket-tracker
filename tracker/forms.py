from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount']
        
#     description = forms.CharField(max_length=100)
#     amount = forms.IntegerField()
#     category = forms.CharField(max_length=100)

#     widget = {
#        'title': forms.TextInput(attrs={'class': 'input-group form-control form-control-lg'}),
#        'amount': forms.TextInput(attrs={'class': 'input-group form-control form-control-lg'}), 
#    }