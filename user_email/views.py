from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from . import models
from . import forms
from . import utils


def home(request):
    return redirect(reverse('user:waiting_list'))

def faq(request):
    template_name = 'registration/faq.html'
    form = forms.RegisterForm()
    return render(request, template_name, {'form': form})

def PhoneUsers(request):
    if not request.user.is_active:
        return redirect(reverse('user:admin_login'))
    template_name = 'registration/users_p.html'
    users = models.WaitingList.objects.filter(phone_number__isnull=False)
    return render(request, template_name, {'users': users})

class Payment(View):
    template_name = 'registration/charge.html'

    def get(self, request):
        form = forms.PaymentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.PaymentForm(request.POST)
        if form.is_valid():
            try:
                data_charge, user = utils.get_charge_data(request.POST)
                charge = utils.make_charge(data_charge)
                print charge
                payment = utils.save_charge(charge, user)
                utils.send_email_payment(user.email, payment)
                messages.success(request, u'Pago realizado con exito')
                return redirect(reverse('user:make_charge'))
            except ValueError:
                print ValueError
                messages.error(request, u'Hubo un error al procesar el pago')
                return render(request, self.template_name, {'form': form})
            return redirect(reverse('user:make_charge'))
        return render(request, self.template_name, {'form': form})

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


class register_card(View):
    template_name = "registration/card.html"
    def get(self, request):
        form = forms.PhoneNumberForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        card = None
        user_profile = models.WaitingList.objects.get(activation_key=activation_key)
        user_profile.generate_activation_date()
        data_user = {
            'name': request.POST.getlist('name')[0],
            'last_name': request.POST.getlist('last_name')[0],
            'phone_number': request.POST.getlist('phone_number')[0],
            'email': user_profile.email,
            'deviceIdHiddenFieldName': request.POST.getlist('deviceIdHiddenFieldName')[0],
            'token_id': request.POST.getlist('token_id')[0]
        }
        try:
            customer = utils.create_customer(data_user)
            card = utils.create_card(data_user, customer)
            user_profile.save_user_data(data_user)
        except Exception as e:
            print '****************************'
            print e
            utils.delete_customer(customer)
            messages.error(request, u'Tu tarjeta no es valida')
            return render(request, self.template_name, {})
        user_profile.save_card_data(card[0]['card_number'], card[0]['id'], card[0]['customer_id'])
        user_profile.active_user = True
        user_profile.save()
        messages.success(request, u'Gus se comunicara contigo en cualquier momento')
        return redirect(reverse('user:waiting_list'))



class SendEmailActivation(View):
    template_name = "registration/send_email_user.html"

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect(reverse('user:admin_login'))
        user_list = models.WaitingList.objects.filter(Q(active_user=False), Q(mail_sent=False))
        return render(request, self.template_name, {'users': user_list})

    def post(self, request):
        if not request.user.is_active:
            return redirect(reverse('user:admin_login'))
        users_list = request.POST.getlist('emails')
        utils.getUserEmail(users_list=users_list)
        return redirect(reverse('user:active_user'))

class GetSentEmailUser(View):
    template_name = "registration/get_users_mail_sent.html"

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect(reverse('user:admin_login'))
        user_list = models.WaitingList.objects.filter(mail_sent=True)
        return render(request, self.template_name, {'users': user_list})

    def post(self, request):
        if not request.user.is_authenticated():
            return redirect(reverse('user:admin_login'))
        users_list = request.POST.getlist('emails')
        utils.getUserEmail(users_list=users_list)
        return redirect(reverse('user:active_user'))


class RegisterUserByInvitation(View):
    template_name = "registration/index.html"
    def get(self, request, invitation):
        form = forms.RegisterForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request, invitation):
        try:
            user = models.WaitingList.objects.get(invitation_url=invitation)
            form = forms.RegisterForm(request.POST)
            email = request.POST['email']
            if form.is_valid():
                new_user = form.save()
                user.referenced_users += 1
                user.save()
                utils.sendMail(email=email, invitation_url=new_user.invitation_url)
                messages.success(request, u'Estas en la lista de espera')
                return redirect(reverse('user:waiting_list'))
            else:
                return render(request, self.template_name, {'form': form})
        except :
             messages.error(request, u'Codigo de invitacion invalido')
             return redirect(reverse('user:waiting_list'))

class WaitingListRegistration(View):
    template_name = "registration/index.html"
    def get(self, request):
        form = forms.RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        template = 'registration/registration.html'
        form = forms.RegisterForm(request.POST)
        phone_number = request.POST['phone_number']
        if form.is_valid():
            new_user = form.save()
            return render(request, template, {})
        else:
            return render(request, self.template_name, {'form': form})
