from datetime import datetime
import datetime as idt

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomerUrl, CustomerFile, ActivityArchive
from .serializers import CustomerUrlSerializer, CustomerFileSerializer
from .utils import serializer_saver, update_counter, update_archive_url


class Url(APIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        urls = CustomerUrl.objects.all()
        serializer = CustomerUrlSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomerUrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer_saver(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    permission_classes = (AllowAny,)
    def put(self, request, format=None):
        data = JSONParser().parse(request)
        request_password = data['password']
        request_url = data['url']

        if request_url[-1:] == "/":
            r_url = request_url[:-1]
            p_url = r_url.split('/')
            id = p_url[-1]
        else:
            p_url = request_url.split('/')
            id = p_url[-1]
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

    def get(self, request, format=None):
        file = CustomerFile.objects.all()
        serializer = CustomerFileSerializer(file, many=True)
        return Response(serializer.data)

    def post(self, request):
        file_obj = request.FILES
        serializer = CustomerFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer_saver(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetFile(APIView):
    permission_classes = (AllowAny,)
    def put(self, request, format=None):
        data = JSONParser().parse(request)
        request_password = data['password']
        request_url = data['url']
        if request_url[-1:] == "/":
            r_url = request_url[:-1]
            p_url = r_url.split('/')
            id = p_url[-1]
        else:
            p_url = request_url.split('/')
            id = p_url[-1]
            print(id)
        try:
            instance = CustomerFile.objects.get(pk=id)
        except CustomerFile.DoesNotExist:
            return HttpResponse(status=404)

        serializer = CustomerFileSerializer(instance)
        if request_password == instance.password:
            update_counter(instance)
            update_archive_url(instance)    #update_archive_file
            return Response(serializer.data)
        return Response(serializer.errors, status=400)




class ActivityArchiveApi(APIView):
    def get(self, requset, date_from, date_to):
        a = datetime.strptime(str(date_from), "%Y-%m-%d")
        b = datetime.strptime(str(date_to), "%Y-%m-%d")
        delta = b - a;
        response = {}

        for x in range(0, delta.days + 1 ):
           b = a.__str__()
           b = b[:-9]
           archive = ActivityArchive.objects.filter(date=b).first()
           if archive is not None:
               url = archive.url_activity
               file = archive.file_activity
               result = activity_statistcs(url, file)
               r = {b.__str__():{'files': result[0], 'links': result[1]}}
           else:
               r = {b.__str__(): {'files': 0, 'links': 0}}
           a =  a + idt.timedelta(hours=24)
           response[b.__str__()] = r

        return JsonResponse(response)


def activity_statistcs(urls, files):

    return [len(set(urls.split(','))), len(set(files.split(',')))]

