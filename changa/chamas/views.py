from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect  # Added this import
from .models import Chama, ChamaMembership
from .forms import ChamaForm


# lets a logged in user create a chama
class ChamaCreateView(LoginRequiredMixin, CreateView):
    model = Chama
    form_class = ChamaForm
    template_name = 'create_chama.html'
    success_url = reverse_lazy('my-chamas')

    def form_valid(self, form):
        response = super().form_valid(form)  
        ChamaMembership.objects.create(
            user=self.request.user,
            chama=self.object,
            role='chairperson'
        )
        return response  
    
