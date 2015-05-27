from django.db import models
from django.contrib.auth.models import User
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
    activation_date = models.DateTimeField(editable=False, null=True)


    def generate_code(self):
        while 1:
            code = str(random.random())[2:6]
            try:
                WaitingList.objects.get(reference_code=code)
            except:
                return code

    def generate_activation_date(self):
        self.activation_date = datetime.datetime.today()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.reference_code = self.generate_code()
            self.registration_date = datetime.datetime.today()
        super(WaitingList, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email + '-' + self.reference_code
