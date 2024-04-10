from django import forms
from django.core.validators import MinValueValidator

from .models import BalanceChange, Category
from django_celery_beat.models import PeriodicTask

# TODO: Сделать нормальное поле для выбора периодичности в регулярном доходе
class IncomeForm(forms.ModelForm):
    sum = forms.DecimalField(max_digits=10, decimal_places=2)

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
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RegularIncomeForm, self).__init__(*args, **kwargs)

    def clean(self):
        print("aaa")
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        sum = int(cleaned_data.get("replenishment_amount")) * 100  # Исправлено на sum

        task_name = f"user_{self.user.id}_income_{sum}_name_{name}"

        # Проверка наличия записи с аналогичными данными в базе данных
        existing_records = PeriodicTask.objects.filter(
            name=task_name,
            args=f"[{self.user.id}, {sum}]"

        )
        if existing_records.exists():
            raise forms.ValidationError("Запись с такими данными уже существует.")

        return cleaned_data