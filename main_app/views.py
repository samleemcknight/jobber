from django.shortcuts import render, redirect

from django.contrib.auth import login

from .forms import SignupForm, EventForm, EditProfileForm

from .models import Event, Category, User

# Create your views here.

# home view:
def home(request):
  events = Event.objects.all().order_by('date')
  categories = Category.objects.all()
  context = {
    'events': events,
    'categories': categories,
  }
  return render(request, 'index.html', context)

def profile(request):
  events = Event.objects.filter(user__id=request.user.id)
  context = {
    'events': events
  }
  return render(request, 'registration/profile.html', context)

def view_profile(request, user_id):
  events = Event.objects.filter(user__id=user_id)
  if user_id:
    user = User.objects.get(id=user_id)
  else:
    user = request.user
  date = user.date_joined
  user.date_joined = date.strftime("%B %d, %Y")
  context = {
    'user': user,
    'events': events
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
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = SignupForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)