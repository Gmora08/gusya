from django import forms
from . import models

class RegisterForm(forms.ModelForm):
    invitation_code = forms.CharField(max_length=6, required=False)

    class Meta:
        model = models.WaitingList
        fields = ['phone_number']

class UserActivationForm(forms.Form):

    def __init__(self, qs=None, *args, **kwargs):
        super(UserActivationForm, self).__init__(*args, **kwargs)
        if qs:
            self.fields['emails'] = forms.ModelMultipleChoiceField(queryset=qs, widget=forms.CheckboxSelectMultiple())

class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = models.WaitingList
        fields = ['name', 'last_name', 'phone_number', 'email']


class LoginAdminForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.Payment
        fields = ['mount', 'description', 'currency','card']

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['card'].queryset = models.WaitingList.objects.filter(token_card__isnull=False)
