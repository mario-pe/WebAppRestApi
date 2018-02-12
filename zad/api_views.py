from datetime import datetime

from django.http import HttpResponse, JsonResponse
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
            update_archive_url(instance)
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
            update_archive_file(instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ActivityArchiveApi(APIView):
    
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, date_from, date_to):
        user_agent_support(request)
        datetime_from = datetime.strptime(str(date_from), "%Y-%m-%d")
        datetime_to_a = datetime.strptime(str(date_to), "%Y-%m-%d")
        delta = datetime_to_a - datetime_from;
        today_date = datetime.utcnow().strftime('%Y-%m-%d')

        response = {}

        for x in range(0, delta.days + 1 ):
            date_from_str = datetime_from.__str__()
            date_from_str = date_from_str[:-9]
            archive = ActivityArchive.objects.filter(date=date_from_str).first()

            if archive is not None:
                if date_from_str == today_date:
                    url = archive.url_activity
                    file = archive.file_activity
                    result = activity_statistcs(url, file)
                    reponse_for_day = {'files': result[0], 'links': result[1]}
                else:
                    result = daily_statisctic_generator(archive)
                    reponse_for_day = {'files': result[0], 'links': result[1]}
            else:
                reponse_for_day = {'files': 0, 'links': 0}

            datetime_from = datetime_from + idt.timedelta(hours=24)
            response[date_from_str.__str__()] = reponse_for_day

        return JsonResponse(response)