from django.contrib import admin
from .models import tchat_match_comment, tchat_match_category, threads

admin.site.register(tchat_match_comment)
admin.site.register(tchat_match_category)
admin.site.register(threads)
