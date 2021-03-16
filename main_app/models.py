from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

TIME_ZONE = (
  ('PST', 'Pacific Time'),
  ('MST', 'Mountain Time'),
  ('CT', 'Central Time'),
  ('ET', 'Eastern Time'),
  ('HST', 'Hawaii Standard Time')
)

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=30)

  def __str__(self):
    return f"{self.name}"

class Event(models.Model):
  name = models.CharField(max_length=100)
  date = models.DateTimeField("Event Date")
  time_zone = models.CharField(max_length=3, choices=TIME_ZONE, default=TIME_ZONE[0][0])
  description = models.CharField(max_length=300)
  speaker = models.CharField(max_length=50)
  location_link = models.CharField(max_length=250)

  user = models.ManyToManyField(User, blank=True)
  category = models.ManyToManyField(Category, blank=True)

  def __str__(self):
    return f"{self.name}"