from django.urls import path, include
from services import views

urlpatterns = [
  path('studentfunds/', views.studentFunds),
  path('councilfunding/', views.councilFunding),
  path('resiliencefund/', views.resilienceFund),
  path('logisticsrental/', views.logisticsRental),
  path('zoomLicense/', views.zoomLicense),
  path('publicitymanagement/', include('publicity.urls')),
]