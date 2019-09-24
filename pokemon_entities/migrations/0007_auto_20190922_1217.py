# Generated by Django 2.2.5 on 2019-09-22 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20190921_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='description',
            field=models.TextField(blank=True, max_length=10000, null=True, verbose_name='описание'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='наименование англ'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='title_jp',
            field=models.CharField(max_length=200, null=True, verbose_name='наименование яп'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='img_url',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='изображение'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='наименование рус'),
        ),
    ]
