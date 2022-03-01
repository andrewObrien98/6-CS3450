from django.db import models
import datetime
from django.utils import timezone
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    type = models.IntegerField() # 0 for worker or 1 for customer
    password = models.CharField(max_length=200)
    phoneNumber = models.IntegerField()
    address = models.CharField(max_length=200)
    accountBalance = models.IntegerField()
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.name

    def isWorker(self):
        return self.type == 0

    def isCustomer(self):
        return self.type == 1
    


class Listing(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customerListing')
    category = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    time_est = models.FloatField()
    dayOfWeek = models.CharField(max_length=10)
    startTimeOfDay = models.FloatField()
    endTimeOfDay = models.FloatField()
    description = models.TextField()
    price = models.IntegerField()
    status = models.IntegerField() #0=open, 1=closed, 2=accepted, 3=pending, 4=completed
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workerListing')
    pubDate = models.DateTimeField('date published')

    def __str__(self):
        return self.customer

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
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customerAppliedFor')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workerAppliedFor')

    def __str__(self):
        return self.worker + ' applied for ' + self.customer + ' job'

#reviews left by the worker for the customer
class CustomerReview(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customerCR')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workerCR')
    rating = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.worker + ' left a review for ' + self.customer

#reviews left by the customer for the worker
class WorkerReview(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customerWR')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workerWR')
    rating = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.customer + ' left a review for ' + self.worker

class Category(models.Model):
    type = models.CharField(max_length=300)

    def __str__(self):
        return self.type
