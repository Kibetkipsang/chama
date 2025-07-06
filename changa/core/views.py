from django.shortcuts import render
from django.views.generic import TemplateView

# landing page
class LandingPageView(TemplateView):

    template_name = 'landing.html'
