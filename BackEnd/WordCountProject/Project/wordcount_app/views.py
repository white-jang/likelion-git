from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def result(request):
    text = request.GET['text']
    return render(request, 'result.html', {'text': text})