from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone
# Create your models here.

class codigos(models.Model):
    #user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo=models.CharField(max_length=500, null=False, default=None)
    created_date=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.codigo