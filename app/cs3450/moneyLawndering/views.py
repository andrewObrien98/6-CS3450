from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the Moneylawndering index.")

def signup(request):
    return HttpResponse("Hello, world. You're at the Moneylawndering singup.")

def signin(request):
    return HttpResponse("Hello, world. You're at the Moneylawndering signin.")

def account(request, user_id):
    return HttpResponse("Hello, world. You're at the Moneylawndering account.")

def publicListing(request):
    return HttpResponse("Hello, world. You're at the Moneylawndering index.")

def myListing(request, user_id):
    return HttpResponse("Hello, world. You're at the Moneylawndering index.")

def newListing(request):
    return HttpResponse("Hello, world. You're at the Moneylawndering index.")

def acceptedJobs(request, user_id):
    return HttpResponse("Hello, world. You're at the Moneylawndering index.")

def directTransfer(request, user_id):
    return HttpResponse("Hello, world. You're at the Moneylawndering index.")

def history(request, user_id):
    return HttpResponse("Hello, world. You're at the Moneylawndering index.")

