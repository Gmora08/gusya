from django.forms import ModelForm
from . import models

class RegisterForm(ModelForm):
    class Meta:
        model = models.WaitingList
        fields = ['email',]
