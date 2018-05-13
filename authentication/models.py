from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Area(models.Model):
    name=models.CharField(max_length=25)
    address=models.CharField(max_length=100)
    d_status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class User_Personal(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobileno=models.BigIntegerField()
    area=models.ForeignKey(Area,on_delete=models.CASCADE,related_name='area')

    def __str__(self):
        return str(self.user.username)

class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ('album', 'order')
        ordering = ['order']

    def __unicode__(self):
        return '%d: %s' % (self.order, self.title)