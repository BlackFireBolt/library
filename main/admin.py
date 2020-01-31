from django.contrib import admin

from .models import SuperCategory, SubCategory
from .forms import SubCategoryForm
from .models import Author, Topic, Publisher
from .models import Article

class SubCategoryInline(admin.TabularInline):
    model = SubCategory

class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)

admin.site.register(SuperCategory, SuperCategoryAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Author, AuthorAdmin)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Publisher, PublisherAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Topic, TopicAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'topic', 'publication_year')
    fields = ('title', 'category', ('publication_year', 'topic'), ('author', 'compiler'), 
             ('publisher', 'publishing_house'), 'description', 'bibliographic_description','isbn', ('file', 'image'))

 #   list_display = ('title', 'context', 'file')
 #   fields = ('title', 'context', 'file')

admin.site.register(Article, ArticleAdmin)

admin.site.site_header = 'Репозиторий БГАИ'