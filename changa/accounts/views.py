from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Profile
from django.shortcuts import redirect

class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully, you can now log in.")
        return super().form_valid(form)
    
class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Log in the user
        response = super().form_valid(form)
        # Force redirect to profile instead of next=
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('profile')

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name= 'profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile
