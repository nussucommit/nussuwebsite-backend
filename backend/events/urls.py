from django.urls import path
from events import views

urlpatterns = [
  path('events/', views.events)
]