# Generated by Django 5.1.5 on 2025-02-03 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anunciante',
            name='endereco',
        ),
    ]
