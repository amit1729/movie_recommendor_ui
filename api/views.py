from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from .crawlers import crawlSetup
from .models import PerliminaryData

# Create your views here.
class GetPreliminaryData(APIView):
  def get(self, request, format = None):
    crawlSetup()
    entries = PerliminaryData.objects.all()
    print(len(entries))
    if(len(entries)<=0):
      return Response({"Response":"Something Gone Wrong"},status=status.HTTP_204_NO_CONTENT)
    else:
      data = entries[0].data
      return Response(data,status=status.HTTP_200_OK)
    

class FormSubmit(APIView):
  def post(self,request,format=None):
    return Response(request.data,status=status.HTTP_200_OK)