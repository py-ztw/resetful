from django.contrib import admin
from django.urls import path

from apps import views

urlpatterns = [
    path('user/', views.user),
    path('users/', views.Userview.as_view()),
    path('users/<str:pk>/', views.Userview.as_view()),
    path("students/", views.StudentView.as_view()),
    path("students/<str:pk>/", views.StudentView.as_view()),
    path("employees/", views.EmployeeAPIView.as_view()),
    path("employees/<str:id>/", views.EmployeeAPIView.as_view()),

]
