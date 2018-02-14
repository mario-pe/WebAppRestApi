
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomerUrlSerializer, CustomerFileSerializer
from .utils import *


class Url(APIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        user_agent_support(request)
        urls = CustomerUrl.objects.all()
        serializer = CustomerUrlSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomerUrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer_saver(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUrl(APIView):

    permission_classes = (AllowAny,)

    def put(self, request, format=None):
        data = JSONParser().parse(request)
        request_password = data['password']
        request_url = data['url']

        if request_url[-1:] == "/":
            url = request_url[:-1]
            splited_url = url.split('/')
            id = splited_url[-1]
        else:
            splited_url = request_url.split('/')
            id = splited_url[-1]
        try:
            instance = CustomerUrl.objects.get(pk=id)
        except CustomerUrl.DoesNotExist:
            return HttpResponse(status=404)

        serializer = CustomerUrlSerializer(instance)
        if request_password == instance.password:
            update_counter(instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class File(APIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = CustomerFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer_saver(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFile(APIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def put(self, request, format=None):
        user_agent_support(request)
        data = JSONParser().parse(request)
        request_password = data['password']
        request_url = data['url']
        if request_url[-1:] == "/":
            url = request_url[:-1]
            splited_url = url.split('/')
            id = splited_url[-1]
        else:
            splited_url = request_url.split('/')
            id = splited_url[-1]
        try:
            instance = CustomerFile.objects.get(pk=id)
        except CustomerFile.DoesNotExist:
            return HttpResponse(status=404)

        serializer = CustomerFileSerializer(instance)
        if request_password == instance.password:
            update_counter(instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



