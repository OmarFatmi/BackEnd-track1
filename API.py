from flask import Flask,request,jsonify
import requests
app =Flask(__name__)

@app.route('/api/hello',methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Use a third-party API to get location data
    location_response = requests.get(f'http://ip-api.com/json/{client_ip}')
    location_data = location_response.json()
    
    city = location_data.get('city', 'your city')
    temperature = 11  # For simplicity, we're using a constant value here
    
    return jsonify({
        'client_ip': client_ip,
        'location': city,
        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)