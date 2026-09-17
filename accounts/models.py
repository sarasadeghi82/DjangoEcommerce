from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'مدیر'),
        ('staff', 'فروشنده'),
        ('customer', 'مشتری'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # هماهنگی دوطرفه بین role و پرچم‌های جنگو
        if self.role == 'admin':
            self.is_staff = True
            self.is_superuser = True
        elif self.is_superuser:
            # اگه یه‌جایی (مثلاً createsuperuser) is_superuser=True شد، role هم admin بشه
            self.role = 'admin'
            self.is_staff = True

        super().save(*args, **kwargs)


    def __str__(self):
        return self.username





