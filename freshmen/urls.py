from django.urls import path
from freshmen import views

urlpatterns = [
  path('', views.freshmen)
]