# Generated by Django 5.1.5 on 2025-02-13 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0014_alter_anunciante_email_alter_anunciante_logingoogle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anunciante',
            name='telefone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='anunciante',
            name='whatsapp',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
