# Generated by Django 4.1.7 on 2023-03-18 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0006_remove_passager_flight_passager_flights_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passager',
            name='flights',
            field=models.ManyToManyField(related_name='lol', to='airline.flight'),
        ),
    ]
