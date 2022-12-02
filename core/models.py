from django.db import models

# Create your models here.
class Powerlifting(models.Model):
    weight = models.CharField(max_length=50)
    gender = models.CharField(max_length=150)
    age = models.CharField(max_length=50)

    def __str__(self):
        return self.name