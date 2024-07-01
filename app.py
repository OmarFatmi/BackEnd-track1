



from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Your OpenWeatherMap API key
OPENWEATHER_API_KEY = '70c16e358990d72dc8e3e736eed857fc'

@app.route('/api/hello', methods=['GET'])
def hello():
    try:
        visitor_name = request.args.get('visitor_name', 'Guest')
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        logging.debug(f'Visitor name: {visitor_name}')
        logging.debug(f'Client IP: {client_ip}')
        
        # Default city for localhost or if location retrieval fails
        default_city = 'Algiers'
        
        if client_ip == '127.0.0.1':
            city = default_city
            logging.debug(f'Using default city: {city} for localhost')
        else:
            # Use a third-party API to get location data
            location_response = requests.get(f'http://ip-api.com/json/{client_ip}')
            location_data = location_response.json()
            
            logging.debug(f'Location data: {location_data}')
            
            # Handle potential issues with location data
            if location_response.status_code != 200 or location_data.get('status') != 'success':
                logging.error('Failed to retrieve location data, using default city')
                city = default_city
            else:
                city = location_data.get('city', default_city)
        
        # Use OpenWeatherMap API to get the current weather data
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather',
            params={'q': city, 'appid': OPENWEATHER_API_KEY, 'units': 'metric'}
        )
        weather_data = weather_response.json()
        
        logging.debug(f'Weather data: {weather_data}')
        
        if 'main' in weather_data:
            temperature = weather_data['main']['temp']
        else:
            temperature = 'unknown'
            logging.error('Weather data does not contain "main" key')
        
        return jsonify({
            'client_ip': client_ip,
            'location': city,
            'greeting': f'Hello, {visitor_name}!, the temperature is {str(temperature)} degrees Celsius in {city}'
        })
    except Exception as e:
        logging.exception('An error occurred')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
