from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist, Library, Node
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
import mimetypes
from storages.backends.sftpstorage import SFTPStorage

from .models import SubCategory, Article, Topic, Author, Category
from .forms import SearchForm
from .filters import ArticleFilter
 
sfs = SFTPStorage()

def download(request, obj=None, pk=None):
    try:
        obj_download = Article.objects.get(id=pk)
    except Article.DoesNotExist:
        raise Http404 
       
    if sfs.exists(obj_download.file.name):
        file = sfs._read(obj_download.file.name)
        type, encoding = mimetypes.guess_type(obj_download.file.name)
        response = HttpResponse(file, content_type=type)
        response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
            filename=obj_download.file.name)
        return response
    raise Http404

class ArticleListView(ListView):
    model = Article
    template_name = 'main/index.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs) 
        article_list = Article.objects.all()
        paginator = Paginator(article_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            article_page = paginator.page(page)
        except PageNotAnInteger:
            article_page = paginator.page(1)
        except EmptyPage:
            article_page = paginator.page(paginator.num_pages)

        context['article_list'] = article_page
        context['authors'] = Author.objects.all()
        context['categories'] = SubCategory.objects.all()
        return context

def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class SearchResultsView(ListView):
    model = Article
    template_name = 'main/search.html'
    paginate_by = 12

    def get_queryset(self): 
        query = self.request.GET.get('q')
        search_vector = SearchVector('category__name', 'author__name', 'topic__title', 'publication_year', 'description', 'title')
        object_list = Article.objects.annotate(search=search_vector).filter(search=query)
        paginator = Paginator(object_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            search_page = paginator.page(page)
        except PageNotAnInteger:
            search_page = paginator.page(1)
        except EmptyPage:
            search_page = paginator.page(paginator.num_pages)

        return search_page

def topic_filter(request, topic):
    topic_filter = Topic.objects.get(title=topic)
    articles = Article.objects.filter(topic=topic_filter)
    paginator = Paginator(articles, 12)

    page = request.GET.get('page')

    try:
        topic_filter_list = paginator.page(page)
    except PageNotAnInteger:
        topic_filter_list = paginator.page(1)
    except EmptyPage:
        topic_filter_list = paginator.page(paginator.num_pages)
    
    context = {'topic_filter_list': topic_filter_list, 'topic': topic}
    return render(request, 'main/topic_list.html', context)

def author_filter(request, author):
    author_filter = Author.objects.get(name=author)
    articles = Article.objects.filter(author=author_filter)
    paginator = Paginator(articles, 12)

    page = request.GET.get('page')

    try:
        author_filter_list = paginator.page(page)
    except PageNotAnInteger:
        author_filter_list = paginator.page(1)
    except EmptyPage:
        author_filter_list = paginator.page(paginator.num_pages)
    
    context = {'author_filter_list': author_filter_list, 'author': author}
    return render(request, 'main/author_list.html', context)

def year_filter(request, year):
    articles = Article.objects.filter(publication_year=year)
    paginator = Paginator(articles, 12)

    page = request.GET.get('page')

    try:
        year_filter_list = paginator.page(page)
    except PageNotAnInteger:
        year_filter_list = paginator.page(1)
    except EmptyPage:
        year_filter_list = paginator.page(paginator.num_pages)
    
    context = {'year_filter_list': year_filter_list, 'year': year}
    return render(request, 'main/year_list.html', context)

def category_filter(request, category):
    category_filter = Category.objects.get(name=category)
    categories = Article.objects.filter(category=category_filter)
    paginator = Paginator(categories, 12)

    page = request.GET.get('page')

    try:
        category_filter_list = paginator.page(page)
    except PageNotAnInteger:
        category_filter_list = paginator.page(1)
    except EmptyPage:
        category_filter_list = paginator.page(paginator.num_pages)
    
    context = {'category_filter_list': category_filter_list, 'category': category}
    return render(request, 'main/category_list.html', context)