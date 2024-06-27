# Generated by Django 5.0.4 on 2024-05-29 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_alter_compositions_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='compositions',
            name='comp_id',
            field=models.CharField(default=None, max_length=600, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='compositions',
            name='key_id',
            field=models.SlugField(max_length=600, null=True),
        ),
    ]