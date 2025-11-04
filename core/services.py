import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from django.utils import timezone
from dateutil.parser import parse as parse_date
from .models import Website, Article

def update_feeds_for_website(website: Website):
    """
    Belirtilen web sitesi için yayınları günceller.
    Sitenin RSS akışı varsa onu, yoksa scraping kuralını kullanır.
    """
    if website.rss_feed_url:
        _update_from_rss(website)
    elif hasattr(website, 'scraping_rule'):
        _update_from_scraping(website)

def _datetime_from_struct_time(st):
    """feedparser'dan gelen struct_time'ı datetime nesnesine çevirir."""
    dt = datetime.fromtimestamp(timezone.mktime(st))
    return timezone.make_aware(dt, timezone.get_current_timezone())

def _update_from_rss(website: Website):
    """Bir web sitesinin yayınlarını RSS akışından günceller."""
    feed = feedparser.parse(website.rss_feed_url)
    for entry in feed.entries:
        article_url = entry.get('link')
        if not article_url or Article.objects.filter(url=article_url).exists():
            continue

        published_time_struct = entry.get('published_parsed') or entry.get('updated_parsed')
        published_at = _datetime_from_struct_time(published_time_struct) if published_time_struct else timezone.now()

        Article.objects.create(
            website=website,
            title=entry.get('title', 'Başlık Yok'),
            url=article_url,
            description=entry.get('summary', ''),
            author=entry.get('author', ''),
            published_at=published_at
        )

def _update_from_scraping(website: Website):
    """Bir web sitesinin yayınlarını scraping kuralına göre günceller."""
    try:
        response = requests.get(website.url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    rule = website.scraping_rule

    for item in soup.select(rule.article_selector):
        try:
            title_element = item.select_one(rule.title_selector)
            link_element = item.select_one(rule.link_selector)

            if not title_element or not link_element:
                continue

            article_url = link_element.get('href')
            if article_url and not article_url.startswith('http'):
                article_url = urljoin(website.url, article_url)

            if not article_url or Article.objects.filter(url=article_url).exists():
                continue

            description = item.select_one(rule.description_selector).get_text(strip=True) if rule.description_selector and item.select_one(rule.description_selector) else ""
            author = item.select_one(rule.author_selector).get_text(strip=True) if rule.author_selector and item.select_one(rule.author_selector) else ""

            published_at = timezone.now()
            if rule.published_at_selector and item.select_one(rule.published_at_selector):
                date_str = item.select_one(rule.published_at_selector).get_text(strip=True)
                try:
                    published_at = parse_date(date_str)
                except (ValueError, TypeError):
                    pass # Tarih ayrıştırılamazsa varsayılanı kullanmaya devam et

            Article.objects.create(
                website=website,
                title=title_element.get_text(strip=True),
                url=article_url,
                description=description,
                author=author,
                published_at=published_at
            )
        except Exception:
            continue
