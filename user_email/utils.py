from django.core.mail import send_mail
from django.core.mail import EmailMessage

def sendMail(email=None, invitation_code=None):
    msg = EmailMessage(subject="Bienvenido a GusYa!", from_email="gmora008@gmail.com", to=[email])
    msg.template_name = "welcome"
    msg.global_merge_vars = {
        'CODE': invitation_code,
    }
    msg.send()
