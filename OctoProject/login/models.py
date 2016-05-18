from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.template.defaultfilters import default


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
    bitrate=models.CharField(max_length=100,default="")
    streamtype=models.CharField(max_length=100,default="")
    publish=models.CharField(max_length=100,default="")
    password=models.CharField(max_length=100,default="")
    readonly=models.CharField(max_length=600,default="")
    
def __unicode__(self):
    return self.name


class customers(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    cpcode=models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
    
class aspects(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    filter=models.CharField(max_length=2000)
    def __unicode__(self):
        return self.name