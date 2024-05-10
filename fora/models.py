from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from website.models import up_match


User = get_user_model()

# Commentaire match
class tchat_match_category(models.Model) :
    title = models.CharField(max_length=100)
    slug_title = models.SlugField(max_length=600, unique=True, blank=True)
    country = models.CharField(max_length=100, null=True)
    slug_country = models.SlugField(max_length=600, blank=True, null=True)

    def save(self, *args, **kwargs) :
        if not self.slug_title :
            self.slug_title = slugify(self.title)
        
        super(tchat_match_category, self).save(*args, **kwargs)
    
    def save(self, *args, **kwargs) :
        if not self.slug_country :
            self.slug_country = slugify(self.country)
        
        super(tchat_match_category, self).save(*args, **kwargs)

    class Meta :
        verbose_name_plural = "categories"

    def __str__(self) :
        return self.title
    
    # Number of post for each category
    @property
    def num_posts(self) :
        return tchat_match_comment.objects.filter(categories=self).count()
    
    # Date of the last post
    @property
    def last_posts(self) :
        return tchat_match_comment.objects.filter(categories=self).latest("date")

class threads(models.Model) :
    match = models.ForeignKey(up_match, on_delete=models.CASCADE)
    category = models.ForeignKey(tchat_match_category, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)

class tchat_match_comment(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(threads, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

