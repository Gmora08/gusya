from django.core.mail import send_mail
from django.core.mail import EmailMessage
import hashlib, datetime, random
from django.utils import timezone
from . import models

def sendMail(email=None, invitation_code=None):
    msg = EmailMessage(subject="Bienvenido a GusYa!", from_email="gmora008@gmail.com", to=[email])
    msg.template_name = "welcome"
    msg.global_merge_vars = {
        'CODE': invitation_code,
    }
    msg.send()

def sendActivationEmail(email=None, activation_key=None):
    msg = EmailMessage(subject="Activacion a GusYa!", from_email="gmora008@gmail.com", to=[email])
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
