from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect("start")
    return render(request, 'home/index.html')

@login_required
def start(request):
    return render(request, 'home/start.html')