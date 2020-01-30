from .models import SubCategory, Article, Author, Topic

def repository_context_processor(request):
    choices = [*range(2001, 2023, 1)]
    context = {}
    context['authors'] = Author.objects.all()
    context['categories'] = SubCategory.objects.all()
    context['topics'] = Topic.objects.all()
    context['years'] = choices
    context['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context