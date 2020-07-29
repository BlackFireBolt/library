from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
import mimetypes
from storages.backends.sftpstorage import SFTPStorage
from haystack.generic_views import SearchView

from .models import Article, Topic, Author, Category
from archive.models import NewsImage
 
sfs = SFTPStorage()


def download(request, obj=None, pk=None):
    obj_download = None
    if obj == 'Article':
        try:
            obj_download = Article.objects.get(id=pk)
        except Article.DoesNotExist:
            raise Http404
    elif obj == 'NewsImage':
        try:
            obj_download = NewsImage.objects.get(id=pk)
        except NewsImage.DoesNotExist:
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
        return context


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class SearchResultsViewOLD(ListView):
    model = Article
    template_name = 'search/search.html'
    paginate_by = 12

    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = Article.objects.search(query)
        paginator = Paginator(object_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            articles_list = paginator.page(page)
        except PageNotAnInteger:
            articles_list = paginator.page(1)
        except EmptyPage:
            articles_list = paginator.page(paginator.num_pages)

        return articles_list


class SearchResultsView(SearchView):
    template_name = 'search/search.html'
    paginate_by = 12


def build_page(self):
    paginator = Paginator(self.queryset, self.paginate_by)
    page = self.request.GET.get('page')

    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    return object_list


def filter_page(request, topic_slug=None, category_slug=None, author_slug=None, year=None):
    filter_object = None
    articles = Article.objects.all()
    filter_type = None
    filter_object_name = None
    if category_slug:
        filter_object = Category.objects.get(slug=category_slug)
        articles = Article.objects.filter(category=filter_object)
        filter_object_name = filter_object.name
        filter_type = 'kaf'
        filter_object = filter_object.slug
    elif year:
        filter_object = year
        articles = Article.objects.filter(publication_year=filter_object)
        filter_type = 'year'
        filter_object_name = filter_object
    elif author_slug:
        filter_object = Author.objects.get(slug=author_slug)
        articles = Article.objects.filter(author=filter_object)
        filter_type = 'author'
        filter_object_name = filter_object
        filter_object = filter_object.slug
    elif topic_slug:
        filter_object = Topic.objects.get(slug=topic_slug)
        articles = Article.objects.filter(topic=filter_object)
        filter_type = 'topic'
        filter_object_name = filter_object
        filter_object = filter_object.slug
    paginator = Paginator(articles, 12)

    page = request.GET.get('page')

    try:
        articles_list = paginator.page(page)
    except PageNotAnInteger:
        articles_list = paginator.page(1)
    except EmptyPage:
        articles_list = paginator.page(paginator.num_pages)

    context = {'articles_list': articles_list, 'filter_object': filter_object, 'filter_object_name': filter_object_name,
               'filter_type': filter_type}
    return render(request, 'main/filter_page.html', context)