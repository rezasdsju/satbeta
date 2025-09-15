from django.shortcuts import render

# Home page view
def index(request):
    return render(request, 'home/index.html')
