from django.contrib import admin
from django.urls import path
from album import views
from django.conf.urls import url, include


urlpatterns = [
    path('musicians/', views.MusicianListView.as_view()),
    path('musicians/<pk>/', views.MusicianView.as_view()),
    path('albums/', views.AlbumListView.as_view()),
    path('albums/<pk>/', views.AlbumView.as_view()),

]