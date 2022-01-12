from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('select/', views.select, name='select'),
    path('result/', views.result, name='result'),
    # url 맵핑 규칙
    # path('select/<int:year>/', .., ..),
]