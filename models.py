from django.db import models

# Create your models here.
from django.db import models

class user(models.Model):
    id = models.IntegerField(auto_created=True,primary_key=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)

    def __str__(self):
        return self.name