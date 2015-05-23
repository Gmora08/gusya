from django import forms
from . import models

class RegisterForm(forms.ModelForm):
    invitation_code = forms.CharField(max_length=6, required=False)

    class Meta:
        model = models.WaitingList
        fields = ['email']
