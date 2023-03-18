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

        self.api_key = config.appid

        # Create widgets
        title_font = ("Arial", 28, "bold")
        input_font = ("Arial", 14)
        data_font = ("Arial", 14)

        self.title_label = tk.Label(
            self.master, text="Weather App", font=title_font, bg="#fff"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.city_label = tk.Label(
            self.master, text="Enter City Name:", font=input_font, bg="#fff"
        )
        self.city_label.grid(row=1, column=0, padx=20)

        self.city_entry = tk.Entry(self.master, font=input_font)
        self.city_entry.grid(row=1, column=1, padx=20)

        self.search_button = tk.Button(
            self.master, text="Search", font=input_font, command=self.get_weather
        )
        self.search_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.current_data_label = tk.Label(
            self.master, text="Current Weather Data:", font=title_font, bg="#fff"
        )
        self.current_data_label.grid(row=3, column=0, columnspan=2, pady=20)

        self.current_weather_label = tk.Label(
            self.master, text="", font=data_font, bg="#fff"
        )
        self.current_weather_label.grid(row=4, column=0, columnspan=2)

    def get_weather(self):
        city = self.city_entry.get()

        # Call weather API
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            # Parse JSON response
            data = json.loads(response.text)
            condition = data["weather"][0]["main"]
            temp = data["main"]["temp"]
            min_temp = data["main"]["temp_min"]
            max_temp = data["main"]["temp_max"]
            pressure = data["main"]["pressure"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            sunrise = time.strftime(
                "%H:%M:%S", time.gmtime(data["sys"]["sunrise"] - 3600)
            )
            sunset = time.strftime(
                "%H:%M:%S", time.gmtime(data["sys"]["sunset"] - 3600)
            )

            # Update current weather label
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
        else:
            # Clear current weather label if city is not found
            self.current_weather_label.config(text="City not found")

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    app.run()
