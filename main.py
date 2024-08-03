import tkinter as tk
import requests
import time
import json
import config

class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather App")
        self.master.geometry("500x600")
        self.master.configure(bg="#fff")

        self.api_key = getattr(config, 'appid', None)
        if not self.api_key:
            raise ValueError("API key not found in config")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        title_font = ("Arial", 28, "bold")
        input_font = ("Arial", 14)
        data_font = ("Arial", 14)

        self.title_label = tk.Label(self.master, text="Weather App", font=title_font, bg="#fff")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.city_label = tk.Label(self.master, text="Enter City Name:", font=input_font, bg="#fff")
        self.city_label.grid(row=1, column=0, padx=20)

        self.city_entry = tk.Entry(self.master, font=input_font)
        self.city_entry.grid(row=1, column=1, padx=20)

        self.search_button = tk.Button(self.master, text="Search", font=input_font, command=self.get_weather)
        self.search_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.current_data_label = tk.Label(self.master, text="Current Weather Data:", font=title_font, bg="#fff")
        self.current_data_label.grid(row=3, column=0, columnspan=2, pady=20)

        self.current_weather_label = tk.Label(self.master, text="", font=data_font, bg="#fff")
        self.current_weather_label.grid(row=4, column=0, columnspan=2)

        self.loading_label = tk.Label(self.master, text="", font=data_font, bg="#fff", fg="red")
        self.loading_label.grid(row=5, column=0, columnspan=2)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.current_weather_label.config(text="Please enter a city name.")
            return

        self.loading_label.config(text="Fetching data...")
        self.master.update_idletasks()

        try:
            weather_data = self.fetch_weather_data(city)
            if weather_data:
                self.update_weather_display(weather_data)
            else:
                self.current_weather_label.config(text="City not found or API error.")
        except requests.exceptions.RequestException as e:
            self.current_weather_label.config(text="Error fetching data. Check your connection.")
            print(e)
        finally:
            self.loading_label.config(text="")

    def fetch_weather_data(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        return None

    def update_weather_display(self, data):
        condition = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        min_temp = data["main"]["temp_min"]
        max_temp = data["main"]["temp_max"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        sunrise = time.strftime("%H:%M:%S", time.gmtime(data["sys"]["sunrise"] - 3600))
        sunset = time.strftime("%H:%M:%S", time.gmtime(data["sys"]["sunset"] - 3600))

        current_weather = (
            f"Condition: {condition}\n"
            f"Temperature: {temp}°C\n"
            f"Min Temperature: {min_temp}°C\n"
            f"Max Temperature: {max_temp}°C\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}"
        )
        self.current_weather_label.config(text=current_weather)

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    app.run()
