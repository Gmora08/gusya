from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from . import models
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
            utils.sendMail(email=email)
            form.save()
            form = forms.RegisterForm()
            messages.success(request, u'Agregado a la lista de espera')
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})
