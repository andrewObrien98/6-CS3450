from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from moneyLawndering.models import User

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

    def test_valid_update(self):
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


