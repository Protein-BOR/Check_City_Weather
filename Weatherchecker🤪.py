import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,
QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):  # <-- See this? It's now INSIDE the class
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: calibri;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;        
            }
            QLabel#temperature_label {
                font-size: 75px;           
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;              
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)
    
        self.get_weather_button.clicked.connect(self.get_weather)



    def get_weather(self):
        
        api_key = "ffb1801dc66eb9dd505c3b7dba5eb904"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.displaay_error("Bad Request\n Please check your input")
                case 401:
                    self.displaay_error("Unauthorized")
                case 403:
                    self.displaay_error("Access is Denied")
                case 404:
                    self.displaay_error("Not found")                
                case 500:
                    self.displaay_error("Interan error")
                case 502:
                    self.displaay_error("Bad Gateway")
                case 503:
                    self.displaay_error("Service Unavailable")              
                case 504:
                    self.displaay_error("Timeout")       
                case _:
                    self.displaay_error("HTTP ERROR Occured\n{http_error}")
        
        except requests.exceptions.ConnectionError:
            self.displaay_errorint("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.displaay_error("Timeout Error")

        except requests.exceptions.TooManyRedirects:
            self.displaay_error("Too many Redirects")
        except requests.exceptions.RequestException as req_error:
            self.displaay_error(f"Request Error: {req_error}")

  
    def displaay_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 40px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()



    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size: 75px")
        temperature_k = data["main"]["temp"]
        temperature_f = (temperature_k*9/5)-459.67
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        
        if weather_id >= 200 and weather_id <= 232:
            return "⛈️"
        elif 200 <= weather_id and weather_id <= 321:
            return "☁️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"  
        elif 701 <= weather_id <= 741:
            return "🌫️"  
        elif weather_id == 762:
            return "🌋"   
        elif weather_id == 771:
            return "💨" 
        elif weather_id == 781:
            return "🌪️" 
        elif weather_id == 800:
            return "☀️" 
        elif 801 <= weather_id <= 804:
            return "😶‍🌫️" 
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app= WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
