from django import forms
from . import models

class RegisterForm(forms.ModelForm):
    invitation_code = forms.CharField(max_length=6, required=False)

    class Meta:
        model = models.WaitingList
        fields = ['email']

class UserActivationForm(forms.Form):

    def __init__(self, qs=None, *args, **kwargs):
        super(UserActivationForm, self).__init__(*args, **kwargs)
        if qs:
            self.fields['emails'] = forms.ModelMultipleChoiceField(queryset=qs, widget=forms.CheckboxSelectMultiple())
