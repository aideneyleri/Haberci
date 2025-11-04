from django import forms
from .models import Website, ScrapingRule

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'url', 'rss_feed_url']
        labels = {
            'name': 'Site Adı',
            'url': 'Site URL',
            'rss_feed_url': 'RSS Akış URL (varsa)'
        }
        help_texts = {
            'rss_feed_url': 'Eğer bu alan boş bırakılırsa, scraping kuralları tanımlamanız gerekecektir.'
        }

class ScrapingRuleForm(forms.ModelForm):
    class Meta:
        model = ScrapingRule
        fields = ['article_selector', 'title_selector', 'link_selector', 'description_selector', 'author_selector', 'published_at_selector']
        labels = {
            'article_selector': 'Yayın Ana Seçicisi',
            'title_selector': 'Başlık Seçicisi',
            'link_selector': 'Link Seçicisi',
            'description_selector': 'Açıklama Seçicisi',
            'author_selector': 'Yazar Seçicisi',
            'published_at_selector': 'Yayın Tarihi Seçicisi'
        }
