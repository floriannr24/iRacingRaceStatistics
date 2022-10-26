import json
import requests


class LapsMulti:
    def __init__(self, subsession_id, session):
        self.subsession_id = subsession_id
        self.session = session
        self.number_of_records = None
        self.laps = None
        self.lapsCollection = None
        self.requestLapsMulti(session)

    def requestLapsMulti(self, session):
        # racesJson = session.get('https://members-ng.iracing.com/data/results/lap/chart/data', params={"subsession_id": self.subsession_id, "simsession_number": "0"})
        # racesDict = racesJson.json()
        # racesJson_final = requests.get(racesDict["link"]).json()
        #
        # base_download_url = racesJson_final["chunk_info"]["base_download_url"]
        # chunk_file_names = racesJson_final["chunk_info"]["chunk_file_names"][0]
        #
        # laps = requests.get(base_download_url+chunk_file_names).json()[0]

        ########## t e m p #########

        laps_json = json.load(
            open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/files/results_lap_chart_data_MULTIUSER.json"))

        ######### t e m p #########

        self.number_of_records = len(laps_json)

        unique_drivers = set()

        for item in laps_json:
            unique_drivers.add(item["cust_id"])

        # ToDo: actual number of laps -> fill missing laptimes with None

        self.lapsCollection = []

        for driver in unique_drivers:
            self.laps = []

            for record in laps_json:
                if record["cust_id"] == driver:
                    value = record["lap_time"]
                    seconds = self.convertTimeformatToSeconds(value)
                    self.laps.append(seconds)
            self.lapsCollection.append(self.laps)

        for x in self.lapsCollection:
            print(x)

    def convertTimeformatToSeconds(self, laptime):
        if not laptime == -1:
            return laptime / 10000
        else:
            return laptime
