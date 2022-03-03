from ctypes import addressof
import email
from unicodedata import name
from django.forms import PasswordInput
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse

from moneyLawndering.models import User, Listing, AppliedFor, CustomerReview, WorkerReview, Category

def index(request):
    return render(request, 'moneyLawndering/signin.html')

def signup(request):
    return render(request, 'moneyLawndering/signup.html')

def createUser(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except(KeyError, User.DoesNotExist) :
        name = request.POST['name']
        email = request.POST['email']
        type = request.POST['type']
        password = request.POST['password']
        phoneNumber = request.POST['phoneNumber']
        address = request.POST['addess']
        accountBalance = request.POST['accountBalance']
        user = User(
            name = name,
            email = email,
            type = type,
            password = password,
            phoneNumber = phoneNumber,
            address = address,
            accountBalance = accountBalance,
        )
        user.save()
        return HttpResponseRedirect(reverse('moneyLawndering:account', args=(user.id,)))
    else:
        response = {
        "error": "User with corresponding email already exists",
        }
        response = JsonResponse(response)
        response['Access-Control-Allow-Origin'] = '*'
        return response


def signin(request):
    try:
        email = request.GET['email']
        password = request.GET['password']
        user = User.objects.get(email=email, password=password)
    except(KeyError, User.DoesNotExist):
        return render(request, 'moneyLawndering/signin.html', {'error_message' : 'Email or Password dont correspsond to any existing user'})
    else:
        return HttpResponseRedirect(reverse('moneyLawndering:account', args=(user.id,)))

def account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, 'moneyLawndering/account.html', context)

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

