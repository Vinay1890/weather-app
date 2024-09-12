from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)

API_KEY = "5TJ24EHEMB5B7V7VEBJH8H3WZ"  # Visual Crossing API key

def get_local_time():
    # Returns the current local time in 12-hour format
    current_time = datetime.datetime.now()
    hour = current_time.strftime("%I")
    minute = current_time.strftime("%M")
    ampm = current_time.strftime("%p")
    return f"{hour}:{minute} {ampm}"

@app.route('/', methods=['GET', 'POST'])
def index():
    location = 'Sultanpur'  # Default city
    
    # If the form is submitted (POST request), use the searched location
    if request.method == 'POST':
        location = request.form.get('location')
    
    # Fetch weather for the given location (default or user-entered)
    weather_data = fetch_weather(location)
    
    return render_template('index.html', weather_data=weather_data)

def fetch_weather(location_name):
    try:
        # API call to fetch the weather data for the given location
        response = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location_name}?key={API_KEY}")
        response.raise_for_status()  # Raise an error if the request fails
        weather_data = response.json()

        current_conditions = weather_data.get('currentConditions', {})
        processed_data = {
            'resolved_address': weather_data.get('resolvedAddress', 'Unknown Location'),
            'date': f"{datetime.datetime.now():%A, %B %Y}",
            'local_time': get_local_time(),
            'temp': f"{current_conditions.get('temp', 'N/A')} °F",
            'icon': f"/static/icons/{current_conditions.get('icon', 'unknown')}.png",
            'wind_dir': f"{current_conditions.get('winddir', 'N/A')} NW",
            'wind_speed': f"{current_conditions.get('windspeed', 'N/A')} Km/h",
            'humidity': f"{current_conditions.get('humidity', 'N/A')} %",
            'dew': current_conditions.get('dew', 'N/A')
        }
        return processed_data
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {'error': 'Could not fetch weather data'}

if __name__ == '__main__':
    app.run(debug=True)
