import json
import requests


class LapsSingle:
    def __init__(self, subsession_id, session):
        self.subsession_id = subsession_id
        self.session = session
        self.number_of_laps = None
        self.laps = None
        self.requestLapsSingle(session)

    def requestLapsSingle(self, session):
        # racesJson = session.get('https://members-ng.iracing.com/data/results/lap_data', params={"subsession_id": self.subsession_id, "simsession_number": "0"})
        # racesDict = racesJson.json()
        # racesJson_final = requests.get(racesDict["link"]).json()
        #
        # base_download_url = racesJson_final["chunk_info"]["base_download_url"]
        # chunk_file_names = racesJson_final["chunk_info"]["chunk_file_names"][0]
        #
        # laps = requests.get(base_download_url+chunk_file_names).json()[0]

        ########## t e m p #########

        laps_json = json.load(open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/files/results_lap_data_SINGLE.json"))

        ######### t e m p #########

        self.number_of_laps = len(laps_json)

        self.laps = []

        for lap in laps_json:
            value = lap["lap_time"]
            seconds = self.convertTimeformatToSeconds(value)
            self.laps.append(seconds)

        print(self.laps)


    def convertTimeformatToSeconds(self, laptime):
        if not laptime == -1:
            return laptime / 10000
        else:
            return laptime












