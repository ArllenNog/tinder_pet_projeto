# Generated by Django 5.1.5 on 2025-04-17 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0035_alter_pet_raca'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anunciante',
            old_name='querAdotar',
            new_name='emailConfirmado',
        ),
    ]
