from django.urls import path

from .views import parse_view, get_page_view, get_all_pages_view

urlpatterns = [
    path('create', parse_view, name='create_page'),
    path('<int:pk>', get_page_view, name='get_page'),
    path('list', get_all_pages_view, name='get_page_list'),
]
