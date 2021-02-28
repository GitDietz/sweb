from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views

from .views import about, base, blog, blog_item, contact, home, pdf, privacy, services, show_pdf, terms

app_name = 'lcore'
urlpatterns = [
    path('about', about, name='about'),
    re_path('article/(?P<pk>\d+)', show_pdf, name='show_pdf'),
    path('base', base, name='base'),
    path('contact', contact, name='contact'),
    path('blog', blog, name='blog'),
    re_path('blog_item/(?P<pk>\d+)', blog_item, name='blog_item'),
    path('home', home, name='home'),
    path('pdf', pdf, name='pdf'),
    path('privacy', privacy, name='privacy'),
    path('services', services, name='services'),
    path('terms', terms, name='terms'),
    ]
