# Generated by Django 4.1.7 on 2023-03-18 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0007_alter_passager_flights'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passager',
            name='flights',
        ),
    ]