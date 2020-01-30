from django.urls import path

from .views import ArticleListView, SearchResultsView
from .views import other_page
from .views import download
from .views import category_filter, year_filter, topic_filter, author_filter
from .models import Article

app_name = 'main'
urlpatterns = [
    path('topic/<str:topic>/', topic_filter, name='topic_filter'),
    path('kaf/<str:category>/', category_filter, name='category_filter'),
    path('author/<str:author>/', author_filter, name='author_filter'),
    path('year/<int:year>/', year_filter, name='year_filter'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('<obj>/<int:pk>/', download, name='download'),
    path('<str:page>/', other_page, name='other'),
    path('', ArticleListView.as_view(), name='index'),
]
