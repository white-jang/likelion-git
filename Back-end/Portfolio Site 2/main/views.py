from django.shortcuts import render, get_object_or_404, redirect
from .models import Content

# Create your views here.
def home(request):
    contents = Content.objects.all()
    return render(request, 'home.html', {'contents':contents})

# def detail(request, port_id):
#     contents = get_object_or_404(Content, pk=port_id)
#     return render(request, 'detail.html', {'contents':contents})