from haystack import indexes
from .models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    category = indexes.CharField(model_attr='category', null=True)
    author = indexes.MultiValueField()
    topic = indexes.CharField(model_attr='topic')
    description = indexes.CharField(model_attr='description')
    bibliographic_description = indexes.CharField(model_attr='bibliographic_description')
    publishing_house = indexes.CharField(model_attr='publishing_house')
    isbn = indexes.CharField(model_attr='isbn')
    publication_year = indexes.IntegerField(model_attr='publication_year')
    keywords = indexes.CharField(model_attr='keywords')

    def prepare_author(self, object):
        return [author.last_name for author in object.author.all()]

    def get_model(self):
        return Article
