from django.db import models

# Model import
from website.models import matches
from django.contrib.auth import get_user_model

# Useful library
from django.core.validators import MaxValueValidator

User = get_user_model()

class predictions_matches(models.Model):
    """
    This class allows us to memorize the prediction of a user.
    
    """
    prediction_match = models.ForeignKey(matches, on_delete=models.PROTECT, null=True)
    user_prediction = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    prediction_margin1 = models.IntegerField(validators=[MaxValueValidator(3)], null=True)
    prediction_margin2 = models.IntegerField(validators=[MaxValueValidator(3)], null=True)
    prediction_total1 = models.IntegerField(validators=[MaxValueValidator(3)], null=True)
    prediction_total2 = models.IntegerField(validators=[MaxValueValidator(3)], null=True)
