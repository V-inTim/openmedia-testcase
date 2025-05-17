import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup

from .models import Page

ORDER_PARAMS = {
    '-h1': 'h1_count',
    '-h2': 'h2_count',
    '-h3': 'h3_count',
    'h1': '-h1_count',
    'h2': '-h2_count',
    'h3': '-h3_count',
}


@csrf_exempt
def parse_view(request):
    """Метод парсинга и сохранения страницы."""
    if request.method != 'POST':
        return JsonResponse(
            {'error': f'Метод {request.method} не поддерживаетcя'},
            status=405,
        )
    url = request.POST.get('url')
    if not url:
        return JsonResponse({'error': "Необходим параметр url"}, status=400)

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    h1_count = len(soup.find_all('h1'))
    h2_count = len(soup.find_all('h2'))
    h3_count = len(soup.find_all('h3'))
    a_links = [link.get('href') for link in soup.find_all('a')]

    page = Page.objects.create(
        url=url,
        h1_count=h1_count,
        h2_count=h2_count,
        h3_count=h3_count,
        a_links=a_links,
    )
    page.save()
    return JsonResponse(data={'id': page.id}, status=201)


def get_page_view(request, pk):
    """Метод получения страницы по id."""
    if request.method != 'GET':
        return JsonResponse(
            {'error': f'Метод {request.method} не поддерживается'},
            status=405,
        )

    try:
        page = Page.objects.get(pk=pk)
        return JsonResponse(
            data={
                'h1': page.h1_count,
                'h2': page.h2_count,
                'h3': page.h3_count,
                'a': page.a_links,
            },
            status=200,
        )
    except Page.DoesNotExist:
        return JsonResponse(
            {'error': "Страницы с таким id не существует"},
            status=404,
        )


def get_all_pages_view(request):
    """Метод получения всех страниц."""
    if request.method != 'GET':
        return JsonResponse(
            {'error': f'Метод {request.method} не поддерживается'},
            status=405,
        )
    order = request.GET.get('order')

    queryset = Page.objects.all()
    if order:
        if not ORDER_PARAMS.get(order):
            return JsonResponse(
                {'error': 'Некорректное значение order'},
                status=400,
            )
        queryset = queryset.order_by(ORDER_PARAMS.get(order))
    else:
        queryset = queryset.order_by('created_at')
    queryset = queryset.only('h1_count', 'h2_count', 'h3_count', 'a_links')

    response_data = [
        {
            'h1': page.h1_count,
            'h2': page.h2_count,
            'h3': page.h3_count,
            'a': page.a_links,
        }
        for page in queryset
    ]
    return JsonResponse(
        data=response_data,
        safe=False,
        status=200,
    )
