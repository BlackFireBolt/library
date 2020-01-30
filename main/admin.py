from django.contrib import admin

from .models import SuperCategory, SubCategory
from .forms import SubCategoryForm
from .models import Author, Topic
from .models import Article

class SubCategoryInline(admin.TabularInline):
    model = SubCategory

class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)

admin.site.register(SuperCategory, SuperCategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm

admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Author)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    fields = ('id', 'title')

admin.site.register(Topic, TopicAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'topic', 'publication_year')
    fields = ('title', 'category', ('publication_year', 'topic'), 'description', 'isbn', 'file')
    filter_horizontal = ('author',)

 #   list_display = ('title', 'context', 'file')
 #   fields = ('title', 'context', 'file')

admin.site.register(Article)