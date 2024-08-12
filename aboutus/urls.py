from django.urls import path, include
from aboutus import views

urlpatterns = [
  path('aboutus/', views.aboutus),
  path('history/', views.history),
  path('governance/', views.governance),
  path('ourteam/', include('ourteam.urls')),
  path('president/', views.president),
]
