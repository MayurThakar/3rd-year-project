# Generated by Django 3.2.4 on 2021-06-25 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20210624_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='HOD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root_user', models.CharField(max_length=25)),
                ('root_paswd', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name_plural': 'HOD',
            },
        ),
    ]