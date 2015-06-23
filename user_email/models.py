from django.db import models
from django.contrib.auth.models import User
from . import choices
import hashlib, datetime, random
import datetime


class WaitingList(models.Model):
    name = models.CharField("Nombre", max_length=255, blank=True, null=True)
    last_name = models.CharField("Apellido", max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    referenced_users = models.IntegerField(default=0, blank=True, null=True)
    active_user = models.BooleanField(default=False)
    mail_sent = models.BooleanField(default=False)
    invitation_url = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.BigIntegerField("Numero Telefonico", unique=True)
    user = models.OneToOneField(User, null=True, blank=True)
    activation_key = models.CharField(max_length=40, blank=True, null=True)
    registration_date = models.DateTimeField(editable=False)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    token_client = models.CharField(max_length=500, blank=True, null=True)
    token_card = models.CharField(max_length=500, blank=True, null=True)
    activation_date = models.DateTimeField(editable=False, null=True)

    def generate_invitation_url(self):
        #Generate activation_key
        salt = hashlib.sha1(str(random.random())).hexdigest()[:3]
        activation_key = hashlib.sha1(salt+str(self.phone_number)).hexdigest()
        return activation_key

    def save_card_data(self, card_number, token_id, client_id):
        self.card_number = card_number
        self.token_card = token_id
        self.token_client = client_id
        self.save()

    def save_user_data(self, user_data):
        self.name = user_data['name']
        self.last_name = user_data['last_name']
        self.phone_number = user_data['phone_number']
        self.save()

    def save_send_email(self):
        self.mail_sent = True
        self.save()

    def generate_activation_date(self):
        self.activation_date = datetime.datetime.today()
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invitation_url = self.generate_invitation_url()
            self.registration_date = datetime.datetime.today()
        super(WaitingList, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.phone_number)


class Payment(models.Model):
    mount = models.FloatField()
    description = models.CharField(max_length=400)
    status = models.CharField(max_length=10 ,default=False)
    currency = models.CharField(max_length=4, choices=choices.CURRENCY)
    order_id = models.CharField(max_length=100)
    creation_date = models.DateTimeField(null=True, blank=True)
    card = models.ForeignKey(WaitingList)

    def __unicode__(self):
        return str(self.mount) + '-' + self.card.email
