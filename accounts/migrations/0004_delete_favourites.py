# Generated by Django 5.0.4 on 2024-07-10 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='favourites',
        ),
    ]
