# Generated by Django 5.1.3 on 2024-11-22 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_artist_alias'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='genre',
        ),
    ]
