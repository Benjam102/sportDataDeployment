# Generated by Django 5.0.4 on 2024-05-23 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fora', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threads_categories_match',
            name='slug_thread_category',
            field=models.SlugField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='threads_categories_match',
            name='slug_thread_league',
            field=models.SlugField(blank=True, max_length=600, primary_key=True, serialize=False),
        ),
    ]
