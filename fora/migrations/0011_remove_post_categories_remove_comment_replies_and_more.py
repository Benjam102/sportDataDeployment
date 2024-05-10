# Generated by Django 5.0.4 on 2024-05-02 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fora', '0010_remove_threads_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='replies',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='user',
        ),
        migrations.DeleteModel(
            name='category',
        ),
        migrations.DeleteModel(
            name='comment',
        ),
        migrations.DeleteModel(
            name='post',
        ),
        migrations.DeleteModel(
            name='reply',
        ),
    ]
