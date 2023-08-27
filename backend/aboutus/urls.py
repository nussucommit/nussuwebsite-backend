from django.urls import path
from aboutus import views

urlpatterns = [
  path('aboutus/', views.aboutus),
  path('history/', views.history),
  path('governance/', views.governance),
  path('ourteam/', views.ourteam),
  path('president/', views.president),
]
