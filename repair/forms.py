from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import RepairRequest
import datetime

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone', 'password1', 'password2']


class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['car', 'problem', 'date', 'time']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(choices=[
                (datetime.time(h, 0), f"{h:02d}:00") for h in range(8, 22)
            ]),
        }

    def clean_time(self):
        time = self.cleaned_data['time']
        if time < datetime.time(8, 0) or time > datetime.time(21, 0):
            raise forms.ValidationError("Можно выбрать время только с 8:00 до 21:00.")
        return time