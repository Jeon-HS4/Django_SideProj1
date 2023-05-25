from django.urls import path

from . import views

app_name ='pybo'

urlpatterns = [
    path('', views.main),
    path('', views.main, name='main'),
    path('diary/', views.main),
    path('test/', views.test, name='test'),
    
    
    path('diary/create/',
         views.diary_create, name='diary_create'),
    path('diary/detail/<str:dates><str:key>/',
         views.diary_detail, name='diary_detail'),
    path('diary/modify/<str:dates><str:key>/',
         views.diary_modify, name='diary_modify'),
    path('diary/delete/<str:dates><str:key>/',
         views.diary_delete, name='diary_delete'),

]
