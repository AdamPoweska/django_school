from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='hello'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    # path('login/', LoginView.as_view(), name='login'),
    path('user_page/', views.UserPage.as_view(), name='user_page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:action>/<str:model_name>/<int:pk>/', views.DynamicModelView.as_view(), name='dynamic_model_view'), # używam już 'as_view()' w widokach
    path('<str:action>/<str:model_name>/', views.DynamicModelView.as_view(), name='dynamic_model_view'),
]
