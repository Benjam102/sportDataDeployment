from django.contrib import admin
from .models import tchats, tchat_posts, threads_categories_match, threads_match, threads_comments_match

# Tchat
admin.site.register(tchats)
admin.site.register(tchat_posts)

# Match threads
admin.site.register(threads_categories_match)
admin.site.register(threads_match)
admin.site.register(threads_comments_match)
