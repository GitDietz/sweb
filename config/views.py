from django.shortcuts import render, redirect

def home(request):
    """
    here just to get the base url to redirect to the one for lcore whihc is the lasding page
    """
    return redirect('lcore:home')
