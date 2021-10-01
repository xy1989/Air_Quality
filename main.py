import requests
from kivy.app import App
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
Window.size = (375, 812)


class Location:
    base_url = "http://ZiptasticAPI.com/"  # call to Ziptastic api
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    def __init__(self, zipcode):
        self.url = self.base_url + zipcode

    def get(self):
        """Get the location city and state from zipcode"""
        response = requests.get(self.url)
        content = response.json()
        self.country = "USA"
        self.state = self.states[content['state']]  # convert abbreviation to full name
        self.city = content['city'].title()
        AirQuality(self.country, self.state, self.city)


class AirQuality:
    api_key = "823383ea-7c32-4251-a3e4-d235a8748872"

    def __init__(self, country, state, city):
        self.country = country
        self.state = state
        self.city = city

        self.url = f"http://api.airvisual.com/v2/city?" \
                   f"city= {self.city}&" \
                   f"state= {self.state}&" \
                   f"country= {self.country}&" \
                   f"key={self.api_key}"

        self.get()

    def get(self):
        """Retrieve air quality index"""
        response = requests.get(self.url)
        content = response.json()
        self.aqi = str(content['data']['current']['pollution']['aqius'])
        app = App.get_running_app()  # create instance of original app
        app.root.get_air_quality(self.aqi)


class Root(MDBoxLayout):
    def get_zipcode(self):
        zipcode = self.ids.zipcode.text
        if zipcode == "":
            self.ids.zipcode.text = "Please enter a valid zipcode."
        else:
            Location(zipcode).get()
            self.ids.zipcode.text = ""

    def get_air_quality(self, aqi):
        self.ids.result.text = aqi
        aqi = int(aqi)
        if aqi >= 301:
            self.ids.interpretation.text = "Hazardous" + "\n" + \
                                           "health warning of emergency conditions: everyone is more " \
                                           "likely to be affected."
        elif aqi >= 201:
            self.ids.interpretation.text = "Very Unhealthy" + "\n" + \
                                           "Health alert: The risk of health effects is increased for everyone."
        elif aqi >= 151:
            self.ids.interpretation.text = "Unhealthy" + "\n" + \
                                           "Some members of the general public may experience health effects; " \
                                           "members of sensitive groups may experience more serious health effects."
        elif aqi >= 101:
            self.ids.interpretation.text = "Unhealthy for Sensitive Groups" + "\n" + \
                                           "Members of sensitive groups may experience health effects. " \
                                           "The general public is less likely to be affected."
        elif aqi >= 51:
            self.ids.interpretation.text = "Moderate" + "\n" + \
                                           "Air quality is acceptable. However, there may be a risk for some people, " \
                                           "particularly those who are unusually sensitive to air pollution."
        else:
            self.ids.interpretation.text = "Good" + "\n" + \
                                           "Air quality is satisfactory, and air pollution poses little or no risk."


class MainApp(MDApp):
    def build(self):
        Builder.load_file("frontend.kv")
        return Root()


MainApp().run()