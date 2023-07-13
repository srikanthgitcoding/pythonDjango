from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
#create tag and tag classes

class Tag(models.Model):
    label = models.CharField(max_length=255) #1

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #type (product, video, artcile) 2
    #ID 3
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object =  GenericForeignKey()











#1 created a field called - label which is gng to be a char field with max_length = 255
#2 using this we can find the table in db
#3 using this we can find the record in the table
#ContentType - is a model that reprensents type of objects in our applications
# to define generic relationships we need to define 3 fields - content type,objectid,content object