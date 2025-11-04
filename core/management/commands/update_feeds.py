from django.core.management.base import BaseCommand
from core.models import Website
from core.services import update_feeds_for_website

class Command(BaseCommand):
    help = 'Tüm aktif web sitelerinin yayın akışlarını günceller.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Yayın akışları güncelleniyor...'))

        active_websites = Website.objects.filter(is_active=True)

        for website in active_websites:
            self.stdout.write(f'"{website.name}" sitesi güncelleniyor...')
            try:
                update_feeds_for_website(website)
                self.stdout.write(self.style.SUCCESS(f'"{website.name}" başarıyla güncellendi.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'"{website.name}" güncellenirken bir hata oluştu: {e}'))

        self.stdout.write(self.style.SUCCESS('Tüm yayın akışları güncellendi.'))
