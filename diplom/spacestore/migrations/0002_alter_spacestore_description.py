# Generated by Django 4.2.16 on 2024-12-09 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacestore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spacestore',
            name='description',
            field=models.TextField(max_length=2000),
        ),
    ]