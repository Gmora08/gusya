from django.core.mail import EmailMessage
import hashlib, datetime, random
from django.utils import timezone
from decimal import *
from . import models
import openpay
import conekta
conekta.api_key = "key_RhTfmgz5UNAAiXbq8VrFPg"

openpay.api_key = "sk_d9d6f6e4c1c64decb6b1897e6f0229eb"
openpay.verify_ssl_certs = False
openpay.merchant_id = "mfwskxgm60glhftb6zoi"
openpay.production = True

def make_charge(data_charge):
    charge = conekta.Charge.create({
        'card': data_charge['card'],
        'amount': data_charge['amount'],
        'currency': data_charge['currency'],
        'description': data_charge['description'],
        'details': data_charge['details']
   })
    return charge

def create_customer(data_user):
    customer = conekta.Customer.create({
        "name":  data_user['name'],
        "email": data_user['email'],
        "phone": data_user['phone'],
    })
    return customer


def create_card(token_card, id_customer):
    customer = conekta.Customer.find(id_customer)
    card = customer.createCard({"token_id": token_card})
    return card

def delete_customer(id_customer):
    customer = conekta.Customer.find(id_customer)
    customer.delete()

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
    amount = Decimal(data.getlist('mount')[0]).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    amount_str = str(amount).replace('.', '')
    amount = int(amount_str)
    
    data_charge = {
        'card': customer.token_card,
        'amount': amount,
        'currency': str(data.getlist('currency')[0]),
        'description': str(data.getlist('description')[0]),
        'details': {
            'email': customer.email
        }
        
    }
    return data_charge, customer

def save_charge(charge, user):

    payment = models.Payment(mount=float(charge.amount), description=charge.description, status=charge.status, currency='MXN', order_id=charge.id, creation_date=datetime.datetime.now(), card=user)
    payment.save()
    return payment

def send_email_payment(email, payment):
    amount_len = len(str(payment.amount))
    amount_str = str(payment.amount)
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
