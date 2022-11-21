import json
import requests
from sessionbuilder.session_builder import SessionBuilder


class RecentRaces:

    def __init__(self, session):
        self.session = session
        self.iRacingData = None
        self.cust_id = 817320

    def get_RecentRaces_Data(self, fetchFromCache):

        data = self.requestRecentRaces(fetchFromCache)

        exportDict = []

        for element in data:
            intdict = {
                "session_start_time": element["session_start_time"],
                "series_name": element["series_name"],
                "start_position": element["start_position"],
                "finish_position": element["finish_position"],
                "winner_name": element["winner_name"],
                "SOF": element["strength_of_field"],
                "subsession_id": element["subsession_id"],
                "track_name": element["track"]["track_name"]
            }

            exportDict.append(intdict)

        return exportDict

    def requestRecentRaces(self, fetchFromCache):

        load_success = False

        if fetchFromCache:
            try:
                self.iRacingData = self.cache_load()
                load_success = True
            except FileNotFoundError:
                print('[recent_race] File does not exist')

        if not load_success:
            print('[recent_race] Requesting recent races from iRacing API...')

            # iRacingAPI
            racesJson = self.session.get('https://members-ng.iracing.com/data/stats/member_recent_races')
            racesDict = racesJson.json()
            racesDict_final = requests.get(racesDict["link"]).json()
            self.iRacingData = racesDict_final["races"]

            self.cache_save()

        return self.iRacingData

    def cache_load(self):
        fileAPI = open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
            self.cust_id) + "_member_recent_races.json")
        APIFile = json.load(fileAPI)
        fileAPI.close()

        print("[recent_races] Loaded list of recent races from cache")

        return APIFile

    def cache_save(self):
        with open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
                self.cust_id) + "_member_recent_races.json", "w") as a:
            json.dump(self.iRacingData, a, indent=2)

        print("[recent_races] Saved recent races to cache")

        # self.subsession_id = racesDict_final["subsession_id"]
        # self.series_name = racesDict_final["series_name"]
        # self.winner_name = racesDict_final["winner_name"]
        # self.track_name = racesDict_final["track"]["track_name"]
        # self.session_start_time = racesDict_final["session_start_time"]
