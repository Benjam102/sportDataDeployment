from django.db import models
from django.utils.text import slugify

class up_match(models.Model):
    # Choix possibles pour le statut du match.
    # Chaque choix est une paire (valeur_en_base_de_données, étiquette_affichée).
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),      
        ('In progress', 'In progress'),     
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    team_home = models.CharField(max_length=100, null=True, blank=True)
    team_away = models.CharField(max_length=100, null=True, blank=True)
    score_home = models.CharField(max_length=20, null=True, blank=True)
    score_away = models.CharField(max_length=20, null=True, blank=True)
    referee = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    hour = models.TimeField(null=True, blank=True)
    stade_name = models.CharField(max_length=100, null=True, blank=True)
    league = models.CharField(max_length=100, null=True, blank=True)
    phase = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    humidity = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    pressure = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)         # ground pressure
    precipitation = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    wind_speed = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    code = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    code_url = models.CharField(max_length=100, null=True, blank=True)
    neutrality = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(max_length=600, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
                team_names = f"{self.team_home}-{self.team_away}"
                date = self.date.replace("/", "-")
                slug = f"{team_names}-{date}"
                self.slug = slugify(slug)
        super().save(*args, **kwargs)


class past_match(models.Model) :
    STATUS_CHOICES = [
        ('Cancelled', 'Cancelled'),      
        ('Finished', 'Finished'),     
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    team_home = models.CharField(max_length=100, null=True, blank=True)
    team_away = models.CharField(max_length=100, null=True, blank=True)
    score_home = models.CharField(max_length=20, null=True, blank=True)
    score_away = models.CharField(max_length=20, null=True, blank=True)
    referee = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    hour = models.TimeField(null=True, blank=True)
    stade_name = models.CharField(max_length=100, null=True, blank=True)
    league = models.CharField(max_length=100, null=True, blank=True)
    phase = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    humidity = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    pressure = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)         # ground pressure
    precipitation = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    wind_speed = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    code = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    code_url = models.CharField(max_length=100, null=True, blank=True)
    neutrality = models.IntegerField(null=True, blank=True)


class players(models.Model) :
    first_last_name = models.CharField(max_length=200, null=True, blank=True)
    nationality1 = models.CharField(max_length=100, null=True, blank=True)
    nationality2 = models.CharField(max_length=100, null=True, blank=True)
    sporting_nationality = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    club = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    tenure_tenure = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    ratio_match = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    nb_min_played = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    unavailability_date = models.DateField(null=True, blank=True)
    unavailability_reason = models.CharField(max_length=200, null=True, blank=True)


class Team(models.Model) :
    club_name = models.CharField(max_length=100, null=True, blank=True)
    city_club = models.CharField(max_length=100, null=True, blank=True)