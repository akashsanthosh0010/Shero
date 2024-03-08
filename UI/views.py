from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

import requests
from django.conf import settings
import json
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':

            email=request.POST.get('email')
            password=request.POST.get('password')

            user = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                login(request,user)
                return redirect(home)
        return render(request,'register.html')




api_key = '8cb67d6bfab14d96b269cff7e6b53f40';

api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + api_key
@login_required(login_url='register')
def home(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
 
        ip = x_forwarded_for.split(',')[0]
 
    else:
 
        ip = request.META.get('REMOTE_ADDR')
 
 
 
    geolocation_json = get_ip_geolocation_data(ip)
    
 
    geolocation_data = json.loads(geolocation_json)
    country = geolocation_data.get('country')
    region = geolocation_data.get('region')
    postal_code = geolocation_data.get('postal_code')
    city = geolocation_data.get('city')
    longitude = geolocation_data.get('longitude')
    latitude = geolocation_data.get('latitude')
    map_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    context = {
                 'country': country,
                 'region': region,
                 'postal_code': postal_code,
                 'city': city,
                 'longitude': longitude,
                 'latitude': latitude,
                 'map_link': map_link,
             }

    return render(request, 'home.html',context)


def get_ip_geolocation_data(ip_address):




    response = requests.get(api_url)

    return response.content
