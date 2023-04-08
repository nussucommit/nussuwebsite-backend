from django.urls import path
from aboutus import views

urlpatterns = [
  path('aboutus/', views.aboutus),
]
