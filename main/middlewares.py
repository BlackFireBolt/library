from .models import SubCategory, Author, Topic


def repository_context_processor(request):
    choices = [*range(2001, 2023, 1)]
    context = {'authors': Author.objects.all(), 'categories': SubCategory.objects.all(), 'topics': Topic.objects.all(),
               'years': choices, 'keyword': '', 'all': ''}
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