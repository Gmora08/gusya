from django.shortcuts import render
from django.views.generic import View
from . import forms
from . import utils


class WaitingListRegistration(View):
    template_name = "registration/index.html"
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        email = request.POST['email']
        if form.is_valid():
            utils.sendMail(email=email)
            form.save()
            form = forms.RegisterForm()
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {})
