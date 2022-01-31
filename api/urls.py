from django.urls import path, include
from .views import GetPreliminaryData, FormSubmit

urlpatterns = [
  path('get-preliminary-data', GetPreliminaryData.as_view()),
  path('submit-prefs', FormSubmit.as_view()),
]