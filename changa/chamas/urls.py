from django.urls import path
from .views import ChamaCreateView

urlpatterns = [
    path('create/', ChamaCreateView.as_view(), name="create-chama"),
]
