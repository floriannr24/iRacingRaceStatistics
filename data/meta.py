import json
import requests
from data.fuzzwah import Fuzzwah


class Meta:
    def __init__(self, subsession_id, session):
        self.subsession_id = subsession_id
        self.session = session
        self.iRacingData = None

    def requestMeta(self):

        load_success = False

        try:
            self.iRacingData = self.cache_load()
            load_success = True
        except FileNotFoundError:
            print('[meta] Files do not exist')

        if not load_success:
            print('[meta] Requesting meta for subsession from iRacing API...')

            # iRacingAPI
            self.iRacingData = self.session.get('https://members-ng.iracing.com/data/results/get',
                                           params={"subsession_id": self.subsession_id, "simsession_number": "0"})
            self.iRacingData = requests.get(self.iRacingData.json()["link"]).json()

            print(self.iRacingData)

            intDict = {}

            intDict["series_name"] = self.iRacingData["series_name"]
            intDict["track"] = self.iRacingData["track"]
            intDict["weather"] = self.iRacingData["weather"]
            intDict["session_results"] = self.iRacingData["session_results"]


            self.iRacingData = intDict

            self.cache_save()

        return self.iRacingData

    def cache_load(self):
        fileAPI = open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
            self.subsession_id) + "_meta.json")
        APIFile = json.load(fileAPI)
        fileAPI.close()

        print("[meta] Loaded subsession (meta) \"" + str(self.subsession_id) + "\" from cache")

        return APIFile

    def cache_save(self):
        with open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
                self.subsession_id) + "_meta.json", "w") as a:
            json.dump(self.iRacingData, a, indent=2)

        print("[meta] Saved subsession (meta) \"" + str(self.subsession_id) + "\" to cache")

