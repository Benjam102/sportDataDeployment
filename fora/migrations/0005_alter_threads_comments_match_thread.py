# Generated by Django 5.0.4 on 2024-07-23 10:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fora', '0004_thread_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threads_comments_match',
            name='thread',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='fora.thread_match'),
        ),
    ]
