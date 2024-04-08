from django import forms
from django.core.validators import MinValueValidator

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

    def __init__(self, user, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['category'].queryset = Category.objects.filter(type='I', user=user)
        self.fields['sum'].validators.append(MinValueValidator(limit_value=0))


class ExpenceForm(forms.ModelForm):
    class Meta:
        model = BalanceChange
        fields = ['sum', 'category', 'description']
        labels = {
            'sum': 'Сумма',
            # 'necessity': 'Необходимость траты',
            'category': 'Категория',
            'description': 'Описание',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ExpenceForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False  # Поле категории не обязательно
        self.fields['category'].queryset = Category.objects.filter(type='E', user=user)
        self.fields['sum'].validators.append(MinValueValidator(limit_value=0))


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        labels = {
            'name': 'Название',
            'type': 'Тип изменения баланса',
        }


# class RegularIncomeForm(forms.ModelForm):
#     class Meta:
#         model = RegularBalanceChange
#         fields = ['sum', 'category', 'description', 'regularity']
#         labels = {
#             'sum': 'Сумма',
#             'category': 'Категория',
#             'description': 'Описание',
#             'regularity': 'Регулярность',
#         }
#
#         widgets = {
#             'category': forms.Select(attrs={'class': 'form-control'}),
#         }


class RegularIncomeForm(forms.Form):
    name = forms.CharField(label="Название", max_length=255)

    replenishment_amount = forms.DecimalField(label='Сумма пополнения', max_digits=10, decimal_places=2,
                                              min_value=0)
    recharge_day = forms.IntegerField(label='День месяца', min_value=1, max_value=31)
