# Generated by Django 5.1.3 on 2024-11-22 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_artist_first_name_artist_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='role',
            field=models.CharField(choices=[('artist', 'Artist'), ('editor', 'Editor'), ('admin', 'Admin')], default='artist', max_length=20),
        ),
    ]