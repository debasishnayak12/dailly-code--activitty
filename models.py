from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the User model
    age = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
