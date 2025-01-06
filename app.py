from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"  
BASE_URL = "https://api.openweathermap.org/data/2.5/"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def get_weather():  
    city = request.form.get('city')
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    try:
        # Fetch current weather
        weather_url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code != 200:
            return jsonify({'error': weather_data.get('message', 'Failed to fetch weather')}), weather_response.status_code

        # Fetch 5-day forecast
        forecast_url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        if forecast_response.status_code != 200:
            return jsonify({'error': forecast_data.get('message', 'Failed to fetch forecast')}), forecast_response.status_code

        return jsonify({
            'current_weather': {
                'city': weather_data['name'],
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'],
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed']
            },
            'forecast': [
                {
                    'date': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'description': item['weather'][0]['description']
                }
                for item in forecast_data['list'][::8]  # Get one forecast per day
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
