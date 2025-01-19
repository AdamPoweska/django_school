# Create your views here.

from django.http import HttpResponse    
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
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


class BaseListView(ListView):
    model = None # model jest przekazany w klasie pochodnej
    template_name = None


class BaseCreateView(CreateView):
    model = None
    fields = '__all__'
    template_name = None
    success_url = reverse_lazy


class DynamicModelView(View):
    # Dictionary with all MODELS
    models = {
        'school_adress': SchoolAdress,
        'director': Director,
        'lesson': Lesson,
        'teacher': Teacher,
        'student': Student,
        'teacher_lesson_student': TeacherLessonStudent,
        'grade': Grade,
        'school': School,
    }
    # HTML templatki - nie muszę już tworzyć osobnych urli, nie jest to wymagane
    templates = {
        'create': 'model_create.html', # Create
        'list': 'model_list.html', # Read
        'update': 'model_update.html', # Update
        'delete': 'model_delete.html', # Delete
    }
    # Actions - Class Based Views
    actions = {
        'create': CreateView,
        'list': ListView,
        'update': UpdateView,
        'delete': DeleteView,
    }

    success_url = reverse_lazy('user_page')

    def dispatch(self, request, *args, **kwargs):
        action = kwargs.get('action')
        model_name = kwargs.get('model_name')
        pk = kwargs.get('pk')

        view_class = self.actions.get(action) # view based on action
        view_model = self.models.get(model_name) # as abowe - we fetch right model based on 'model_name' passed from urls (urls gets it form html)
        view_template = self.templates.get(action)

        if not view_class or not view_model:
            return HttpResponse("Błędna akcja, lub niewłaściwy model", status=400)
        
        class DynamicHeaders(view_class):
            model = view_model
            template_name = view_template
            success_url = self.success_url

            if action == "create":
                fields = '__all__'

            def get_context_data(inner_self, **inner_kwargs):
                context = super().get_context_data(**inner_kwargs)
                context['headers'] = [field.verbose_name for field in view_model._meta.fields]

                object_list = context.get('object_list', [])
                if object_list:
                    context['object_fields'] = [[getattr(obj, field.name) for field in view_model._meta.fields] for obj in object_list]
                else:
                    context['object_fields'] = []

                return context
        
        view = DynamicHeaders.as_view()
        
        # view = view_class.as_view(
        #     model=view_model,
        #     template_name=view_template,
        #     success_url=self.success_url,
        # )

        if action in ['update', 'delete'] and pk: # jeśli akcja to 'update" lub 'delete' i zawiera przekazane pk
            # obj = view_model.objects.filter(pk=pk).first() # zapytanie do bazy danych 'objects.filter' używając pk, które zwraca 'queryset'. Następnie 'first()' zwraca pierwszy pasujący wynik z tego queryset'u (zgodny z kryteriami). Jeśli queryste jest pusty to zwróci 'None' (w przeciwieństwie do '.get(pk=pk)' - które w razie błędu zwróci "DoesNotExist" error. First jest łatwiejsze do obsługi).
            obj = get_object_or_404(view_model, pk=pk)
            if not obj:
                return HttpResponse("Obiekt nie odnaleziony", status=404)
            return view(request, pk=obj.pk)

        return view(request)