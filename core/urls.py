from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView,
    HomeView,
    WebsiteListView,
    MarkArticleAsReadView,
    WebsiteCreateView,
    WebsiteUpdateView,
    WebsiteDeleteView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # Website CRUD
    path('websites/', WebsiteListView.as_view(), name='website-list'),
    path('websites/new/', WebsiteCreateView.as_view(), name='website-create'),
    path('websites/<int:pk>/edit/', WebsiteUpdateView.as_view(), name='website-update'),
    path('websites/<int:pk>/delete/', WebsiteDeleteView.as_view(), name='website-delete'),

    # Article actions
    path('article/<int:pk>/mark-as-read/', MarkArticleAsReadView.as_view(), name='mark-as-read'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
