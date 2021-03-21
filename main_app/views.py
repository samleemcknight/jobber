from django.shortcuts import render, redirect
from datetime import datetime, date
from django.core.mail import send_mail
from django.utils import dateformat
from django.utils.timezone import make_aware, timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import uuid
import boto3
from .forms import SignupForm, EventForm, EditProfileForm
from django.core.mail import send_mail


from .models import Event, Category, User, Photo

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'jobberproject'

# Create your views here.

# home view:
def home(request):
  events = Event.objects.all().order_by('date')
  categories = Category.objects.all()
  today = date.today()
  events_list = []
  for event in events:
    if event.date >= today:
      events_list.append(event)
  context = {
    'events': events_list,
    'categories': categories,

  }
  return render(request, 'index.html', context)

def about(request):
  return render(request, 'about.html')

@login_required
def profile(request):
  events = Event.objects.filter(user__id=request.user.id)
  date_joined = request.user.date_joined.strftime("%B %d, %Y")
  last_login = request.user.last_login.strftime("%B %d, %Y")
  today = date.today()
  future_events = []
  past_events = []
  for event in events:
    if event.date >= today:
      future_events.append(event)
    else:
      past_events.append(event)
  context = {
    'past_events': past_events,
    'date_joined': date_joined,
    'last_login': last_login,
    'future_events': future_events
  }
  return render(request, 'registration/profile.html', context)

@login_required
def view_profile(request, user_id):
  user = User.objects.get(id=user_id)
  if user_id == request.user.id:
    return redirect('profile')
  # formats dates to not include times:
  user.date_joined = user.date_joined.strftime("%B %d, %Y")
  user.last_login = user.last_login.strftime("%B %d, %Y")
  events = Event.objects.filter(user__id=user_id)
  # following 9 lnes separates events into past and future
  today = datetime.now()
  today = make_aware(today)
  future_events = []
  past_events = []
  for event in events:
    if event.date >= today:
      future_events.append(event)
    else:
      past_events.append(event)
  context = {
    'user': user,
    'past_events': past_events,
    'future_events': future_events
  }
  return render(request, 'registration/profile.html', context)

@login_required
def edit_profile(request):
  user = User.objects.get(id=request.user.id)
  profile_form = EditProfileForm(request.POST or None, instance=user)
  if request.POST and profile_form.is_valid():
    profile_form.save()
    return redirect('profile')
  else:
    return render(request, 'registration/edit_profile.html', { 'user': user, 'profile_form': profile_form })

def event_detail(request, event_name):
  event = Event.objects.get(name=event_name)
  categories = event.category.all()
  categories_without = Category.objects.exclude(id__in=categories.values_list('id')).values()
  atendee = event.user.filter(id=request.user.id)
  guests = event.user.all()
  if len(atendee) == 1:
    atendee = atendee[0]
  # the following conditional ensures that a string is passed to the html in order to
  # format it nicely
  if len(categories) > 1:
    categories_list = []
    for el in categories:
      categories_list.append(el.name)
    categories = ' | '.join(categories_list)
  elif len(categories) == 1:
    categories = categories[0]
  else:
    categories = "N/A"
  context = {
    'event': event,
    'categories': categories,
    'categories_without': categories_without,
    'atendee': atendee,
    'guests': guests,
  }
  return render(request, 'events/event.html', context)

@login_required
def add_category(request, event_id):
  event = Event.objects.get(id=event_id)
  category = Category.objects.get(name=request.POST['name'])
  event.category.add(category.id)
  return redirect('event_detail', event.name)

@login_required
def remove_category(request, event_id):
  event = Event.objects.get(id=event_id)
  category = Category.objects.get(name=request.POST['name'])
  event.category.remove(category.id)
  return redirect('event_detail', event.name)

@login_required
def event_register(request, event_id):
  pass
  event = Event.objects.get(id=event_id)
  success_message = ''
  if request.POST['action'] == 'register':
    event.user.add(request.user)
  else: 
    event.user.remove(request.user)
  return redirect('event_detail', event.name)

@login_required
def create_event(request):
  if request.user.is_superuser:
    form = EventForm()
    if request.method == 'POST':
      form = EventForm(request.POST)
      form.save()
      event = Event.objects.get(name=request.POST['name'])
      category = Category.objects.get_or_create(name=request.POST['category'])
      event.category.add(category[0])
      return redirect('/')
    else:
      return render(request, 'events/create.html', { "form": form })
  else:
    return redirect('/')

@login_required
def edit_event(request, event_name):
  if request.user.is_superuser:
    event = Event.objects.get(name=event_name)
    category = Category.objects.filter(id__in=event.category.all().values_list('id'))
    form = EventForm(request.POST or None, instance=event)
    context = {
      "form": form,
      "event": event,
      "categories": category
    }
    if request.method == 'POST' and form.is_valid():
      form.save()
      return redirect('event_detail', event_name=event_name)
    else:
      return render(request, 'events/edit.html', context)
  else:
    return redirect('event_detail', event_name=event_name)

def search_bar(request):
  categories = Category.objects.all()
  context = { 'categories': categories }
  if request.method == 'GET':
    search = request.GET.get('search')
    search_term = f"{search}"
    events = Event.objects.all().filter(name__icontains=search)
    context = {
      'events': events,
      'categories': categories,
      'search_term': search_term
    }
    return render(request, 'events/search_result.html', context)

def filter(request):
  events = Event.objects.filter(category__name=request.POST['category'])
  categories = Category.objects.all()
  filter_term = f"{request.POST['category']}"
  if request.method == 'POST':
    context = {
      'events': events,
      'categories': categories,
      'filter_term': filter_term
    }
    return render(request, 'events/search_result.html', context)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      send_mail(
      'CONFIRMATION: Welcome to Jobber',
      'Thank you for joining Jobber. Here is your confirmation email. ',
      'projectjobber@gmail.com',
      [user.email],
      fail_silently=True,
      )
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = SignupForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)