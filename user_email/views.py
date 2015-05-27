from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import ast
from . import models
from . import forms
from . import utils


def home(request):
    return redirect(reverse('user:waiting_list'))


def PhoneUsers(request):
    if not request.user.is_active:
        return redirect(reverse('user:admin_login'))
    template_name = 'registration/users_p.html'
    users = models.WaitingList.objects.filter(phone_number__isnull=False)
    return render(request, template_name, {'users': users})

class LoginAdmin(View):
    template_name = 'registration/login_admin.html'
    def get(self, request):
        if request.user.is_active:
            return redirect(reverse('user:active_user'))
        form = AuthenticationForm()
        return  render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print user
        if user:
            login(request, user)
            return redirect(reverse('user:active_user'))
        else:
            messages.error(request, u'Usuario/Password Incorrectos')
            return render(request, self.template_name, {'form': form})


def logout_admin(request):
    logout(request)
    return redirect(reverse('user:admin_login'))


class register_confirm(View):
    template_name = "registration/phone_number.html"
    def get(self, request, activation_key):
        form = forms.PhoneNumberForm()
        # check if there is UserProfile which matches the activation key (if not then display 404)
        try:
            user_profile = models.WaitingList.objects.get(activation_key=activation_key)

        except:
            messages.error(request, u'Hubo un problema con tu codigo contactanos a contacto@gusya.co')
            return redirect(reverse('user:waiting_list'))

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
            name = request.POST.getlist('name')
            last_name = request.POST.getlist('last_name')
            user_profile = models.WaitingList.objects.get(activation_key=activation_key)

            user_profile.phone_number = phone_number[0]
            user_profile.name = name[0]
            user_profile.last_name = last_name[0]
            user_profile.generate_activation_date()
            user_profile.save()
            messages.success(request, u'Gus se comunicara contigo en cualquier momento')
            return redirect(reverse('user:waiting_list'))
        return render(request, self.template_name, {'form': form})

class SendEmailActivation(View):
    template_name = "registration/send_email_user.html"

    def get(self, request):
        if not request.user.is_active:
            return redirect(reverse('user:admin_login'))

        user_list = models.WaitingList.objects.filter(active_user=False)
        return render(request, self.template_name, {'users': user_list})

    def post(self, request):
        if not request.user.is_active:
            return redirect(reverse('user:admin_login'))
        users_list = request.POST.getlist('emails')
        print users_list
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
            return redirect(reverse('user:waiting_list'))
        else:
            return render(request, self.template_name, {'form': form})
