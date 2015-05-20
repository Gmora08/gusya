from django.db import models
import random

class WaitingList(models.Model):
    email = models.EmailField()
    reference_code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    referenced_users = models.IntegerField(default=0, blank=True, null=True)

    def generate_code(self):
        while 1:
            code = str(random.random())[2:6]
            try:
                WaitingList.objects.get(reference_code=code)
            except:
                self.reference_code = code

#    def save(*args, **kwargs):
#       if not self.pk:
            #lalal
#      super(WaitingList, self).save(*args, **kwargs)
