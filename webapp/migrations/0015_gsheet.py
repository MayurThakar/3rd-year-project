# Generated by Django 3.2.4 on 2021-06-30 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_auto_20210627_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gsheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheetID', models.CharField(max_length=50)),
                ('sheetNAME', models.CharField(max_length=10)),
            ],
        ),
    ]
