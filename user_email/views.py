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
                payment = utils.save_charge(charge, user)
                utils.send_email_payment(user.email, payment)
                messages.success(request, u'Pago realizado con exito')
                return redirect(reverse('user:make_charge'))
            except e:
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
    def get(self, request, activation_key):
        form = forms.PhoneNumberForm()
        # check if there is UserProfile which matches the activation key (if not then display 404)
        try:
            user_profile = models.WaitingList.objects.get(activation_key=activation_key)

        except:
            messages.error(request, u'Hubo un problema con tu codigo contactanos a contacto@gusya.co')
            return redirect(reverse('user:waiting_list'))

        return render(request, self.template_name, {'form': form})

    def post(self, request, activation_key):

        card = None
        user_profile = models.WaitingList.objects.get(activation_key=activation_key)
        data_user = {
            'name': request.POST["name"],
            'last_name': request.POST['last_name'],
            'phone': request.POST['phone_number'],
            'email': user_profile.email,
            'token_id': request.POST["conektaTokenId"]
        }
        try:
            customer = utils.create_customer(data_user)
            card = utils.create_card(data_user['token_id'], customer.id)
            user_profile.generate_activation_date()
            user_profile.save_user_data(data_user)
        except Exception as e:
            print e
            utils.delete_customer(customer.id)
            messages.error(request, u'Tu tarjeta no es valida')
            return render(request, self.template_name, {})
        user_profile.save_card_data(card.last4, card.id, customer.id)
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
        form = forms.RegisterForm(request.POST)
        email = request.POST['email']
        if form.is_valid():
            new_user = form.save()
            utils.sendMail(email=email, invitation_url=new_user.invitation_url)
            messages.success(request, u'Estas en la lista de espera')
            return redirect(reverse('user:waiting_list'))
        else:
            return render(request, self.template_name, {'form': form})
