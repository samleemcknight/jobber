from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Event

class SignupForm(UserCreationForm):
  first_name = forms.CharField(max_length=20, required=False, help_text='Optional')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
  email = forms.EmailField(max_length=200, help_text='Required')
  
  def validate_email(value):
    if User.objects.filter(email = value).exists():
      raise ValidationError(
          (f"{value} is taken."),
          params = {'value':value}
      )

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = ('name', 'date', 'time_zone', 'description', 'speaker', 'location_link')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)