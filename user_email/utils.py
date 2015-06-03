from django.core.mail import send_mail
from django.core.mail import EmailMessage
import hashlib, datetime, random
from django.utils import timezone
from . import models
import openpay

openpay.api_key = "sk_d9d6f6e4c1c64decb6b1897e6f0229eb"
openpay.verify_ssl_certs = False
openpay.merchant_id = "mfwskxgm60glhftb6zoi"

def make_charge():
    pass

def get_customer(id_customer):
    customer = openpay.Customer.retrieve(id_customer)

def create_customer(data_user):
    customer = openpay.Customer.create(
        name=data_user['name'],
        email=data_user['email'],
        last_name=data_user['last_name'],
        phone_number=data_user['phone_number'],
    )
    return customer


def create_card(data_user, customer):
    card = customer.cards.create(
        token_id=data_user['token_id'],
        device_session_id=data_user['deviceIdHiddenFieldName']
    )
    return card, customer


def delete_customer(customer):
    print '+++++++++++++++++++++++++'
    print customer
    id_c = customer['id']
    customer.delete(
        id=id_c
    )


def sendMail(email=None, invitation_code=None):
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
        key_expires = datetime.datetime.today() + datetime.timedelta(2)

        #Add activation_key to user
        u.activation_key = activation_key
        u.key_expires = key_expires
        u.save()

        code = "http://www.gusya.co/user/confirm/%s" % activation_key
        #Send activation_email
        sendActivationEmail(email=u.email, activation_key=code)
    return True
