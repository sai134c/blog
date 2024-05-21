from django.urls import path
from . import views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pid>/', views.post_detail, name='post_detail'),
    path('new/', views.post_new, name='post_new'),
    path('<int:pid>/edit/',views.post_edit, name = 'post_edit')
]