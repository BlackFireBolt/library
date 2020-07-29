import django_filters

from .models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ('category', 'author', 'topic', 'publication_year', 'description', 'title')
