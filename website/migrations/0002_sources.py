# Generated by Django 5.0.4 on 2024-05-23 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='sources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=200, null=True)),
                ('image_source', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
