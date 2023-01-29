from django.db import models

# Create your models here.
class Pais(models.Model):
    codigo=models.CharField(max_length=10)
    pais=models.TextField()
    def __str__(self):
        return self.pais