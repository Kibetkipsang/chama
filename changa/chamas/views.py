from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect  
from .models import Chama, ChamaMembership
from .forms import ChamaForm
from django.contrib import messages


class ChamaCreateView(LoginRequiredMixin, CreateView):
    model = Chama
    form_class = ChamaForm
    template_name = 'create_chama.html'
    success_url = reverse_lazy('dashboard') 

    def form_valid(self, form):
        response = super().form_valid(form)
      
        ChamaMembership.objects.create(
            user=self.request.user,
            chama=self.object,
            role='chairperson'
        )
        messages.success(self.request, "Your chama was created successfully!")
        return response

    
