from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect
from .models import Article, Website, ScrapingRule
from .forms import WebsiteForm, ScrapingRuleForm

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('core:login')
    template_name = 'core/signup.html'

class HomeView(LoginRequiredMixin, generic.ListView):
    model = Article
    template_name = 'core/home.html'
    context_object_name = 'articles'
    paginate_by = 20
    def get_queryset(self):
        return Article.objects.filter(website__user=self.request.user).order_by('-published_at')

class WebsiteListView(LoginRequiredMixin, generic.ListView):
    model = Website
    template_name = 'core/website_list.html'
    context_object_name = 'websites'
    def get_queryset(self):
        return Website.objects.filter(user=self.request.user).order_by('name')

class WebsiteCreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'core/website_form.html'

    def get(self, request, *args, **kwargs):
        website_form = WebsiteForm()
        scraping_rule_form = ScrapingRuleForm()
        return self.render_to_response({'website_form': website_form, 'scraping_rule_form': scraping_rule_form})

    def post(self, request, *args, **kwargs):
        website_form = WebsiteForm(request.POST)
        scraping_rule_form = ScrapingRuleForm(request.POST)
        if website_form.is_valid():
            website = website_form.save(commit=False)
            website.user = request.user
            website.save()
            if not website.rss_feed_url and scraping_rule_form.is_valid():
                scraping_rule = scraping_rule_form.save(commit=False)
                scraping_rule.website = website
                scraping_rule.save()
            return redirect('core:website-list')
        return self.render_to_response({'website_form': website_form, 'scraping_rule_form': scraping_rule_form})

class WebsiteUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'core/website_form.html'

    def test_func(self):
        website = get_object_or_404(Website, pk=self.kwargs['pk'])
        return website.user == self.request.user

    def get(self, request, *args, **kwargs):
        website = get_object_or_404(Website, pk=self.kwargs['pk'])
        website_form = WebsiteForm(instance=website)
        scraping_rule_form = ScrapingRuleForm(instance=getattr(website, 'scraping_rule', None))
        return self.render_to_response({'website_form': website_form, 'scraping_rule_form': scraping_rule_form})

    def post(self, request, *args, **kwargs):
        website = get_object_or_404(Website, pk=self.kwargs['pk'])
        website_form = WebsiteForm(request.POST, instance=website)
        scraping_rule_form = ScrapingRuleForm(request.POST, instance=getattr(website, 'scraping_rule', None))
        if website_form.is_valid():
            website = website_form.save()
            if not website.rss_feed_url and scraping_rule_form.is_valid():
                scraping_rule, created = ScrapingRule.objects.get_or_create(website=website)
                scraping_rule_form_instance = ScrapingRuleForm(request.POST, instance=scraping_rule)
                if scraping_rule_form_instance.is_valid():
                    scraping_rule_form_instance.save()
            return redirect('core:website-list')
        return self.render_to_response({'website_form': website_form, 'scraping_rule_form': scraping_rule_form})

class WebsiteDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Website
    template_name = 'core/website_confirm_delete.html'
    success_url = reverse_lazy('core:website-list')

    def test_func(self):
        return self.get_object().user == self.request.user

class MarkArticleAsReadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article_id = self.kwargs.get('pk')
        try:
            article = Article.objects.get(pk=article_id, website__user=request.user)
            article.is_read = True
            article.save()
            return JsonResponse({'status': 'success'})
        except Article.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Article not found'}, status=404)
