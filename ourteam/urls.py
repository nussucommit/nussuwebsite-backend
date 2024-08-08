from django.urls import path
from ourteam import views

urlpatterns = [
  path('presidential/', views.presidential),
  path('relations/', views.relations),
  path('secretariat/', views.secretariat),
  path('finance/', views.finance),
  path('communications/', views.communications),
  path('studentlife/', views.studentlife),
  path('studentwelfare/', views.studentwelfare),
]
