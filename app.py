from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your OpenWeatherMap API key
OPENWEATHER_API_KEY = '70c16e358990d72dc8e3e736eed857fc'

@app.route('/api/hello', methods=['GET'])
def hello():
    try:
        visitor_name = request.args.get('visitor_name', 'Guest')
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        # Use a third-party API to get location data
        location_response = requests.get(f'http://ip-api.com/json/{client_ip}')
        location_data = location_response.json()
        
        city = location_data.get('city', 'your city')
        
        # Use OpenWeatherMap API to get the current weather data
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather',
            params={'q': city, 'appid': OPENWEATHER_API_KEY, 'units': 'metric'}
        )
        weather_data = weather_response.json()
        
        temperature = weather_data['main']['temp'] if 'main' in weather_data else 'unknown'
        
        return jsonify({
            'client_ip': client_ip,
            'location': city,
            'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
