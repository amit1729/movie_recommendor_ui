from urllib import response
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import generics, serializers, status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from .crawlers import crawlSetup
from .models import PerliminaryData
from itertools import combinations

# Create your views here.
class GetPreliminaryData(APIView):
  def get(self, request, format = None):
    crawlSetup()
    entries = PerliminaryData.objects.all()
    #print(len(entries))
    if(len(entries)<=0):
      return Response({"Response":"Something Gone Wrong"},status=status.HTTP_204_NO_CONTENT)
    else:
      data = entries[0].data
      return Response(data,status=status.HTTP_200_OK)
    

class FormSubmit(APIView):
  def post(self,request,format=None):
    entries = PerliminaryData.objects.all()
    if(len(entries)<=0):
      crawlSetup()
      entries = PerliminaryData.objects.all()
    else:
      data = entries[0].data
      res = request.data
      titleTypeIndices = []
      genreIndices = []
      certificateIndices =[]
      languageIndex = 0
      for i,d in enumerate(request.data["titleType"]):
        if(d): titleTypeIndices.append(i)
      for i,d in enumerate(request.data["genres"]):
        if(d): genreIndices.append(i)
      for i,d in enumerate(request.data["certificates"]):
        if(d): certificateIndices.append(i)
      #print(data.data)
      for i,d in enumerate(data["language"]):
        if(request.data["language"]==d):
          languageIndex = i
          break
      genre_combinations = [(x,) for x in genreIndices]
      if len(genreIndices) >= 2:
        genre_combinations += combinations(genreIndices, 2)

      if len(genreIndices) >= 3:
        genre_combinations += combinations(genreIndices, 3)
      
      BASE_URL = "https://www.imdb.com/search/title/?"
      urls = []
      url = BASE_URL+"title_type="
      for i in titleTypeIndices:
        url+=(data["TitleTypes_values"][i]+",")
      url=url+"&release_date="+str(res["releaseYear"])+"-01-01,"
      url=url+"&user_rating="+str(res["minIMDb"])+","
      url=url+"&certificates="
      for i in certificateIndices:
        url+=(data["certificates"][i]+",")
      url=url+"&languages="+data["language_values"][languageIndex]+","
      if(res["adultTitles"]):
        url+="&adult=include"
      url+="&genres="
      for gen in genre_combinations:
        url1=url
        for i in range(len(gen)):
          url1+=(data["genres_values"][gen[i]]+",")
        urls.append(url1)
      
    return Response(request.data,status=status.HTTP_200_OK)