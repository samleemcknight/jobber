from django.shortcuts import render, redirect

from django.contrib.auth import login

from .forms import SignupForm, EventForm

from .models import Event, Category

# Create your views here.

# home view:
def home(request):
  events = Event.objects.all()
  context = {
    'events': events
  }
  return render(request, 'index.html', context)

def event_detail(request, event_id):
  event = Event.objects.get(id=event_id)

  categories = event.category.all()

  context = {
    'event': event,
    'categories': categories
  }

  return render(request, 'events/event.html', context)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = SignupForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)