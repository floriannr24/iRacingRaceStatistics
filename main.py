import requests
from SessionBuilder import sessionBuilder

my_sessionBuilder = sessionBuilder.SessionBuilder()
my_sessionBuilder.authenticate()
session = my_sessionBuilder.session


responseJson = session.get('https://members-ng.iracing.com/data/car/get')
responseDict = responseJson.json()
finalJson = requests.get(responseDict["link"])
finalList = finalJson.json()

print(finalList[0]["car_name"])
