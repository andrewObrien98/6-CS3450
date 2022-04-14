from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from moneyLawndering.models import User, Listing


class CreateUserTest(TestCase):
    def setUp(self):
        bob = User(
            name='bob',
            email='bob@gmail.com',
            type=1,
            password='password',
            phoneNumber=123789,
            address='1439 Oak Drive',
            accountBalance=120,
        )
        bob.save()

    def testCanCreateValidUser(self):
        data = {
            'name': 'fakeuser',
            'email': 'fakeuser@gmail.com',
            'type': 0,
            'password': 'fakepassword',
            'phoneNumber': 123456,
            'address': '123 ave',
            'accountBalance': 400,
        }
        response = self.client.post(reverse('moneyLawndering:createUser'), data)
        self.assertRedirects(response, reverse('moneyLawndering:account'))

    def testRejectsExistingUser(self):
        data = {
            'name': 'bob',
            'email': 'bob@gmail.com',
            'type': 1,
            'password': 'password',
            'phoneNumber': 123789,
            'address': '1439 Oak Drive',
            'accountBalance': 120,
        }
        response = self.client.post(reverse('moneyLawndering:createUser'), data)
        self.assertEqual(response.json()['error'], "User with corresponding email already exists")


class SignInTest(TestCase):
    def setUp(self):
        admin = User(
            name='admin',
            email='admin@gmail.com',
            type=2,
            password='adminpassword',
            phoneNumber=123789,
            address='1439 Oak Drive',
            accountBalance=120,
        )
        admin.save()
        worker = User(
            name='worker',
            email='worker@gmail.com',
            type=0,
            password='workerpassword',
            phoneNumber=123789,
            address='100 Oak Drive',
            accountBalance=200,
        )
        worker.save()

    def testAcceptValidUser(self):
        userData = {
            'email': 'worker@gmail.com',
            'password': 'workerpassword',
        }
        response = self.client.post(reverse('moneyLawndering:signin'), userData)
        self.assertRedirects(response, reverse('moneyLawndering:account'))

    def testAcceptValidAdmin(self):
        adminData = {
            'email': 'admin@gmail.com',
            'password': 'adminpassword',
        }
        response = self.client.post(reverse('moneyLawndering:signin'), adminData)
        self.assertRedirects(response, reverse('moneyLawndering:admin'))

    def testDenyUnauthorizedUser(self):
        invalidData = {
            'email': 'fake@gmail.com',
            'password': 'fakepassword',
        }
        response = self.client.post(reverse('moneyLawndering:signin'), invalidData)
        self.assertEqual(response.status_code, 200)


class UpdateUserTest(TestCase):
    def setUp(self):
        user = User(
            name='jim',
            email='jim@gmail.com',
            type=0,
            password='password',
            phoneNumber=75849,
            address='123 Logan Dr',
            accountBalance=15,
        )
        user.save()
        session = self.client.session
        session['userId'] = user.id
        session.save()
        cookieName = settings.SESSION_COOKIE_NAME
        self.client.cookies[cookieName] = session.session_key

    def testValidUpdate(self):
        updateData = {
            'name': 'bob',
            'email': 'bob@gmail.com',
            'password': 'password2',
            'phoneNumber': 123789,
            'address': '1439 Oak Drive',
            'accountBalance': 120,
        }
        response = self.client.post(reverse('moneyLawndering:updateUser'), updateData)
        updatedUser = User.objects.get(pk=self.client.session['userId'])
        self.assertEqual(updatedUser.name, updateData['name'])
        self.assertEqual(updatedUser.email, updateData['email'])
        self.assertEqual(updatedUser.password, updateData['password'])
        self.assertEqual(updatedUser.phoneNumber, updateData['phoneNumber'])
        self.assertEqual(updatedUser.address, updateData['address'])
        self.assertEqual(updatedUser.accountBalance, updateData['accountBalance'])
        self.assertRedirects(response, reverse('moneyLawndering:account'))

class ListingsTest(TestCase):
    def setUp(self):
        self.customer = User(
            name='jim',
            email='jim@gmail.com',
            type=1,
            password='password',
            phoneNumber=75849,
            address='123 Logan Dr',
            accountBalance=100,
        )
        self.listingData = {
            "category": "Lawn Care",
            "location": "123 Fake Street",
            "time_est": 10,
            "dayOfWeek": "Tuesday",
            "startTime": "1:00pm",
            "endTime": "3:00pm",
            "description": "Mow my lawn",
            "price": 25,
        }
        self.customer.save()
        session = self.client.session
        session['userId'] = self.customer.id
        session.save()
        cookieName = settings.SESSION_COOKIE_NAME
        self.client.cookies[cookieName] = session.session_key

    def testValidNewListing(self):
        response = self.client.post(reverse('moneyLawndering:newListing'), self.listingData)
        self.assertRedirects(response, reverse('moneyLawndering:myListing'))

    def testInsufficientFundsForListing(self):
        # Price out of bounds
        self.listingData['price'] = 10000
        response = self.client.post(reverse('moneyLawndering:newListing'), self.listingData)
        self.assertEqual(response.json()['failure'], "You have insufficient funds for this job!")

    def testInvalidNewListing(self):
        # Remove price field and get invalid error
        self.listingData.pop('price')
        response = self.client.post(reverse('moneyLawndering:newListing'), self.listingData)
        self.assertEqual(response.json()['failure'], "You sent an invalid listing and it could not create it")

    def testDeleteListing(self):
        response = self.client.post(reverse('moneyLawndering:newListing'), self.listingData)
        self.assertRedirects(response, reverse('moneyLawndering:myListing'))
        listingId = self.customer.listing_set.filter(time_est = "10")[0].id
        response = self.client.get(reverse('moneyLawndering:deleteListing', args=(listingId,)))
        self.assertRedirects(response, reverse('moneyLawndering:myListing'))
        self.assertEqual(0, len(self.customer.listing_set.filter(time_est="10")))


class AcceptListingTest(TestCase):
    def setUp(self):
        self.customer = User(
            name='jim',
            email='jim@gmail.com',
            type=1,
            password='password',
            phoneNumber=75849,
            address='123 Logan Dr',
            accountBalance=100,
        )
        self.customer.save()
        self.exampleListing = Listing(
            customer=self.customer,
            category="Lawn Care",
            location="123 Logan Ave",
            time_est="2",
            dayOfWeek="Tuesday",
            startTimeOfDay="1:00pm",
            endTimeOfDay="3:00pm",
            description="desc",
            price=25,
            status=0,
            pubDate=timezone.now(),
            worker=0,
            workerPhoneNumber=0,
            workername="")
        self.exampleListing.save()
        session = self.client.session
        session['userId'] = self.customer.id
        session.save()
        cookieName = settings.SESSION_COOKIE_NAME
        self.client.cookies[cookieName] = session.session_key

    def testAcceptExistingListing(self):
        response = self.client.get(reverse('moneyLawndering:acceptListing', args=(self.exampleListing.id,)))
        self.assertRedirects(response, reverse('moneyLawndering:publicListing'))

    def testAcceptNonexistantListing(self):
        response = self.client.get(reverse('moneyLawndering:acceptListing', args=(1500,)))
        self.assertEqual(response.status_code, 404)