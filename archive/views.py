from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import News, NewsImage


class NewsListView(ListView):
    model = News
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        article_list = News.objects.all()
        paginator = Paginator(article_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            article_page = paginator.page(page)
        except PageNotAnInteger:
            article_page = paginator.page(1)
        except EmptyPage:
            article_page = paginator.page(paginator.num_pages)

        context['news_list'] = article_page
        return context


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    news_image = NewsImage.objects.all()
    return render(request, 'archive/news_detail.html', {'news': news, 'news_image': news_image})