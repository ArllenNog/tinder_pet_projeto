# Generated by Django 5.1.5 on 2025-02-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0004_rename_raca_raca_racas_remove_pet_idtipo_raca_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='tipo',
            field=models.SmallIntegerField(default=0),
        ),
    ]
