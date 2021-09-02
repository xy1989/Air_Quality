import requests


class Location:
    base_url = "http://ZiptasticAPI.com/"  # call to Ziptastic api

    def __init__(self, zipcode):
        self.url = self.base_url + zipcode

    def get(self):
        response = requests.get(self.url)
        content = response.json()
        self.country = content['country']
        self.state = content['state']
        self.city = content['city']


class AirQuality(Location):
    api_key = "823383ea-7c32-4251-a3e4-d235a8748872"
    url = f"http://api.airvisual.com/v2/city?city=" \
               f"{self.city}&state={self.state}&" \
               f"country={self.country}&" \
               f"key={api_key}"

    def get(self):
        response = requests.get(self.url)
        content = response.json()
        print(content)


if __name__ == "__main__":
    zipcode = input("Please enter a zipcode: ")
    Location(zipcode).get()




