from django.urls import path

from .views import NewsListView, news_detail

app_name = 'archive'
urlpatterns = [
    path('detail/<int:pk>/', news_detail, name='news_detail'),
    path('', NewsListView.as_view(), name='archive'),
]