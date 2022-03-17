from ctypes import addressof
import email
from django.utils import timezone
from unicodedata import category, name
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
        address = request.POST['address']
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
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email, password=password)
    except(KeyError, User.DoesNotExist):
        return render(request, 'moneyLawndering/signin.html', {'error_message' : 'Email and/or Password doesn\'t correspond to any existing user'})
    else:
        if user.isAdmin():
            return HttpResponseRedirect(reverse('moneyLawndering:admin', args=(user.id,)))
        else:
            return HttpResponseRedirect(reverse('moneyLawndering:account', args=(user.id,)))

def updateUser(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.phoneNumber = request.POST['phoneNumber']
    user.address = request.POST['address']
    user.accountBalance = request.POST['accountBalance']
    user.save()
    return HttpResponseRedirect(reverse('moneyLawndering:account', args=(user.id,)))


def account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, 'moneyLawndering/account.html', context)

def publicListing(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if(user.type == 1):
        response = {
        "failure": "You are not a worker and do not have access to this page",
        "user_id": user_id,
        "user_name": user.name,
        "isCustomer": user.type,
        }
        response = JsonResponse(response)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    #this means that they are not a worker
    listings = Listing.objects.all()
    listings.exclude(status=1)
    listings.exclude(status=2)
    listings.exclude(status=4)
    #we might want to order the listing by date created
    context = {'listings' : listings,
                'user': user}
    return render(request, 'moneyLawndering/publicListing.html', context)

def acceptListing(request, user_id, listing_id):
    #first make sure that they have posted a listing
    try:
        listing = Listing.objects.get(pk=listing_id)
    except(KeyError, Listing.DoesNotExist) :
        raise Http404("Listing does not exist here jose")
    listing = Listing.objects.get(pk=listing_id)
    try:
        listing.applicants.get(worker=user_id)
    except(KeyError, AppliedFor.DoesNotExist) :
        listing.applicants.create(worker=user_id)
    return HttpResponseRedirect(reverse('moneyLawndering:publicListing', args=(user_id,)))

    


def myListing(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        listings = []
        if (user.isWorker):
            listings = Listing.objects.get(worker=user_id)
        else:
            listings = user.listing_set.all()
    except (KeyError, Listing.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'moneyLawndering/myListing.html', {
            'no_listing': "You currently have no listings",
            'user_id': user_id,
            'user': user,
        })
    return render(request, 'moneyLawndering/myListing.html', {
            'listings': listings,
            'user_id': user_id,
            'user': user,
        })

def createListing(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    categories = Category.objects.all()
    return render(request, "moneyLawndering/createListing.html", {'user':user, 'categories':categories})

def newListing(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try:
        if user.isCustomer:
            category = request.POST['category']
            location = request.POST['location']
            time_est = request.POST['time_est']
            dayOfWeek = request.POST['dayOfWeek']
            startTimeOfDay = request.POST['startTime']
            endTimeOfDay = request.POST['endTime']
            description = request.POST['description']
            price = request.POST['price']
            status = 0
            pubDate = timezone.now()
            listing = user.listing_set.create(category=category, location=location,
                                time_est=time_est, dayOfWeek=dayOfWeek, startTimeOfDay=startTimeOfDay, 
                                endTimeOfDay=endTimeOfDay, description=description, price=price,
                                status=status, pubDate=pubDate, worker=0)
            
            listing.save()
    except:
        response = {
        "failure": "You sent an invalid listing and it could not create it",
        "category": category,
        "location": location,
        "time_est": time_est,
        "dayOfWeek": dayOfWeek,
        "StartTime": startTimeOfDay,
        "EndTime": endTimeOfDay,
        "Description": description,
        "price": price,
        "status": status,
        "pubDate": pubDate,
        "user_id": user_id,
        }
        response = JsonResponse(response)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return HttpResponseRedirect(reverse('moneyLawndering:myListing', args=(user.id,)))


def acceptedJobs(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, 'moneyLawndering/acceptedJobs.html', context)

def directTransfer(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, 'moneyLawndering/directTransfer.html', context)

def history(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    listings = Listing.objects.all()
    listings.exclude(status=0)
    listings.exclude(status=2)
    listings.exclude(status=3)
    listing_status = ['Open', 'Closed', 'Accepted', 'Pending', 'Completed']
    for listing in listings:
        listing.status = listing_status[listing.status]
    context = {'user': user, 'listings': listings}
    return render(request, 'moneyLawndering/history.html', context)

def admin(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    users = User.objects.all()
    user_types = ['Worker', 'Customer', 'Admin']
    for u in users:
        u.type = user_types[u.type]

    listings = Listing.objects.all()
    listing_status = ['Open', 'Closed', 'Accepted', 'Pending', 'Completed']
    for listing in listings:
        listing.status = listing_status[listing.status]
    context = {'user': user, 'users': users, 'listings': listings}
    return render(request, 'moneyLawndering/admin.html', context)

