from django import forms
from .models import BalanceChange, Category


class IncomeForm(forms.ModelForm):
    class Meta:
        model = BalanceChange
        fields = ['sum', 'category_id', 'description']
        labels = {
            'sum': 'Сумма',
            'category_id': 'Категория',
            'description': 'Описание',
        }

        widgets = {
            'category_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].required = False  # Поле категории не обязательно


class ExpenceForm(forms.ModelForm):
    class Meta:
        model = BalanceChange
        fields = ['sum', 'necessity', 'category_id', 'description']
        labels = {
            'sum': 'Сумма',
            'necessity': 'Необходимость траты',
            'category_id': 'Категория',
            'description': 'Описание',
        }

        widgets = {
            'category_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExpenceForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].required = False  # Поле категории не обязательно


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_private', 'type']
        labels = {
            'name': 'Название',
            'is_private': 'Приватность',
            'type': 'Тип изменения баланса',
        }
