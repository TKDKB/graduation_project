from django import forms
from .models import BalanceChange, Category, RegularBalanceChange

# TODO: Сделать нормальное поле для выбора периодичности в регулярном доходе
class IncomeForm(forms.ModelForm):
    class Meta:
        model = BalanceChange
        fields = ['sum', 'category', 'description']
        labels = {
            'sum': 'Сумма',
            'category_id': 'Категория',
            'description': 'Описание',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False  # Поле категории не обязательно


class ExpenceForm(forms.ModelForm):
    class Meta:
        model = BalanceChange
        fields = ['sum', 'necessity', 'category', 'description']
        labels = {
            'sum': 'Сумма',
            'necessity': 'Необходимость траты',
            'category': 'Категория',
            'description': 'Описание',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExpenceForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False  # Поле категории не обязательно


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_private', 'type']
        labels = {
            'name': 'Название',
            'is_private': 'Приватность',
            'type': 'Тип изменения баланса',
        }


class RegularIncomeForm(forms.ModelForm):
    class Meta:
        model = RegularBalanceChange
        fields = ['sum', 'category', 'description', 'regularity']
        labels = {
            'sum': 'Сумма',
            'category': 'Категория',
            'description': 'Описание',
            'regularity': 'Регулярность',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
