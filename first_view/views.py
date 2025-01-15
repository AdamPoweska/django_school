# Create your views here.

from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, TemplateView, ListView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .models import * # using * in import allows to import all functions from given file

class HomeView(TemplateView):
    template_name = 'hello.html'

class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    # success_url = '/user_page/'
    # next_page = 'user_page.html'
    # redirect_authenticated_user = False
    redirect_authenticated_user = True
    success_url = reverse_lazy('user_page')

class UserPage(TemplateView):
    template_name = 'user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['is_director'] = user.groups.filter(name="Dyrektor").exists()
        context['is_teacher'] = user.groups.filter(name="Teacher").exists()
        context['is_student'] = user.groups.filter(name="Student").exists()

        return context