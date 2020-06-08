from django.contrib import admin

from .models import SuperCategory, SubCategory
from .forms import SubCategoryForm
from .models import Author, Topic, Publisher
from .models import Article


class SubCategoryInline(admin.TabularInline):
    list_display = ['name', 'slug', ]
    model = SubCategory
    prepopulated_fields = {'slug': ('name', )}


class SuperCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', ]
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(SuperCategory, SuperCategoryAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'slug',)
    prepopulated_fields = {'slug': ('last_name',)}


admin.site.register(Author, AuthorAdmin)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Publisher, PublisherAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', )
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Topic, TopicAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'topic', 'publication_year')
    fields = ('title','slug', 'category', ('publication_year', 'topic'), ('author', 'compiler'),
              ('publisher', 'publishing_house'), 'description', 'bibliographic_description', 'isbn', 'doi',
              ('file', 'image'))
    prepopulated_fields = {'slug': ('title', )}

 #   list_display = ('title', 'context', 'file')
 #   fields = ('title', 'context', 'file')


admin.site.register(Article, ArticleAdmin)

admin.site.site_header = 'Репозиторий БГАИ'