from __future__ import unicode_literals

from django.db import models
from django.core.validators import *

from django.contrib.auth.models import User, Group

from django.contrib import admin
import base64

from rest_framework import serializers

def validation(value):
    if 1 <= value <= 5:
        pass

class Breed(models.Model):
    name = models.CharField(max_length=1000, blank=False)
    breed_choices = (('T', 'Tiny'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'))
    size = models.CharField(max_length=1, choices=breed_choices, blank=False)
    friendliness = models.IntegerField(validators=[validation])
    trainability = models.IntegerField(validators=[validation])
    sheddingamount = models.IntegerField(validators=[validation])
    exerciseneeds = models.IntegerField(validators=[validation])

    def __str__(self):
        return str(self.name)

    def validation(value):
        if 1 <= value <= 5:
            pass

def valid(val):
    if 1<= val <= 100:
        pass

class Dog(models.Model):
    name = models.CharField(max_length=1000, blank=False)
    age = models.IntegerField(validators=[valid])
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1000, blank=False)
    color = models.CharField(max_length=1000, blank=False)
    favoritefood = models.CharField(max_length=1000, blank=False)
    favoritetoy = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return str(self.name)

class Event(models.Model):
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=1000, blank=False)
    info = models.CharField(max_length=1000, blank=False)
    group = models.ForeignKey(Group, related_name="events", on_delete=models.CASCADE)


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
class Profile(models.Model):
    name = models.CharField(max_length=1000, blank=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    # validators should be a list
    user =models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # relationship field
    # children <-- list of parent objects related to this profile

class Child(models.Model):
    name = models.CharField(max_length=1000, blank=False)
    parent = models.ForeignKey(Profile, related_name="children", on_delete=models.CASCADE)

    def __str__(self):
        return str(str(self.id)+' - ' + self.name)

class Group(models.Model):
    name = models.CharField(max_length=1000, blank=False)
    members = models.ManyToManyField(Child, related_name="groups")

    def __str__(self):
        return str(str(self.id)+' - ' + self.name)
    # relationship fields
    # events <-- list of event objects mapped to this group

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('timestamp', 'title', 'info', 'group')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'phone_number', 'user')

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ('name', 'parent')

class GroupSerializer(serializers.ModelSerializer):
    included_serializers = {
    'members': ChildSerializer, 'events': EventSerializer
    }
    class Meta:
        model = Group
        fields = ('name', 'members')
    class JSONAPIMeta:
        included_resources = ['members', 'events']

class EventAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'title', 'info', 'group')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number')

class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ('id', 'name', 'age', 'breed', 'gender', 'color', 'favoritefood', 'favoritetoy')

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ('id', 'name', 'size', 'friendliness', 'trainability', 'sheddingamount', 'exerciseneeds')

class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'breed', 'gender', 'color', 'favoritefood', 'favoritetoy')

class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'friendliness', 'trainability', 'sheddingamount', 'exerciseneeds')

class ApiKey(models.Model):
    owner = models.CharField(max_length=1000, blank=False)
    key = models.CharField(max_length=5000, blank=False)

    def __str__(self):
        return str(self.owner) + str(self.key)

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('owner','key')
