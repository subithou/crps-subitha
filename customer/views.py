# Create your views here.
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from joblib import load

model = load('./savedModels/model.joblib')


@login_required
def customer_home(request):
    current_user = request.user
    print(current_user.id)
    context = {
        'name': current_user.first_name + " " + current_user.last_name
    }
    y_pred = model.predict([[10, 20, 10, 30, 40, 40, 50]])
    print(y_pred)
    return render(request, 'customer_home_page.html', {'context': context})


@login_required
def crop_prediction(request):
    current_user = request.user
    context = {
        'name': current_user.first_name + " " + current_user.last_name
    }

    if request.method == 'POST':
        n = float(request.POST.get('n'))
        p = float(request.POST.get('p'))
        k = float(request.POST.get('k'))
        rainfall = float(request.POST.get('rainfall'))
        ph = float(request.POST.get('ph'))
        temperature = float(request.POST.get('temperature'))
        humidity = float(request.POST.get('humidity'))

        print(n, p, k, temperature, humidity, ph, rainfall)
        return redirect('customer_crop_prediction_result', n, p, k, temperature, humidity, ph, rainfall)

    return render(request, 'customer_crop_prediction.html', {'context': context})


@login_required
def crop_prediction_result(request, n, p, k, t, h, ph, r):
    current_user = request.user
    temperature = t
    humidity = h
    rainfall = r

    y_pred = model.predict(
        [[float(n), float(p), float(k), float(temperature), float(humidity), float(ph), float(rainfall)]])
    print(y_pred[0])
    context = {
        'crop': y_pred[0].upper(),
        'n': n,
        'p': p,
        'k': k,
        'temperature': temperature,
        'rainfall': rainfall,
        'humidity': humidity,
        'ph': ph,
        'name': current_user.first_name + " " + current_user.last_name
    }
    return render(request, 'customer_crop_prediction_result.html', {'context': context})


@login_required
def yield_prediction(request):
    current_user = request.user
    context = {
        'name': current_user.first_name + " " + current_user.last_name
    }

    if request.method == 'POST':
        n = float(request.POST.get('n'))
        p = float(request.POST.get('p'))
        k = float(request.POST.get('k'))
        rainfall = float(request.POST.get('rainfall'))
        ph = float(request.POST.get('ph'))
        temperature = float(request.POST.get('temperature'))
        humidity = float(request.POST.get('humidity'))

        print(n, p, k, temperature, humidity, ph, rainfall)
        # return redirect('customer_crop_prediction_result', n, p, k, temperature, humidity, ph, rainfall)

    return render(request, 'customer_yield_prediction.html', {'context': context})


@login_required
def weather(request):
    global parsed_forecast
    current_user = request.user
    context = {
        'name': current_user.first_name + " " + current_user.last_name
    }

    import requests
    from bs4 import BeautifulSoup

    if request.method == 'POST':
        city = request.POST.get('city')
        city = city.capitalize()

        try:

            import requests
            import json

            def get_weather_forecast(location, api_key):
                base_url = "http://api.openweathermap.org/data/2.5/forecast"
                params = {
                    "q": location,
                    "appid": api_key,
                    "units": "metric"
                }

                response = requests.get(base_url, params=params)
                data = response.json()

                if response.status_code == 200:
                    return data
                else:
                    print("Error:", data["message"])
                    return None

            def parse_weather_forecast(forecast_data):
                parsed_forecast = []
                for forecast in forecast_data["list"]:
                    date_time = forecast["dt_txt"].split()
                    date = date_time[0]
                    full_time = date_time[1].split(":")
                    time = full_time[0] + ":" + full_time[1]
                    temperature = forecast["main"]["temp"]
                    description = forecast["weather"][0]["description"]
                    icon = forecast["weather"][0]["icon"]
                    wind = forecast["wind"]["speed"]
                    humidity = forecast["main"]["humidity"]

                    print(forecast)
                    parsed_forecast.append({
                        "date": date,
                        "time": time,
                        "temperature": temperature,
                        "description": description,
                        "icon": icon,
                        "wind": wind,
                        "humidity": humidity
                    })

                return parsed_forecast

            # def display_weather_forecast(forecast):
            #     for data in forecast:
            #         print("Date:", data["date"])
            #         print("Temperature:", data["temperature"], "°C")
            #         print("Description:", data["description"])
            #         print()

            # Set your OpenWeatherMap API key here
            api_key = "41f7df6e61a48c2051e1cb8447655f41"

            # Set the location for which you want to get the weather forecast
            location = city.capitalize()

            # Get the weather forecast data
            forecast_data = get_weather_forecast(location, api_key)

            if forecast_data:
                parsed_forecast = parse_weather_forecast(forecast_data)
                # display_weather_forecast(parsed_forecast)
                # for data in parsed_forecast:
                #     print("Date:", data["date"])
                #     print("Temperature:", data["temperature"], "°C")
                #     print("Description:", data["description"])

            context = {
                'data': parsed_forecast,
                'name': current_user.first_name + " " + current_user.last_name,
                'city': city

            }
            return render(request, 'customer_weather_page.html', {'context': context})

        except:
            messages.error(request, 'Please enter correct city name')

    return render(request, 'customer_weather_page.html', {'context': context})


fertilizer_model = load('./savedModels/fertilizer_model.joblib')


def fertilizer_suggestion(request):
    current_user = request.user

    context = {
        'name': current_user.first_name + " " + current_user.last_name
    }
    if request.method == 'POST':
        n = float(request.POST.get('n'))
        p = float(request.POST.get('p'))
        k = float(request.POST.get('k'))
        temperature = float(request.POST.get('temperature'))
        humidity = float(request.POST.get('humidity'))
        soil_type = int(request.POST.get('soil_type'))
        crop_type = int(request.POST.get('crop_type'))
        y_pred = fertilizer_model.predict(
            [[temperature, humidity, soil_type, crop_type, n, k, p]])
        print(y_pred[0])

        current_user = request.user
        context = {
            'name': current_user.first_name + " " + current_user.last_name,
            'fertilizer': y_pred[0]
        }
    return render(request, 'customer_fertilizer_suggestion.html', {'context': context})


def log_out(request):
    logout(request)

    return HttpResponseRedirect('/')
