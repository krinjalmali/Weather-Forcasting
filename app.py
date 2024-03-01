from flask import Flask, render_template, request
import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from matplotlib.figure import Figure  


app = Flask(__name__)

def get_weather_data(city_name):
    api_key = 'e2fb9d722dda3bdefdbbe59d036e8b5d'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&APPID={api_key}'

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('main', {})
    else:
        return None

def generate_plot(temperature, Days):
    # Ensure you have imported the necessary libraries: 
    # import matplotlib.pyplot as plt
    # from io import BytesIO
    # import base64

    # Create a line graph
    Days = ['27Feb', '28 Feb', '29 Feb', '1 Mar', '2 Mar', '3 Mar', '4 Mar']
    temperature = ['8°C', '26°C', '8°C', '28°C', '10°C', '20°C', '21°C']

    # Define yaxis (temperature values)
    yaxis = [int(temp.replace('°C', '')) for temp in temperature]

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Plot the temperature data against Days
    ax.plot(Days, yaxis, marker='o', label='Temperature')

    # Set labels and title
    ax.set_xlabel('Days')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Graph')
    plt.scatter(Days, temperature)
    # Add a legend
    ax.legend()

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 for HTML embedding
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Show the plot (optional)
    plt.show()

    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['name']

        weather_data = get_weather_data(city_name)

        if weather_data:
            temp = weather_data.get('temp')
            weather = weather_data.get('weather', [{}])[0].get('description')
            min_temp = weather_data.get('temp_min')
            max_temp = weather_data.get('temp_max')
            pressure = weather_data.get('pressure')
            humidity = weather_data.get('humidity')
            icon = weather_data.get('weather', [{}])[0].get('icon')

            # Generate plot
            plot_url = generate_plot(city_name, temp )

            print(temp, weather, min_temp, max_temp, icon, pressure, humidity)

            return render_template('index.html', temp=temp, weather=weather, min_temp=min_temp, max_temp=max_temp, pressure=pressure,humidity=humidity, icon=icon, city_name=city_name, plot_url=plot_url)

        else:
            return render_template('index.html', error='City not found.')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
