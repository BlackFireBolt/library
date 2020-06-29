from django.urls import path

from .views import ArticleListView #SearchResultsView
from .views import other_page
from .views import download
from .views import filter_page

app_name = 'main'
urlpatterns = [
    path('topic/<slug:topic_slug>/', filter_page, name='topic_filter'),
    path('kaf/<slug:category_slug>/', filter_page, name='category_filter'),
    path('author/<slug:author_slug>/', filter_page, name='author_filter'),
    path('year/<int:year>/', filter_page, name='year_filter'),
    path('<obj>/<int:pk>/', download, name='download'),
    path('<str:page>/', other_page, name='other'),
    path('', ArticleListView.as_view(), name='index'),
]
