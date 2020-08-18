import pathlib
from django.conf import settings as conf_settings
from django.db import connection
from django.http import FileResponse
from django.shortcuts import render, redirect

from .models import Services, Reference, Article, Category, Tag, Feature, Skill


def get_base_context():
    service_list = Services.objects.top_five()
    company = Reference.objects.get(primary=1)
    co_name = company.company
    co_addr = company.address
    co_country = company.country
    co_phone = company.phone
    co_email = company.email
    print(co_name)
    return {'service_list': service_list,
            'co_name': co_name,
            'co_addr': co_addr,
            'co_country': co_country,
            'co_phone': co_phone,
            'co_email': co_email,
    }


def base(request):
    template = "base.html"
    context = {}
    return render(request, template, context)


def blog(request):
    template = "blog.html"
    active_articles = Article.objects.visible()
    recent_articles = Article.objects.recent_five()
    active_tags = Tag.objects.active() #change to used
    with connection.cursor() as cursor:
        cursor.execute("Select C.name, count(C.name) as cat_count from lcore_article_category as JJ inner join lcore_category C on JJ.category_id = C.id group by name;")
        columns = [col[0] for col in cursor.description]
        category_count = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    local_context = {
        'articles': active_articles,
        'recent_articles': recent_articles,
        'active_tags': active_tags,
        'category_count': category_count
    }

    context = {**get_base_context(), **local_context}
    print(context)
    return render(request, template, context)


def home(request):
    template = "home.html"
    services = Services.objects.all()[:6]
    local_context = {
        'services': services,
    }

    context = {**get_base_context(), **local_context}
    print(context)
    return render(request, template, context)


def pdf(request):
    # TODO set up to take redirect to display all blog_article files
    root = pathlib.Path(conf_settings.MEDIA_ROOT)
    file_path = pathlib.Path.joinpath(root,'blog_image','Email_processing.pdf')
    print(f'{file_path}')
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def show_pdf(request, pk):
    root = pathlib.Path(conf_settings.MEDIA_ROOT)
    try:
        article = Article.objects.get(pk=pk)
        filename = str(article.article_file)
    except:
        return redirect('lcore:blog')
    if filename == '':
        return redirect('lcore:blog')
    file_path = pathlib.Path.joinpath(root, filename)
    print(f'{file_path}')
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def services(request):
    template = "services.html"
    services = Services.objects.all()[:6]
    features = Feature.objects.active()[:8]
    local_context = {
        'services': services,
        'features': features,
    }

    context = {**get_base_context(), **local_context}
    return render(request, template, context)


def about(request):
    template = "about.html"
    services = Services.objects.all()[:6]
    features = Feature.objects.active()[:8]
    skill = Skill.objects.active()
    local_context = {
        'services': services,
        'features': features,
        'skill': skill,
    }

    context = {**get_base_context(), **local_context}
    return render(request, template, context)
