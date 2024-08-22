from django.urls import path
from publicity import views

urlpatterns = [
  path('page-1/', views.pageOne),
  path('page-2/', views.pageTwo),
]
