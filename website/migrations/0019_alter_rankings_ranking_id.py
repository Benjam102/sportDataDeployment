# Generated by Django 5.0.4 on 2024-05-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_remove_rankings_id_rankings_ranking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankings',
            name='ranking_id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
