from django.core.mail import EmailMessage
import hashlib, datetime, random
from django.utils import timezone
from decimal import *
from . import models
import openpay

openpay.api_key = "sk_d9d6f6e4c1c64decb6b1897e6f0229eb"
openpay.verify_ssl_certs = False
openpay.merchant_id = "mfwskxgm60glhftb6zoi"
openpay.production = False

def make_charge(data_charge):
    charge = openpay.Charge.create(
        method = 'card',
        source_id = data_charge['id_card'],
        amount = data_charge['amount'],
        currency = data_charge['currency'],
        description = data_charge['description'],
        device_session_id=data_charge['device_session_id'],
        customer = data_charge['customer'],
    )
    return charge

def get_customer(id_customer):
    customer = openpay.Customer.retrieve(id_customer)
    return customer

def create_customer(data_user):
    customer = openpay.Customer.create(
        name=data_user['name'],
        email=data_user['email'],
        last_name=data_user['last_name'],
        phone_number=data_user['phone_number'],
        requires_account=False
    )
    return customer

def create_card(data_user, customer):
    card = customer.cards.create(
        token_id=data_user['token_id'],
        device_session_id=data_user['deviceIdHiddenFieldName']
    )
    return card, customer


def delete_customer(customer):
    id_c = customer['id']
    customer.delete(
        id=id_c
    )


def sendMail(email=None, invitation_url=None):
    invitation_code = "gusya.co/user/invitation/%s" % invitation_url
    msg = EmailMessage(subject="Bienvenido a GusYa!", from_email="contacto@gusya.co", to=[email])
    msg.template_name = "welcome"
    msg.global_merge_vars = {
        'CODE': invitation_code,
    }
    msg.send()

def sendActivationEmail(email=None, activation_key=None):
    msg = EmailMessage(subject="Activacion a GusYa!", from_email="contacto@gusya.co", to=[email])
    msg.template_name = "Activate"
    msg.global_merge_vars = {
        'KEY': activation_key,
    }
    msg.send()

def getUserEmail(users_list=None):
    for user in users_list:
        #Get user by pk
        u = models.WaitingList.objects.get(pk=user)
        #Generate activation_key
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt+u.email).hexdigest()

        #Add activation_key to user
        u.activation_key = activation_key
        u.mail_sent = True
        u.save()

        code = "http://www.gusya.co/user/confirm/%s" % activation_key
        #Send activation_email
        print u.email
        sendActivationEmail(email=u.email, activation_key=code)
    return True

def get_charge_data(data):
    customer = models.WaitingList.objects.get(pk=data.getlist('card')[0])
    data_charge = {
        'id_card': customer.token_card,
        'amount': data.getlist('mount')[0],
        'currency': data.getlist('currency')[0],
        'description': data.getlist('description')[0],
        'device_session_id': 'kR1MiQhz2otdIuUlQkbEyitIqVMiI16f',
        'customer': customer.token_client,
    }
    return data_charge, customer

def save_charge(charge, user):
    payment = models.Payment(
        mount=float(charge['amount']),
        description=charge['description'],
        status=charge['status'],
        currency=charge['currency'],
        order_id=charge['id'],
        creation_date=charge['operation_date'],
        card=user
    )
    payment.save()
    return payment


def send_email_payment(email, payment):
    amount_len = len(str(payment.mount))
    amount_str = str(payment.mount)
    amount_new = amount_str[:amount_len-2] + '.' + amount_str[amount_len-2:]
    msg = EmailMessage(subject="Recibos GusYa!", from_email="contacto@gusya.co", to=[email])
    msg.template_name = "payment"
    msg.global_merge_vars = {
        'amount': amount_new,
        'description': payment.description,
        'card': payment.card.card_number,
        'date': payment.creation_date,
    }
    msg.send()
