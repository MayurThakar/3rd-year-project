# Generated by Django 3.2.4 on 2021-06-27 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_alter_announce_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announce',
            name='time',
        ),
        migrations.AlterField(
            model_name='announce',
            name='date',
            field=models.DateField(),
        ),
    ]
