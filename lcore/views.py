import logging
import pathlib
from django.conf import settings as conf_settings
from django.contrib import messages
from django.core.cache import cache
from django.db import connection
from django.http import FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from .emailer import send_email
from .forms import ContactForm
from .models import Services, Reference, Article, Category, Tag, Feature, Skill


logger = logging.getLogger('db')


def get_base_context():
    service_list = Services.objects.top_five()
    if cache.get('co_name'):
        logger.info('cache exists')
    else:
        logger.info('no cache')
        company = Reference.objects.get(primary=1)
        cache.set('co_name', company.company, 60 * 60)
        cache.set('co_addr', company.address, 60 * 60)
        cache.set('co_country', company.country, 60 * 60)
        cache.set('co_phone', company.phone, 60 * 60)
        cache.set('co_email', company.email, 60 * 60)

    co_name = cache.get('co_name')
    co_addr = cache.get('co_addr')
    co_country = cache.get('co_country')
    co_phone = cache.get('co_phone')
    co_email = cache.get('co_email')

    logger.info(co_name)
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
    """
    General blog page with summary of blogs and links to individuals
    """
    template = "blog.html"
    active_articles = Article.objects.visible()
    recent_articles = Article.objects.recent_five()
    active_tags = Tag.objects.active()  # change to used
    with connection.cursor() as cursor:
        sql = ("Select C.name, count(C.name) as cat_count from lcore_article_category as JJ inner join"
               " lcore_category C on JJ.category_id = C.id group by name;")
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        category_count = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    page = request.GET.get('page', 1)
    paginator = Paginator(active_articles, 5)
    try:
        article_page = paginator.page(page)
    except PageNotAnInteger:
        article_page = paginator.page(1)
    except EmptyPage:
        article_page = paginator.page(paginator.num_pages)

    local_context = {
        'articles': article_page,
        'recent_articles': recent_articles,
        'active_tags': active_tags,
        'category_count': category_count
    }

    context = {**get_base_context(), **local_context}
    return render(request, template, context)


def blog_item(request, pk):
    """
    more detail on the specific blog item to read the more detailed description
    :param request:
    :param pk:for Article
    :return: render
    """
    try:
        article = Article.objects.get(pk=pk)

    except:
        return redirect('lcore:blog')
    template = "blog_detail.html"

    if article.extract != article.story:
        story_extract_differ = True
    local_context = {
        'article': article,
        'story_extract_differ': story_extract_differ,
    }

    context = {**get_base_context(), **local_context}
    return render(request, template, context)


def home(request):
    template = "home.html"
    services = Services.objects.all()[:6]
    local_context = {
        'services': services,
    }

    context = {**get_base_context(), **local_context}
    return render(request, template, context)


def pdf(request):
    """
    Testing view for a PDF file
    """
    root = pathlib.Path(conf_settings.MEDIA_ROOT)
    file_path = pathlib.Path.joinpath(root, 'blog_image', 'Email_processing.pdf')
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
    # print(f'{file_path}')
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


def contact(request):
    """ process the form to send the email for enquiry """
    form = ContactForm()
    send_status = 2
    template_name = 'contact_page.html'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            body = f'Enquiry from {data.get("full_name")}, regarding {data.get("content")}'
            email_kwargs = {'email': data.get('email'),
                            'subject': data.get('subject'),
                            'full_name': data.get('full_name'),
                            'content': body,
                            }
            send_result, sender = send_email(**email_kwargs)
            if send_result != 0:
                messages.error(request, f"Your email could not be sent, please email us direct on {sender}")
                send_status = 1
            else:
                messages.success(request, "Your email was successfully sent")
                send_status = 0

    local_context = {
        'form': form,
        'send_status': send_status,
    }

    context = {**get_base_context(), **local_context}
    return render(request, template_name, context)


def terms(request):
    template = "terms.html"
    local_context = {
      'title': 'Website terms and conditions'
    }

    context = {**get_base_context(), **local_context}
    return render(request, template, context)


def privacy(request):
    template = "privacy.html"
    local_context = {
      'title': 'Website terms and conditions'
    }

    context = {**get_base_context(), **local_context}
    return render(request, template, context)
