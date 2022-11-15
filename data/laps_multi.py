import json
import requests
from data.fuzzwah import Fuzzwah


class LapsMulti:
    def __init__(self, subsession_id, session):
        self.subsession_id = subsession_id
        self.session = session

        self.inputLaps = None
        self.iRacingData = None
        self.fuzzData = None
        self.carclassid = None
        self.fuzzInstance = None

    def requestLapsMulti(self):

        load_success = False

        try:
            self.initFuzzwah()
            self.iRacingData, self.fuzzData = self.cache_load()
            load_success = True
        except FileNotFoundError:
            print('[laps_multi] Files do not exist')

        if not load_success:
            print('[laps_multi] Requesting subsession from iRacing API and Fuzzwah...')

            # Fuzzwah
            self.initFuzzwah()
            self.fuzzData = self.fuzzInstance.requestResultsSimple()[1]

            # iRacingAPI
            racesJson = self.session.get('https://members-ng.iracing.com/data/results/lap_chart_data',
                                         params={"subsession_id": self.subsession_id, "simsession_number": "0"})
            racesDict = racesJson.json()
            racesJson_final = requests.get(racesDict["link"]).json()

            base_download_url = racesJson_final["chunk_info"]["base_download_url"]
            chunk_file_names = racesJson_final["chunk_info"]["chunk_file_names"][0]

            self.iRacingData = []

            for data in racesJson_final["chunk_info"]["chunk_file_names"]:
                intList = requests.get(base_download_url + data).json()
                self.iRacingData = self.iRacingData + intList

            self.cache_save()

        return self.iRacingData, self.fuzzData

    def cache_load(self):
        fileAPI = open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
            self.subsession_id) + "_results_lap_chart_data_MULTI.json")
        APIFile = json.load(fileAPI)
        fileAPI.close()

        fileFuzz = open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
            self.subsession_id) + "_fuzzwah.json")
        fuzzFile = json.load(fileFuzz)
        fileFuzz.close()

        print("[laps_multi] Loaded subsession \"" + str(self.subsession_id) + "\" from cache")

        return APIFile, fuzzFile

    def cache_save(self):
        with open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
                self.subsession_id) + "_results_lap_chart_data_MULTI.json", "w") as a:
            json.dump(self.iRacingData, a, indent=2)

        with open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
                self.subsession_id) + "_fuzzwah.json", "w") as f:
            json.dump(self.fuzzData, f, indent=2)

        print("[laps_multi] Saved subsession \"" + str(self.subsession_id) + "\" to cache")

    def initFuzzwah(self):
        self.fuzzInstance = Fuzzwah(self.subsession_id)