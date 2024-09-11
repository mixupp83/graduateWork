from django.contrib import admin
from .models import Article, Profile
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'content')
    list_filter = ('pub_date',)
    search_fields = ('title', 'content')

admin.site.register(Article, ArticleAdmin)

admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)