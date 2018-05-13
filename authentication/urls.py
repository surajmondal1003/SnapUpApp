from django.contrib import admin
from django.urls import path
from authentication import views
from .views import UserCreate
from django.conf.urls import url, include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('create_user',views.UserCreate.as_view()),

]