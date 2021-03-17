from django.shortcuts import render, redirect

from django.contrib.auth import login

from .forms import SignupForm, EventForm, EditProfileForm

from .models import Event, Category, User

# Create your views here.

# home view:
def home(request):
  events = Event.objects.all().order_by('date')
  context = {
    'events': events
  }
  return render(request, 'index.html', context)

def profile(request):
  
  return render(request, 'registration/profile.html')


def view_profile(request, user_id):
  if user_id:
    user = User.objects.get(id=user_id)
  else:
    user = request.user
  date = user.date_joined
  user.date_joined = date.strftime("%B %d, %Y")
  print('date: ', date)
  context = {
    'user': user
  }
  return render(request, 'registration/profile.html', context)

def edit_profile(request, user_id):
  user = User.objects.get(id=user_id)
  if user.id == request.user.id:
    profile_form = EditProfileForm(request.POST or None, instance=user)
    
    if request.POST and profile_form.is_valid():

      profile_form.save()

      return redirect('view_profile', user_id=user_id)
    else:
      return render(request, 'registration/edit_profile.html', { 'user': user, 'profile_form': profile_form })

  else:
    return redirect('view_profile', user_id=request.user.id)

def event_detail(request, event_id):
  event = Event.objects.get(id=event_id)

  categories = event.category.all()

  context = {
    'event': event,
    'categories': categories
  }

  return render(request, 'events/event.html', context)

def search_bar(request):
  if request.method == 'GET':
    search = request.GET.get('search')
    events = Event.objects.all().filter(name=search)
    context = {
      'events': events
    }
    return render(request, 'events/searchResult.html', context)

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