from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from .crawlers import crawlSetup
import json

# Create your views here.
class GetPreliminaryData(APIView):
  def get(self, request, format = None):
    crawlSetup()
    with open("preliminary") as f:
      data = json.load(f)
    return Response(data,status=status.HTTP_200_OK)

