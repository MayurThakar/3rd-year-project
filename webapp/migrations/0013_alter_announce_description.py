# Generated by Django 3.2.4 on 2021-06-27 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20210627_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announce',
            name='description',
            field=models.TextField(max_length=255),
        ),
    ]