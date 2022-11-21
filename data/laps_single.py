import json
import requests


class LapsSingle:
    def __init__(self, subsession_id, session):
        self.subsession_id = subsession_id
        self.session = session

        self.inputLaps = None
        self.iRacingData = None
        self.fuzzData = None
        self.carclassid = None
        self.fuzzInstance = None

    def requestLapsSingle(self):

        load_success = False

        try:
            self.iRacingData = self.cache_load()
            load_success = True
        except FileNotFoundError:
            print('[laps_single] Files do not exist')

        if not load_success:
            print('[laps_single] Requesting subsession from iRacing API and Fuzzwah...')

            # Fuzzwah
            self.fuzzData = self.fuzzInstance.requestResultsSimple()[1]

            # iRacingAPI
            racesJson = self.session.get('https://members-ng.iracing.com/data/results/lap_data',
                                         params={"subsession_id": self.subsession_id, "simsession_number": "0"})
            racesDict = racesJson.json()
            racesJson_final = requests.get(racesDict["link"]).json()

            base_download_url = racesJson_final["chunk_info"]["base_download_url"]

            self.iRacingData = []

            for data in racesJson_final["chunk_info"]["chunk_file_names"]:
                intList = requests.get(base_download_url + data).json()
                self.iRacingData = self.iRacingData + intList

            self.cache_save()

        return self.iRacingData

    def cache_load(self):
        fileAPI = open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
            self.subsession_id) + "_results_lap_data_SINGLE.json")
        APIFile = json.load(fileAPI)
        fileAPI.close()

        print("[laps_single] Loaded subsession \"" + str(self.subsession_id) + "\" from cache")

        return APIFile

    def cache_save(self):
        with open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
                self.subsession_id) + "_results_lap_data_SINGLE.json", "w") as a:
            json.dump(self.iRacingData, a, indent=2)

        print("[laps_single] Saved subsession \"" + str(self.subsession_id) + "\" to cache")

