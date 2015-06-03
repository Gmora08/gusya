from django.db import models
from django.contrib.auth.models import User
from . import choices
import random
import datetime


class WaitingList(models.Model):
    name = models.CharField("Nombre", max_length=255, blank=True, null=True)
    last_name = models.CharField("Apellido", max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    reference_code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    referenced_users = models.IntegerField(default=0, blank=True, null=True)
    active_user = models.BooleanField(default=False)
    phone_number = models.BigIntegerField("Numero Telefonico", blank=True, null=True)
    user = models.OneToOneField(User, null=True, blank=True)
    activation_key = models.CharField(max_length=40, blank=True, null=True)
    key_expires = models.DateTimeField(default=datetime.date.today(), blank=True, null=True)
    registration_date = models.DateTimeField(editable=False)
    card_number = models.CharField(max_length=255, blank=True, null=True)
    token_client = models.CharField(max_length=500, blank=True, null=True)
    token_card = models.CharField(max_length=500, blank=True, null=True)
    activation_date = models.DateTimeField(editable=False, null=True)

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

    def generate_code(self):
        while 1:
            code = str(random.random())[2:6]
            try:
                WaitingList.objects.get(reference_code=code)
            except:
                return code

    def generate_activation_date(self):
        self.activation_date = datetime.datetime.today()
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.reference_code = self.generate_code()
            self.registration_date = datetime.datetime.today()
        super(WaitingList, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email


class Payment(models.Model):
    mount = models.FloatField()
    description = models.CharField(max_length=400)
    status = models.BooleanField(default=False)
    currency = models.CharField(max_length=4, choices=choices.CURRENCY)
    order_id = models.CharField(max_length=100)
    creation_date = models.DateTimeField(null=True, blank=True)
    operation_date = models.DateTimeField(null=True, blank=True)
    card = models.ForeignKey(WaitingList)

    def __unicode__(self):
        return self.mount + self.card
