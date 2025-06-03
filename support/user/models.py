from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def calc_age(self):
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
            )
        return None

    def save(self, *args, **kwargs):
        # Forcer can_data_be_shared à False si l'utilisateur a moins de 15 ans
        age = self.calc_age()
        if age is not None and age < 15:
            self.can_data_be_shared = False

        super().save(*args, **kwargs)
