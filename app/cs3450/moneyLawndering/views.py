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
        #set the status = 3 because the listing is now pending
        listing.status = 3
        listing.save()
    return HttpResponseRedirect(reverse('moneyLawndering:publicListing', args=(user_id,)))

    


def myListing(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.type == 0:
        raise Http404("You are not a customer and therefore do not have access to the accepted jobs page")
    #first get all listing that are just open
    openListing = user.listing_set.filter(status=0)

    #get all listings that are pending
    applicantsList = []
    pendingListing = user.listing_set.filter(status=3)
    for listing in pendingListing:
        applicantsList.append(len(listing.applicants.all()))
    #applicantsList should be an array that has the amount of people who have applied to each listing

    #get all listings that have a worker but not completed
    acceptedListing = user.listing_set.filter(status=2)

    #get all listings that have worker that completed the job but hasnt left a review
    completedListing = user.listing_set.filter(status=4)

    pendingListingSize = []
    for i in range(len(pendingListing)):
        pendingListingSize.append(i)

    return render(request, 'moneyLawndering/myListing.html', {
            'openListing': openListing,
            'pendingListing': pendingListing,
            'pendingListingSize': pendingListingSize,
            'applicantsList': applicantsList,
            'acceptedListing': acceptedListing,
            'completedListing': completedListing,
            'user': user,
        })

def customerReview(request, listing_id, user_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing.status = 5
    listing.save()
    customer = get_object_or_404(User, pk=user_id)
    worker = get_object_or_404(User, pk=listing.worker)

    workerReview = worker.workerreview_set.create(
        customer = customer.id,
        rating = request.POST['rating'],
        description = request.POST['review']
    )
    workerReview.save()

    #reset the workers rating
    workerReviews = worker.workerreview_set.all()
    overallRating = 0
    for review in workerReviews:
        overallRating = overallRating + review.rating
    overallRating = overallRating // len(workerReviews)
    worker.rating = overallRating
    worker.save()

    return HttpResponseRedirect(reverse('moneyLawndering:myListing', args=(customer.id,)))
    
def applicantList(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    applications = listing.applicants.all()
    users = []
    for application in applications:
        users.append(User.objects.get(pk=application.worker))
    context = {'listing': listing, 'users': users}
    return render(request, "moneyLawndering/listApplicants.html", context)

def acceptApplicant(request, listing_id, user_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing.worker = user_id
    listing.status=2
    listing.save()
    return HttpResponseRedirect(reverse('moneyLawndering:myListing', args=(listing.customer.id,)))


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
    if(user.type == 1):
        raise Http404("You are not a worker and therefore do not have an accepted jobs page")
    
    #this will get all the jobs with which the worker has been accepted
    acceptedListings = Listing.objects.filter(worker=user_id, status=2)
    completedListings = Listing.objects.filter(worker=user_id, status=4)
    #this will get all jobs for which the worker has applied
    applications = AppliedFor.objects.filter(worker=user_id)
    pendingListings = []
    for application in applications:
        #this will make sure that the listing is still pending
        if application.listing.status == 3:
            pendingListings.append(application.listing)

    context = {'user': user, 
                'acceptedListings': acceptedListings, 
                'pendingListings': pendingListings ,
                'completedListings': completedListings,}
    return render(request, 'moneyLawndering/acceptedJobs.html', context)

def completedJob(request, listing_id, user_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if(listing.status == 4):
        raise Http404("You have already left a review for this person")
    listing.status = 4
    listing.save()

    worker = get_object_or_404(User, pk=user_id)
    customer = get_object_or_404(User, pk=listing.customer.id)
    admin = get_object_or_404(User, )

    #transfer the money now
    worker.accountBalance = worker.accountBalance + listing.price
    customer.accountBalance = customer.accountBalance - listing.price
    worker.save()
    customer.save()

    #add the review now
    customerReview = customer.customerreview_set.create(
        worker = worker.id,
        rating = request.POST['rating'],
        description = request.POST['review']
    )
    customerReview.save()

    #reset the customers reviews now
    customerReviews = customer.customerreview_set.all()
    overallRating = 0
    for review in customerReviews:
        overallRating = overallRating + review.rating
    overallRating = overallRating // len(customerReviews)
    customer.rating = overallRating
    customer.save()

    return HttpResponseRedirect(reverse('moneyLawndering:acceptedJobs', args=(worker.id,)))

def history(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    listings = []
    #is a customer
    if user.type== 1:
        #only get the listings that have been completed
        listings = user.listing_set.filter(status=5)
        context = {'user': user, 'listings': listings}
        return render(request, 'moneyLawndering/history.html', context)
    #is a worker
    elif user.type == 0:
        listings = Listing.objects.filter(worker=user_id, status=5)
        context = {'user': user, 'listings': listings}
        return render(request, 'moneyLawndering/history.html', context)
    #is the admin
    elif user.type == 2:
        listings = Listing.objects.all(status=5)
        context = {'user': user, 'listings': listings}
        return render(request, 'moneyLawndering/history.html', context)
    context = {'user': user, 'listings': listings}
    return render(request, 'moneyLawndering/history.html', context)


def directTransfer(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    listings = Listing.objects.filter(customer=user, status=4)
    workers = set()
    for listing in listings:
        worker = get_object_or_404(User, pk=listing.worker)
        workers.add(worker)
    context = {'user': user, 'workers': workers}
    return render(request, 'moneyLawndering/directTransfer.html', context)


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

def sendMoney(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.accountBalance -= float(request.POST['amount'])
    user.save()
    worker = get_object_or_404(User, pk=int(request.POST['worker']))
    worker.accountBalance += float(request.POST['amount'])
    worker.save()
    return HttpResponseRedirect(reverse('moneyLawndering:directTransfer', args=(user_id,)))

