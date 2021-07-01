from django.db import models

# Create your models here.


class Faculty(models.Model):
    full_name = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    mail = models.EmailField()
    password = models.CharField(max_length=50)
    status = (
        ('active', 'active'),
        ('pending', 'pending'),
        ('deactive', 'deactive')
    )
    account_status = models.CharField(
        choices=status, default='pending', max_length=10)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.username


class Student(models.Model):
    full_name = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    mail = models.EmailField()
    password = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.username


class OTP(models.Model):
    otp = models.IntegerField()
    mail = models.EmailField()

    class Meta:
        verbose_name_plural = 'OTPs'

    def __str__(self):
        return str(self.otp)


class Announce(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=255)

    class Meta:
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.title


class Gsheet(models.Model):
    sheetID = models.CharField(max_length=50)
    sheetNAME = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Gsheet'

    def __str__(self):
        return self.sheetNAME
