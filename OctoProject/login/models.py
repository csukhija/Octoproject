from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Meta:
        permissions = (
            ("add_remove_job_chirag", "Chirag add/remove jobs"),
        )

# Create your models here.

class Quota(User):
    quota=models.CharField(max_length=100)

class streams(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    aspect=models.CharField(max_length=100)
  
def __unicode__(self):
    return self.name


class customers(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    cpcode=models.CharField(max_length=100)
    def __unicode__(self):
        return self.name