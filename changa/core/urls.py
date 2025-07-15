from django.urls import path
from .views import LandingPageView,DashboardView

urlpatterns = [
    path('', LandingPageView.as_view(), name= 'home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
