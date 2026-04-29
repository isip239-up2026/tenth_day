from django import forms


class ApplicationForm(forms.Form):
    hacker_handle = forms.CharField(
        label="Ваш псевдоним",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-light border-secondary",
            "placeholder": "Введите свой псевдоним"
        })
    )
    message = forms.CharField(
        label="Сообщение заказчику",
        widget=forms.Textarea(attrs={
            "class": "form-control bg-dark text-light border-secondary",
            "rows": 4,
            "placeholder": "Почему именно вы должны получить этот контракт?"
        })
    )