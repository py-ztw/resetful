from django.contrib import admin
from django.urls import path

from day4homeworkapp import views

urlpatterns = [

    path("students1/", views.StudentsAPIVIew.as_view()),
    path("students1/<str:pk>/", views.StudentsAPIVIew.as_view()),


]
