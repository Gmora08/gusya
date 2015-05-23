from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib import messages
import ast
from . import models
from . import forms
from . import utils

def home(request):
    return redirect(reverse('user:waiting_list'))

class SendEmailActivation(View):
    template_name = "registration/send_email_user.html"
    def get(self, request):
        qs = models.WaitingList.objects.filter(active_user=False)
        form = forms.UserActivationForm(qs)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        emails = request.POST.getlist('emails')
        pass

class WaitingListRegistration(View):
    template_name = "registration/index.html"
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        email = request.POST['email']
        invitation_code = request.POST['invitation_code']
        if form.is_valid():
            if invitation_code:
                try:
                    user = models.WaitingList.objects.get(reference_code=invitation_code)
                    user.referenced_users += 1
                    user.save()
                except:
                    messages.error(request, u'Codigo Invalido')
                    return render(request, self.template_name, {'form': form})
            new_user = form.save()
            utils.sendMail(email=email, invitation_code=new_user.reference_code)
            form = forms.RegisterForm()
            messages.success(request, u'Agregado a la lista de espera')
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})
