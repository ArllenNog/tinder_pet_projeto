# Generated by Django 5.1.5 on 2025-02-04 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0005_pet_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuncio',
            name='dataPublicacao',
            field=models.DateField(null=True),
        ),
    ]
