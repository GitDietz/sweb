from django.shortcuts import render

# Create your views here.
def base(request):
    template = "basen.html"
    context = {}
    return render(request, template, context)
