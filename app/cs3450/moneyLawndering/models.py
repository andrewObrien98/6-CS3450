from django.db import models
import datetime
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    type = models.IntegerField()  # 0 for worker, 1 for customer, 2 for admin
    password = models.CharField(max_length=200)
    phoneNumber = models.IntegerField()
    address = models.CharField(max_length=200)
    accountBalance = models.FloatField()
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.name

    def isWorker(self):
        return self.type == 0

    def isCustomer(self):
        return self.type == 1

    def isAdmin(self):
        return self.type == 2
    


class Listing(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    time_est = models.FloatField()
    dayOfWeek = models.CharField(max_length=100)
    startTimeOfDay = models.CharField(max_length=100)
    endTimeOfDay = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    status = models.IntegerField()  # 0=open, 1=closed, 2=accepted, 3=pending, 4=completedForWorker 5=completedForCustomer
    worker = models.IntegerField()
    workerPhoneNumber = models.IntegerField()
    workername = models.CharField(max_length=100)
    pubDate = models.DateTimeField('date published')

    def __str__(self):
        return self.customer.name

    def wasPublishedRecently(self):
        return self.pubDate >= timezone.now() - datetime.timedelta(days=1)

    def isOpen(self):
        return self.status == 0

    def isClosed(self):
        return self.status == 1

    def isAccepted(self):
        return self.status == 2

    def isPending(self):
        return self.status == 3

    def isCompleted(self):
        return self.status == 4

    
    

class AppliedFor(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="applicants")
    worker = models.IntegerField()


#reviews left by the worker for the customer
class CustomerReview(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    worker = models.IntegerField()
    rating = models.IntegerField()
    description = models.TextField()


#reviews left by the customer for the worker
class WorkerReview(models.Model):
    customer = models.IntegerField()
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()


class Category(models.Model):
    type = models.CharField(max_length=300)

    def __str__(self):
        return self.type
