#home/views.py======================================
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core import serializers          
import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from .models import Student, Exam, ResultSheet
from django.utils import timezone

def index(request):
    return render(request, 'home/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def programming_hub_view(request):
    return render(request, 'home/programming/program_hub.html')
def python_child_1_view(request):
    return render(request, "home/programming/python_child_1.html")

def python_runner(request):
    return render(request, "home/programming/python_runner.html")
def django_minor_details_view(request):
    return render(request, 'home/programming/djn_minor_details.html')
def user_auth_tutorial_view(request):
    return render(request, "home/programming/user_auth.html")
def ban_ara_eng_layout(request):
    return render(request,'home/programming/latex/layout_1.html')
