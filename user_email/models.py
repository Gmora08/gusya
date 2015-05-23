from django.db import models
import random

class WaitingList(models.Model):
    email = models.EmailField(unique=True)
    reference_code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    referenced_users = models.IntegerField(default=0, blank=True, null=True)

    def generate_code(self):
        while 1:
            code = str(random.random())[2:6]
            try:
                WaitingList.objects.get(reference_code=code)
            except:
                return code

    def save(self, *args, **kwargs):
        if not self.pk:
            self.reference_code = self.generate_code()
        super(WaitingList, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email + '-' + self.reference_code
