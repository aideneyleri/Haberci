from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Website, Article, ScrapingRule

class ScrapingRuleInline(admin.StackedInline):
    model = ScrapingRule
    can_delete = False
    verbose_name_plural = 'Scraping Kuralı'

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'url', 'is_active', 'created_at')
    list_filter = ('is_active', 'user')
    search_fields = ('name', 'url')
    inlines = (ScrapingRuleInline,)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'website', 'published_at', 'is_read')
    list_filter = ('is_read', 'website')
    search_fields = ('title', 'url')
    date_hierarchy = 'published_at'

# Django'nun varsayılan Group modelini admin panelinden kaldırıyoruz.
admin.site.unregister(Group)
