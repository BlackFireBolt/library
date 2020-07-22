from django.contrib import admin

from .models import News, NewsImage


class NewsImageInline(admin.TabularInline):
    list_display = ['name', 'slug', ]
    model = NewsImage


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    inlines = (NewsImageInline,)


admin.site.register(News, NewsAdmin)