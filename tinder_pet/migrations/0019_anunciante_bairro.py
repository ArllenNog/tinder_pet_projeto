# Generated by Django 5.1.5 on 2025-02-21 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0018_rename_desc_anuncio_texto_remove_anuncio_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='anunciante',
            name='bairro',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
