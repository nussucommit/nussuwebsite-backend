from django.urls import path
from contact import views

urlpatterns = [
  path('', views.contact),
  path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
]
