# Generated by Django 2.2.6 on 2019-10-08 19:32

from django.db import migrations


def remove_null(apps, schema_editor):
    Pokemon = apps.get_model("pokemon_entities", "Pokemon")
    for pokemon in Pokemon.objects.all():
        if not pokemon.description:
            pokemon.description = ''
        if not pokemon.img_file:
            pokemon.img_file = ''
        if not pokemon.title_ru:
            pokemon.title_ru = ''
        if not pokemon.title_en:
            pokemon.title_en = ''
        if not pokemon.title_jp:
            pokemon.title_jp = ''
        pokemon.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0015_auto_20191008_2218'),
    ]

    operations = [
        migrations.RunPython(remove_null),
    ]
