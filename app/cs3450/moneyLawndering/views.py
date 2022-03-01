from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse

from moneyLawndering.models import User, Listing, AppliedFor, CustomerReview, WorkerReview, Category

def index(request):
    return render(request, 'moneyLawndering/signup.html')

def signup(request):
    return render(request, 'moneyLawndering/signup.html')

def signin(request):
    return render(request, 'moneyLawndering/signin.html')

def account(request, user_id):
    return render(request, 'moneyLawndering/account.html')

def publicListing(request):
    return render(request, 'moneyLawndering/publicListing.html')

def myListing(request, user_id):
    return render(request, 'moneyLawndering/myListing.html')

def newListing(request):
    return render(request, 'moneyLawndering/newListing.html')

def acceptedJobs(request, user_id):
    return render(request, 'moneyLawndering/acceptedJobs.html')

def directTransfer(request, user_id):
    return render(request, 'moneyLawndering/directTransfer.html')

def history(request, user_id):
    return render(request, 'moneyLawndering/history.html')

