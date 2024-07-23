from django.db import models

# Model import
from django.contrib.auth import get_user_model
from website.models import matches

# Useful library
from django.utils.text import slugify  # to create slug

User = get_user_model()

"""
-> All our classes are inherited from the django model class

-> Explanation of the code used in each model :
    * class Meta :
            Django will add an 's' to the end of the class name to make it plural when displayed in the administration interface. 
            To avoid having 2 s following each other, I decided to choose its name.
    * def save(self, *args, **kwargs) :
            Override of the save method to generate automatically a slug (part of url)
"""
 
# Tchat
class tchats(models.Model) :
    """
    This class allows us to define tchats (general, irish, french...) 
    
    """
    tchat_category = models.CharField(max_length=100, null=True)
    slug_tchat_category = models.SlugField(max_length=600, blank=True, null=True)
    tchat_name = models.CharField(max_length=100, null=True)
    slug_tchat_name = models.SlugField(max_length=600, blank=True, primary_key=True)  # Primary key

    def save(self, *args, **kwargs) :
        if not self.slug_tchat_category :
            self.slug_tchat_category = slugify(self.tchat_category)
        
        if not self.slug_tchat_name :
            self.slug_tchat_name = slugify(self.tchat_name)
        
        super(tchats, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "tchats"

class tchat_posts(models.Model) :
    """
    This class allows us to define posts for each tchat and each user 
    """
    # Primary key auto-generated
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tchat = models.ForeignKey(tchats, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "tchat_posts"

# Thread for a match
class threads_categories_match(models.Model) :
    """
    This class allows us to define leagues (top 14, prodD2...) and categories (club, international, other) for the threads.
    """
    thread_league = models.CharField(max_length=100, null=True)
    slug_thread_league = models.SlugField(max_length=600, blank=True, primary_key=True)
    thread_category = models.CharField(max_length=100, null=True)
    slug_thread_category = models.SlugField(max_length=600, blank=True, null=True)

    def save(self, *args, **kwargs) :
        if not self.slug_thread_league :
            self.slug_thread_league = slugify(self.thread_league)

        if not self.slug_thread_category :
            self.slug_thread_category = slugify(self.thread_category)
        
        super(threads_categories_match, self).save(*args, **kwargs)

    class Meta :
        verbose_name_plural = "threads_categories_match"

class threads_match(models.Model) :
    """
    This class allows us to define a thread for each match.
    """
    key_id = models.SlugField(max_length=600, primary_key=True) 
    category = models.ForeignKey(threads_categories_match, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
    
class threads_comments_match(models.Model) :
    """
    This class allows us to define comments for each thread and and related to a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(threads_match, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "threads_comments_match"

