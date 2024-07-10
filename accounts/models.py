from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class favourites(models.Model) :
    """
    This class allows us to define posts for each tchat and each user 
    """
    name_competition = models.CharField(max_length=100, null=True)
    slug_competition = models.SlugField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs) :
        if not self.slug_competition :
            self.slug_competition = slugify(self.name_competition)
        
        super(favourites, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "favourites"