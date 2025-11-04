from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='websites')
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    rss_feed_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=255, blank=True)
    published_at = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

class ScrapingRule(models.Model):
    website = models.OneToOneField(Website, on_delete=models.CASCADE, related_name='scraping_rule')
    article_selector = models.CharField(max_length=255, help_text="Her bir yayın bloğunu kapsayan ana CSS seçici.")
    title_selector = models.CharField(max_length=255, help_text="Başlığı içeren elementin CSS seçicisi.")
    link_selector = models.CharField(max_length=255, help_text="Yayın linkini içeren 'a' etiketinin CSS seçicisi.")
    description_selector = models.CharField(max_length=255, blank=True, help_text="Açıklamayı içeren elementin CSS seçicisi.")
    author_selector = models.CharField(max_length=255, blank=True, help_text="Yazarı içeren elementin CSS seçicisi.")
    published_at_selector = models.CharField(max_length=255, blank=True, help_text="Yayın tarihini içeren elementin CSS seçicisi.")

    def __str__(self):
        return f"Scraping kuralı: {self.website.name}"
