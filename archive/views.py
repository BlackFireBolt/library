from django.shortcuts import render

from.models import News


def news_detail(request, pk):
    news = News.objects.get(pk=pk)
    return render(request, {'news': news})