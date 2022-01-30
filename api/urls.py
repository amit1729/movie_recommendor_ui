from django.urls import path, include
from .views import GetPreliminaryData

urlpatterns = [
  path('get-preliminary-data', GetPreliminaryData.as_view()),
]