from django.db import models

# Create your models here.
class PerliminaryData(models.Model):
  data = models.JSONField()

class MovieDatabase(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  movie_id = models.CharField(max_length=500, unique=True)
  movie_details = models.JSONField()
  watched = models.BooleanField(null=False, default=False)
  active = models.BooleanField(null=False, default=False)