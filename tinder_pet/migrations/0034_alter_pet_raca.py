# Generated by Django 5.1.5 on 2025-04-09 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0033_pet_castrado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='raca',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tinder_pet.raca'),
        ),
    ]
