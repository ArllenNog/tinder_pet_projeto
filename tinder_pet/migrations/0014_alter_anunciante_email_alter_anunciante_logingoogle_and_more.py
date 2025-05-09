# Generated by Django 5.1.5 on 2025-02-11 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0013_anunciante_logingoogle_anunciante_senha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anunciante',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='anunciante',
            name='loginGoogle',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='anunciante',
            name='nome',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='anunciante',
            name='senha',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='anunciante',
            name='telefone',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
