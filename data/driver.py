import requests


class Driver:

    def __init__(self, display_name, session):
        self.display_name = display_name
        self.licenses = None
        self.cust_id = None
        self.requestDriver(session)

    def requestDriver(self, session):
        responseJson = session.get('https://members-ng.iracing.com/data/lookup/drivers', params={"search_term": self.display_name})
        responseDict = responseJson.json()
        finalJson = requests.get(responseDict["link"])
        finalDict = finalJson.json()[0]

        self.cust_id = finalDict["cust_id"]
        self.licenses = finalDict["licenses"]
