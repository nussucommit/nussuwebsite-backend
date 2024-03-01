from django.urls import path
from joinus import views

urlpatterns = [
  path('', views.joinus)
]