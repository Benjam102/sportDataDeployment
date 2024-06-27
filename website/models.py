from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator
from django.db.models import UniqueConstraint

class teams(models.Model) :
    name = models.CharField(max_length=100, primary_key=True) # Primary key: name
    logo = models.CharField(max_length=200, null=True)
    club = models.CharField(max_length=100, null=True)
    national = models.IntegerField(validators=[MaxValueValidator(4)], null=True) 
    competition1 = models.CharField(max_length=100, null=True)
    competition2 = models.CharField(max_length=100, null=True)
    competition3 = models.CharField(max_length=100, null=True)
    stadium1 = models.CharField(max_length=100, null=True)
    stadium2 = models.CharField(max_length=100, null=True)
    stadium3 = models.CharField(max_length=100, null=True)

class matches(models.Model):
    key_id = models.SlugField(max_length=600, primary_key=True) # Primary key: slug
    status = models.CharField(max_length=50, null=True)
    home_team = models.ForeignKey(teams, related_name='home_team_matches', on_delete=models.PROTECT)
    away_team = models.ForeignKey(teams, related_name='away_team_matches', on_delete=models.PROTECT)
    home_score = models.IntegerField(validators=[MaxValueValidator(3)], null=True) 
    away_score = models.IntegerField(validators=[MaxValueValidator(3)], null=True) 
    referee = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    kickoff = models.TimeField(null=True)
    stadium = models.CharField(max_length=100, null=True)
    competition = models.CharField(max_length=100, null=True)
    phase = models.CharField(max_length=100, null=True)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    pressure = models.FloatField(null=True)
    precipitation = models.FloatField(null=True)
    wind_speed = models.FloatField(null=True)
    weather_code = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug_match_id:
                team_names = f"{self.team_home}-{self.team_away}"
                date = self.date.replace("/", "-")
                slug = f"{team_names}-{date}"
                self.slug_match_id = slugify(slug)
        super().save(*args, **kwargs)


class odds(models.Model) :
    key_id = models.SlugField(max_length=600, primary_key=True) # Primary key: slug
    date = models.DateField(null=True)
    hour = models.TimeField(null=True)
    home_team = models.ForeignKey(teams, related_name='home_team_odds', on_delete=models.PROTECT)
    away_team = models.ForeignKey(teams, related_name='away_team_odds', on_delete=models.PROTECT)
    home_odds = models.FloatField(null=True)
    away_odds = models.FloatField(null=True)
    draw_odds = models.FloatField(null=True)
    probable_score_diff = models.FloatField(null=True)
    total_point = models.FloatField(null=True)


class rankings(models.Model) :
    ranking_id = models.CharField(max_length=200, primary_key=True)
    competition = models.CharField(max_length=100, null=True)
    pool = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=100, null=True)
    locale = models.IntegerField(validators=[MaxValueValidator(4)], null=True) 
    rank = models.IntegerField(validators=[MaxValueValidator(3)], null=True) 
    team = models.ForeignKey(teams, related_name='team_ranking', on_delete=models.PROTECT)
    played = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    won = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    draw = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    lost = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    points = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    points_for = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    avg_points_for = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    points_against = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    avg_points_against = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    points_difference = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    try_for = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    try_against = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    bonus = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    att_bonus = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    def_bonus = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    tendency = models.CharField(max_length=100, null=True)

    # Manière d'avoir une clé primaire composite (pas vraiment une clé primaire)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['competition', 'pool', 'year', 'locale', 'rank'], name='cle_primaire')
        ]

class players(models.Model) :
    player_id = models.SlugField(max_length=600, primary_key=True) # Primary key: slug
    name = models.CharField(max_length=100, null=True)
    nationality = models.CharField(max_length=100, null=True)
    nationality2 = models.CharField(max_length=100, null=True)
    sport_nationality = models.CharField(max_length=100, null=True)
    age = models.IntegerField(validators=[MaxValueValidator(3)], null=True)
    height = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    weight = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    club = models.CharField(max_length=100, null=True)
    position = models.CharField(max_length=100, null=True)
    percentage = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    ratio = models.CharField(max_length=100, null=True)
    minute_played = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    unavailability = models.DateField(null=True)
    unavailability_motiv = models.CharField(max_length=200, null=True)
    picture = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=600, null=True)


class compositions(models.Model) :
    comp_id = models.CharField(max_length=600, primary_key=True) # Primary key: slug
    key_id = models.SlugField(max_length=600, null=True) 
    local_team = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    player1 = models.ForeignKey(players, related_name='compo_player1', null=True, blank=True, on_delete=models.PROTECT)
    player2 = models.ForeignKey(players, related_name='compo_player2', null=True, blank=True, on_delete=models.PROTECT)
    player3 = models.ForeignKey(players, related_name='compo_player3', null=True, blank=True, on_delete=models.PROTECT)
    player4 = models.ForeignKey(players, related_name='compo_player4', null=True, blank=True, on_delete=models.PROTECT)
    player5 = models.ForeignKey(players, related_name='compo_player5', null=True, blank=True, on_delete=models.PROTECT)
    player6 = models.ForeignKey(players, related_name='compo_player6', null=True, blank=True, on_delete=models.PROTECT)
    player7 = models.ForeignKey(players, related_name='compo_player7', null=True, blank=True, on_delete=models.PROTECT)
    player8 = models.ForeignKey(players, related_name='compo_player8', null=True, blank=True, on_delete=models.PROTECT)
    player9 = models.ForeignKey(players, related_name='compo_player9', null=True, blank=True, on_delete=models.PROTECT)
    player10 = models.ForeignKey(players, related_name='compo_player10', null=True, blank=True, on_delete=models.PROTECT)
    player11 = models.ForeignKey(players, related_name='compo_player11', null=True, blank=True, on_delete=models.PROTECT)
    player12 = models.ForeignKey(players, related_name='compo_player12', null=True, blank=True, on_delete=models.PROTECT)
    player13 = models.ForeignKey(players, related_name='compo_player13', null=True, blank=True, on_delete=models.PROTECT)
    player14 = models.ForeignKey(players, related_name='compo_player14', null=True, blank=True, on_delete=models.PROTECT)
    player15 = models.ForeignKey(players, related_name='compo_player15', null=True, blank=True, on_delete=models.PROTECT)
    player16 = models.ForeignKey(players, related_name='compo_player16', null=True, blank=True, on_delete=models.PROTECT)
    player17 = models.ForeignKey(players, related_name='compo_player17', null=True, blank=True, on_delete=models.PROTECT)
    player18 = models.ForeignKey(players, related_name='compo_player18', null=True, blank=True, on_delete=models.PROTECT)
    player19 = models.ForeignKey(players, related_name='compo_player19', null=True, blank=True, on_delete=models.PROTECT)
    player20 = models.ForeignKey(players, related_name='compo_player20', null=True, blank=True, on_delete=models.PROTECT)
    player21 = models.ForeignKey(players, related_name='compo_player21', null=True, blank=True, on_delete=models.PROTECT)
    player22 = models.ForeignKey(players, related_name='compo_player22', null=True, blank=True, on_delete=models.PROTECT)
    player23 = models.ForeignKey(players, related_name='compo_player23', null=True, blank=True, on_delete=models.PROTECT)
    player24 = models.ForeignKey(players, related_name='compo_player24', null=True, blank=True, on_delete=models.PROTECT)
    player25 = models.ForeignKey(players, related_name='compo_player25', null=True, blank=True, on_delete=models.PROTECT)

    # Manière d'avoir une clé primaire composite (pas vraiment une clé primaire)
    class Meta:
        unique_together = ('key_id', 'local_team')

class sources(models.Model) :
    image_url = models.CharField(max_length=200, null=True)
    image_source = models.CharField(max_length=200, null=True)

class substitution(models.Model) :
    sub_id = models.CharField(max_length=600, primary_key=True)  # Clé primaire
    key_id = models.SlugField(max_length=600, null=True)
    local_team = models.IntegerField(validators=[MaxValueValidator(4)], null=True)

    player_in1 = models.ForeignKey(players, related_name='player_in1', null=True, blank=True, on_delete=models.PROTECT)
    player_out1 = models.ForeignKey(players, related_name='player_out1', null=True, blank=True, on_delete=models.PROTECT)
    sub_time1 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in2 = models.ForeignKey(players, related_name='player_in2', null=True, blank=True, on_delete=models.PROTECT)
    player_out2 = models.ForeignKey(players, related_name='player_out2', null=True, blank=True, on_delete=models.PROTECT)
    sub_time2 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in3 = models.ForeignKey(players, related_name='player_in3', null=True, blank=True, on_delete=models.PROTECT)
    player_out3 = models.ForeignKey(players, related_name='player_out3', null=True, blank=True, on_delete=models.PROTECT)
    sub_time3 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in4 = models.ForeignKey(players, related_name='player_in4', null=True, blank=True, on_delete=models.PROTECT)
    player_out4 = models.ForeignKey(players, related_name='player_out4', null=True, blank=True, on_delete=models.PROTECT)
    sub_time4 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in5 = models.ForeignKey(players, related_name='player_in5', null=True, blank=True, on_delete=models.PROTECT)
    player_out5 = models.ForeignKey(players, related_name='player_out5', null=True, blank=True, on_delete=models.PROTECT)
    sub_time5 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in6 = models.ForeignKey(players, related_name='player_in6', null=True, blank=True, on_delete=models.PROTECT)
    player_out6 = models.ForeignKey(players, related_name='player_out6', null=True, blank=True, on_delete=models.PROTECT)
    sub_time6 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in7 = models.ForeignKey(players, related_name='player_in7', null=True, blank=True, on_delete=models.PROTECT)
    player_out7 = models.ForeignKey(players, related_name='player_out7', null=True, blank=True, on_delete=models.PROTECT)
    sub_time7 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in8 = models.ForeignKey(players, related_name='player_in8', null=True, blank=True, on_delete=models.PROTECT)
    player_out8 = models.ForeignKey(players, related_name='player_out8', null=True, blank=True, on_delete=models.PROTECT)
    sub_time8 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in9 = models.ForeignKey(players, related_name='player_in9', null=True, blank=True, on_delete=models.PROTECT)
    player_out9 = models.ForeignKey(players, related_name='player_out9', null=True, blank=True, on_delete=models.PROTECT)
    sub_time9 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in10 = models.ForeignKey(players, related_name='player_in10', null=True, blank=True, on_delete=models.PROTECT)
    player_out10 = models.ForeignKey(players, related_name='player_out10', null=True, blank=True, on_delete=models.PROTECT)
    sub_time10 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in11 = models.ForeignKey(players, related_name='player_in11', null=True, blank=True, on_delete=models.PROTECT)
    player_out11 = models.ForeignKey(players, related_name='player_out11', null=True, blank=True, on_delete=models.PROTECT)
    sub_time11 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)
    
    player_in12 = models.ForeignKey(players, related_name='player_in12', null=True, blank=True, on_delete=models.PROTECT)
    player_out12 = models.ForeignKey(players, related_name='player_out12', null=True, blank=True, on_delete=models.PROTECT)
    sub_time12 = models.IntegerField(validators=[MaxValueValidator(4)], null=True)