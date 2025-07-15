from django.urls import path
from .views import ChamaCreateView

urlpatterns = [
    path('create-chama/', ChamaCreateView.as_view(), name="create-chama"),
]
