from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

from .views import base, blog, home

app_name = 'lcore'
urlpatterns = [
    # path("home", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path('base', base, name='base'),
    path('blog', blog, name='blog'),
    path('home', home, name='home'),
    ]
