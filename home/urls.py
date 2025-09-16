from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('programming-hub/', views.programming_hub_view, name='program_hub'),
    path("python-child-1/", views.python_child_1_view, name="python_child_1"),
    #path("python-runner/", views.python_runner, name="python_runner"),

]
