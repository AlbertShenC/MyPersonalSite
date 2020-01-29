from django.shortcuts import render

# Create your views here.

def intro_main(request):
    return render(request, 'intro/index.html')