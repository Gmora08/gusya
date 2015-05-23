from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib import messages
import ast
from django.utils import timezone
from . import models
from . import forms
from . import utils


def home(request):
    return redirect(reverse('user:waiting_list'))


def PhoneUsers(request):
    template_name = 'registration/users_p.html'
    users = models.WaitingList.objects.filter(phone_number__isnull=False)
    return render(request, template_name, {'users': users})


class register_confirm(View):
    template_name = "registration/phone_number.html"
    def get(self, request, activation_key):
        form = forms.PhoneNumberForm()
        # check if there is UserProfile which matches the activation key (if not then display 404)
        user_profile = models.WaitingList.objects.get(activation_key=activation_key)
        print user_profile
        #check if the activation key has expired, if it hase then render confirm_expired.html
        if user_profile.key_expires < timezone.now():
            messages.error(request, u'Lo sentimos tu codigo de activacion expiro')
            return redirect(reverse('user:waiting_list'))
        #if the key hasn't expired save user and set him as active and render some template to confirm activation
        user_profile.active_user = True
        user_profile.save()
        return render(request, self.template_name, {'form': form})

    def post(self, request, activation_key):
        form = forms.PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = request.POST.getlist('phone_number')
            user_profile = models.WaitingList.objects.get(activation_key=activation_key)
            print phone_number
            print type(phone_number)
            user_profile.phone_number = phone_number[0]
            user_profile.save()
            return redirect(reverse('user:waiting_list'))
        return render(request, self.template_name, {'form': form})

class SendEmailActivation(View):
    template_name = "registration/send_email_user.html"
    def get(self, request):
        qs = models.WaitingList.objects.exclude(active_user=True)
        form = forms.UserActivationForm(qs)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        users_list = request.POST.getlist('emails')
        utils.getUserEmail(users_list=users_list)
        return redirect(reverse('user:active_user'))


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
