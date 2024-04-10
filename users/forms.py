from django import forms

from users.models import User


""" Registration form """

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=150)
    email = forms.EmailField(max_length=256)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")
    active_balance = forms.FloatField(min_value=0)
    # safe_balance = forms.FloatField(min_value=0)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким username уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean(self):
        data = self.cleaned_data
        if data["password1"] != data["password2"]:
            print("bitch")
            raise forms.ValidationError("Пароли не совпадают!")
        print("mf")
        return data

    class Meta:
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
            "active_balance": forms.NumberInput(attrs={"class": "form-control"}),
            "safe_balance": forms.NumberInput(attrs={"class": "form-control"}),
        }


""" Form for user edition """

class ActiveBalanceForm(forms.Form):
    sum = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError("Значение не может быть отрицательным")
        return amount



""" Password reset form """

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    def clean(self):
        data = self.cleaned_data
        if data["password1"] != data["password2"]:
            print("bitch")
            raise forms.ValidationError("Пароли не совпадают!")
        print("mf")
        return data

    class Meta:
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }
