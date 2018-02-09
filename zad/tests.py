import unittest
import tempfile
from PIL import Image
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client


import datetime as idt

from rest_framework.test import MockOriginalResponse as response, APITestCase
from rest_framework.test import RequestsClient
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from zad.api_views import Url
from zad.api_views import File as ApiFile
from zad.models import CustomerUrl, CustomerFile
from zad.utils import password_generator


class TestDB(unittest.TestCase):
    def setUp(self):
        password1 = password_generator()
        CustomerUrl.objects.create(url="http://www.testUrl.pl", date="2017-11-05", password=password1)

    def test_add_to_database(self):
        instance = CustomerUrl.objects.get(url="http://www.testUrl.pl")
        self.assertEqual(instance.url, "http://www.testUrl.pl")


class TestDeferentPasswords(unittest.TestCase):
    def setUp(self):
        password1 = password_generator()
        password2 = password_generator()
        CustomerUrl.objects.create(url="http://www.testUrl_1.pl", date="2017-11-07", password=password1)
        CustomerUrl.objects.create(url="http://www.testUrl_2.pl", date="2017-11-07", counter=0, password=password2)

    def test_deferent_passwords(self):
        instance1 = CustomerUrl.objects.get(url="http://www.testUrl_2.pl")
        instance2 = CustomerUrl.objects.get(url="http://www.testUrl_1.pl")
        self.assertNotEqual(instance1.password, instance2.password)


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
        file = open("test_file", 'w+')
        mylist = file.readlines()
        CustomerFile.objects.create(file=mylist, password="111111")

    def test_put_file(self):

        file = CustomerFile.objects.get(password="111111")
        address = file.get_absolute_url()
        c = RequestsClient()
        response = c.put('http://127.0.0.1:8000/zad/get_file/', json={"url": address, "password": "111111"})
        assert response.status_code == 200


class TestFilePostMethod(unittest.TestCase):
    def setUp(self):
        file = open("test_file", 'w+')
        mylist = file.readlines()
        customer_file = CustomerFile.objects.create(file=mylist, password="")
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
