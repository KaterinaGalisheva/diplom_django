# Generated by Django 4.2.16 on 2024-12-09 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sign_in', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='birthdate',
        ),
    ]
