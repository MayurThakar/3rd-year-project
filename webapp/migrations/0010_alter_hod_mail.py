# Generated by Django 3.2.4 on 2021-06-25 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_hod_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hod',
            name='mail',
            field=models.EmailField(max_length=254),
        ),
    ]