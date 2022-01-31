from django.db import models

# Create your models here.
class PerliminaryData(models.Model):
  data = models.JSONField()