# Generated by Django 3.2.4 on 2021-06-24 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_rename_generated_at_otp_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='created_at',
        ),
    ]