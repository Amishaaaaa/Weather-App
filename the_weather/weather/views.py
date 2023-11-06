import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e16f591c18fccb3df9619b6d411fcb7c'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        if 'main' in r and 'temp' in r['main']:
            city_weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }
            weather_data.append(city_weather)
        else:
        # Handle cases where the 'main' key or 'temp' key is not present in the response
            city_weather = {
                'city': city.name,
                'error_message': 'Data not available for this city',
            }
            weather_data.append(city_weather)
      
    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)