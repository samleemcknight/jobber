from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from datetime import timedelta, datetime
from django.utils import dateformat
from django.utils.timezone import make_aware, timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, EventForm, EditProfileForm

from .models import Event, Category, User

# Create your views here.

# home view:
def home(request):
  events = Event.objects.all().order_by('-date')
  categories = Category.objects.all()
  context = {
    'events': events,
    'categories': categories,
  }
  return render(request, 'index.html', context)

@login_required
def profile(request):
  events = Event.objects.filter(user__id=request.user.id)
  date_joined = request.user.date_joined.strftime("%B %d, %Y")
  last_login = request.user.last_login.strftime("%B %d, %Y")
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
    'past_events': past_events,
    'date_joined': date_joined,
    'last_login': last_login,
    'future_events': future_events
  }
  return render(request, 'registration/profile.html', context)

@login_required
def view_profile(request, user_id):
  # Edited the following conditional to get rid of any errors result from tring to get to 
  # a url with a user.id that doesn't exist.
  # It also makes it so that the logged-in user doesn't have two separate profiles
  user = User.objects.all()
  if user.filter(pk=user_id).exists() and user_id != request.user.id:
    user = User.objects.get(id=user_id)
  else:
    return redirect('profile')
  # if we're formatting the date this way, maybe we can just format it in the user model?
  user.date_joined = user.date_joined.strftime("%B %d, %Y")
  user.last_login = user.last_login.strftime("%B %d, %Y")
  events = Event.objects.filter(user__id=user_id)
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

def event_detail(request, event_id):
  event = Event.objects.get(id=event_id)
  categories = event.category.all()
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
  else:
    categories = categories[0]
  context = {
    'event': event,
    'categories': categories,
    'atendee': atendee,
    'guests': guests,
  }

  return render(request, 'events/event.html', context)

@login_required
def event_register(request, event_id):
  pass
  event = Event.objects.get(id=event_id)
  success_message = ''
  if request.POST['action'] == 'register':
    event.user.add(request.user)
  else: 
    event.user.remove(request.user)
  return redirect('event_detail', event_id)

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
      'Subject here',
      'Here is the message.',
      'projectjobber@gmail.com',
      [user.email],
      fail_silently=False,
      )
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = SignupForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)