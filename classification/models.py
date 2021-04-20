from django.db import models

# Create your models here.
class PredictionImage(models.Model):
    nama = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='upload/')

class PredictionModel(models.Model):
    model = models.FileField(upload_to='upload/')
    model_weights = models.FileField(upload_to='upload/')
