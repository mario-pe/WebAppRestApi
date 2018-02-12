import unittest

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import RequestsClient
from rest_framework.test import force_authenticate

from zad.api_views import Url
from zad.models import CustomerUrl, CustomerFile
from zad.utils import password_generator


class TestDB(unittest.TestCase):
    def setUp(self):
        self.password = password_generator()
        CustomerUrl.objects.create(url="http://www.testUrl.pl", date="2017-11-05", password=password_generator())
        CustomerFile.objects.create(file=mock_file(), password=self.password)

    def test_add_to_database(self):
        instance_url = CustomerUrl.objects.filter(url="http://www.testUrl.pl").first()
        instance_file = CustomerFile.objects.create(url="http://www.testUrl.pl").first()
        self.assertEqual(instance_url.url, "http://www.testUrl.pl")
        self.assertEqual(instance_file.password, self.password)


class TestPasswords(unittest.TestCase):
    def setUp(self):
        CustomerUrl.objects.create(url="http://www.testUrl_1.pl", date="2017-11-07", password=password_generator())
        CustomerUrl.objects.create(url="http://www.testUrl_2.pl", date="2017-11-07", counter=0, password=password_generator())
        CustomerFile.objects.create(file=mock_file(), password=password_generator())
        CustomerFile.objects.create(file=mock_file(), password=password_generator())

    def test_deferent_passwords(self):
        instance_url_1 = CustomerUrl.objects.filter(url="http://www.testUrl_2.pl").first()
        instance_url_2 = CustomerUrl.objects.filter(url="http://www.testUrl_1.pl").first()
        instance_file_1 = CustomerUrl.objects.filter(url="http://www.testUrl_1.pl").first()
        instance_file_2 = CustomerUrl.objects.filter(url="http://www.testUrl_1.pl").first()
        self.assertNotEqual(instance_url_1.password, instance_url_2.password)
        self.assertNotEqual(instance_file_1.password, instance_file_2.password)


class TestDate(unittest.TestCase):
    def setUp(self):
        password1 = password_generator()
        CustomerUrl.objects.create(url="http://www.testUrl1.pl", date="2017-11-07", password=password1)

    def test_current_date_of_create(self):
        instance = CustomerUrl.objects.get(url="http://www.testUrl1.pl")
        self.assertNotEqual(instance.date, "2017-11-07")


class TestUrlPutMethod(unittest.TestCase):
    def setUp(self):
        CustomerUrl.objects.create(url="http://www.testUrll.pl", date="2017-11-25", password="")

    def test_put_url(self):

        instance = CustomerUrl.objects.get(url="http://www.testUrll.pl")
        address = instance.get_absolute_url()
        c = RequestsClient()
        response = c.put('http://127.0.0.1:8000/zad/get_url/', json={"url": address, "password": ""})
        assert response.status_code == 200


class TestUrlPostMethod(unittest.TestCase):
    def setUp(self):

        self.user = User.objects.create(username='a', password="123456Mp")
        self.post_data = {"url": "https://www.interaaia.pl/"}
        self.address = {'http://127.0.0.1:8000/zad/urls/'}

    def test_post_url(self):
        factory = APIRequestFactory()
        request = factory.post(self.address, self.post_data)
        force_authenticate(request, user=self.user)
        view = Url.as_view()
        response = view(request)
        assert response.status_code == 201


class TestFilePutMethod(APITestCase):
    def setUp(self):

        CustomerFile.objects.create(file=mock_file(), password="111111")

    def test_put_file(self):

        file = CustomerFile.objects.get(password="111111")
        address = file.get_absolute_url()
        c = RequestsClient()
        response = c.put('http://127.0.0.1:8000/zad/get_file/', json={"url": address, "password": "111111"})
        assert response.status_code == 200


class TestFilePostMethod(unittest.TestCase):
    def setUp(self):
        customer_file = CustomerFile.objects.create(file=mock_file(), password="")
        file_url = customer_file.get_absolute_url()
        self.user = User.objects.create(username='b', password="123456Mp")
        self.post_data = {"url": file_url}

    def test_post_file(self):
        factory = APIRequestFactory()
        request = factory.post('http://127.0.0.1:8000/zad/files/', self.post_data)
        force_authenticate(request, user=self.user)
        view = Url.as_view()
        response = view(request)
        assert response.status_code == 201


def mock_file():
    file = open("test_file", 'w+')
    mylist = file.readlines()
    return mylist


