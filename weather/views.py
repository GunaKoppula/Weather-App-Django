from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignupForm, UserLoginForm
from .models import CountryWeather
from django.contrib import messages
import requests
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz


def home(request):
    if request.user.is_authenticated:
        weather_data = CountryWeather.objects.filter(user=request.user)
        return render(request, 'weather/home.html', {'weather_data': weather_data})
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log in the user
            return redirect('home')  # Redirect to the home page after signup
    else:
        form = UserSignupForm()
    return render(request, 'weather/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'weather/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')


def get_datetime_from_coordinates(latitude, longitude):
    # Find the timezone using coordinates
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    
    if timezone_str is None:
        return "Timezone not found for the given coordinates."

    # Get the current time in the specified timezone
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)

    # Format the date and time
    formatted_date = now.strftime("%A, %d %B")
    formatted_time = now.strftime("%H:%M")

    return formatted_date, formatted_time

# Calculate Dew Point
def calculate_dew_point(temp, humidity):
    dew = temp - (100 - humidity) / 5
    dew_point = round(dew, 2)
    return dew_point


def fetch_weather(country):
    print("Entered fetch_weather")
    api_key = '2ba56868930ce82ca35aadb64bd40c95'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={country}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        print(data)
        
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        date, time = get_datetime_from_coordinates(lat, lon)
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        dew_point = calculate_dew_point(temp, humidity)
        cloud_cover = data['clouds']['all']

        # Determine weather condition based on cloud cover
        if cloud_cover <= 20:
            weather_condition = "Clear"
        elif cloud_cover <= 50:
            weather_condition = "Partly Cloudy"
        elif cloud_cover <= 80:
            weather_condition = "Cloudy"
        else:
            weather_condition = "Overcast"
        print(weather_condition)
        return {
            'country': data['name'],
            'date': date,
            'time': time,
            'temperature': temp,
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': humidity,
            'feels_like': data['main']['feels_like'],
            'pressure': data['main']['pressure'],
            'visibility': data['visibility'],
            'wind_speed' : data['wind']['speed'],
            'dew_point': dew_point,
            'weather_condition' : weather_condition
        }
    return None


# def add_country(request):
#     if request.method == 'POST':
#         country_name = request.POST.get('country_name')
#         weather = fetch_weather(country_name)
#         print(weather)
#         if weather:
#             CountryWeather.objects.create(
#                 user=request.user,
#                 country_name=weather['country'],
#                 temperature=weather['temperature'],
#                 humidity=weather['humidity'],
#                 date=weather['date'],
#                 time=weather['time'],
#                 temp_min=weather['temp_min'],
#                 temp_max=weather['temp_max'],
#                 feels_like=weather['feels_like'],
#                 pressure=weather['pressure'],
#                 visibility=weather['visibility'],
#                 wind_speed=weather['wind_speed'],
#                 dew_point=weather['dew_point'],
#                 weather_condition=weather['weather_condition']
#             )
#     return redirect('home')


def add_country(request):
    if request.method == 'POST':
        country_name = request.POST.get('country_name')
        
        # Check if the user already has 3 countries
        user_countries = CountryWeather.objects.filter(user=request.user)
        
        if user_countries.count() >= 3:
            messages.error(request, "You can only add up to 3 countries. Please remove one to add another.")
            return redirect('home')
        
        # Fetch the weather data
        weather = fetch_weather(country_name)
        print(weather)
        
        if weather:
            CountryWeather.objects.create(
                user=request.user,
                country_name=weather['country'],
                temperature=weather['temperature'],
                humidity=weather['humidity'],
                date=weather['date'],
                time=weather['time'],
                temp_min=weather['temp_min'],
                temp_max=weather['temp_max'],
                feels_like=weather['feels_like'],
                pressure=weather['pressure'],
                visibility=weather['visibility'],
                wind_speed=weather['wind_speed'],
                dew_point=weather['dew_point'],
                weather_condition=weather['weather_condition']
            )
        else:
            messages.error(request, "Could not fetch weather data for the given country.")
    
    return redirect('home')



def remove_country(request, country_id):
    country = CountryWeather.objects.get(id=country_id)
    if country.user == request.user:
        country.delete()
    return redirect('home')
