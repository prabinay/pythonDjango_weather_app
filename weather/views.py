# Create your views here.
import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    
    #Open weathermMap API integration
    url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=7f22c9c7a8b5d003aa26bb233afc15d3'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        #City Verification and Addition
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
                message = err_msg
                message_class = 'is-danger'
        else:
                message = 'City added successfully!'
                message_class = 'is-success'

            
    #Data from API to front 
    form= CityForm()
    cities= City.objects.all()
    weather_Data= []
    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_Data.append(city_weather)
    print(weather_Data)
    context = {
        'weather_Data': weather_Data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather/weather.html', context)


#City Deletion 
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
