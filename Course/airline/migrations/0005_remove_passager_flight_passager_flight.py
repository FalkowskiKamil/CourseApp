# Generated by Django 4.1.7 on 2023-03-18 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0004_alter_passager_flight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passager',
            name='flight',
        ),
        migrations.AddField(
            model_name='passager',
            name='flight',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passagers', to='airline.flight'),
        ),
    ]