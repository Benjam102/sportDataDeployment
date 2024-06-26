# Generated by Django 5.0.4 on 2024-05-29 12:42

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_alter_rankings_unique_together_rankings_cle_primaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='ranks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.CharField(max_length=100, null=True)),
                ('pool', models.CharField(max_length=100, null=True)),
                ('year', models.CharField(max_length=100, null=True)),
                ('locale', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('rank', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(3)])),
                ('played', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('won', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('draw', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('lost', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('points', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('points_for', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('avg_points_for', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('points_against', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('avg_points_against', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('points_difference', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('try_for', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('try_against', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('bonus', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('att_bonus', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('def_bonus', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)])),
                ('tendency', models.CharField(max_length=100, null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='team_ranking2', to='website.teams')),
            ],
            options={
                'auto_created': False,
            },
        ),
        migrations.AddConstraint(
            model_name='ranks',
            constraint=models.UniqueConstraint(fields=('competition', 'pool', 'year', 'locale', 'rank'), name='cle_primaire_rank'),
        ),
    ]
