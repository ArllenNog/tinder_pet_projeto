# Generated by Django 5.1.5 on 2025-02-14 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder_pet', '0015_alter_anunciante_telefone_alter_anunciante_whatsapp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anuncio',
            name='foto1',
        ),
        migrations.RemoveField(
            model_name='anuncio',
            name='foto2',
        ),
        migrations.RemoveField(
            model_name='anuncio',
            name='foto3',
        ),
        migrations.RemoveField(
            model_name='anuncio',
            name='foto4',
        ),
        migrations.RemoveField(
            model_name='anuncio',
            name='fotoDestaqueURL',
        ),
        migrations.AddField(
            model_name='anuncio',
            name='titulo',
            field=models.TextField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='foto1',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='foto2',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='foto3',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='foto4',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='fotoDestaque',
            field=models.URLField(null=True),
        ),
    ]
