import json
import requests
import numpy


class LapsMulti:
    def __init__(self, subsession_id, session):
        self.subsession_id = subsession_id
        self.session = session
        self.lapsDict = self.requestLapsMulti(session)


    # ToDo: actual number of laps -> fill missing laptimes with None

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

        unique_drivers = self.findUniqueDrivers(laps_json)

        return self.collectInfo(laps_json, unique_drivers)

    def collectInfo(self, laps_json, unique_drivers):
        self.lapsDict = []
        for driver in unique_drivers:

            laps = []
            intDict = {
                "driver": driver,
                "finish_position": None,
                "laps": laps
            }
            self.lapsDict.append(intDict)

            for record in laps_json:
                if record["display_name"] == driver:
                    seconds = self.cleanAndConvertLapTimes(record["lap_time"], record["lap_number"])
                    intDict["laps"].append(seconds)
        return self.lapsDict

    def findUniqueDrivers(self, laps_json):
        unique_drivers = set()
        for item in laps_json:
            unique_drivers.add(item["display_name"])
        return unique_drivers

    def cleanAndConvertLapTimes(self, lap_time, lap_number):
        if lap_number > 0:
            if not lap_time == -1:
                seconds = self.convertTimeformatToSeconds(lap_time)
                return seconds
            if lap_time == -1:
                return None
        else:
            return lap_time

    def convertTimeformatToSeconds(self, laptime):
        if not laptime == -1:
            return laptime / 10000
        else:
            return None
