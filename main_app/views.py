from django.shortcuts import render

# temporary for 'sanity check':
from django.http import HttpResponse
# Create your views here.

# home view:
def home(request):
  return render(request, 'index.html')