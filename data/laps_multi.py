import json

import requests
from data.fuzzwah import Fuzzwah


class LapsMulti:
    def __init__(self, subsession_id, session):

        self.subsession_id = subsession_id
        self.session = session
        self.inputLaps = None
        self.lapsJson = None
        self.fuzzResults = None
        self.carclassid = None
        self.fuzzInstance = None

    def masterBoxPlotMulti(self):
        self.requestLapsMulti()
        self.carclassid = self.searchUsersCarClass(self.fuzzInstance.username)

        self.fuzzResults, self.inputLaps = self.filterByCarClass(self.carclassid)
        unique_drivers = self.findUniqueDrivers(self.inputLaps)
        lapsDict = self.bpm_collectInfo(self.inputLaps, unique_drivers)

        return self.sortDictionary(lapsDict)

    def masterDelta(self, beforeDrivers, afterDrivers):
        self.requestLapsMulti()
        self.carclassid = self.searchUsersCarClass(self.fuzzInstance.username)

        self.fuzzResults, self.inputLaps = self.filterByCarClass(self.carclassid)
        unique_drivers = self.findUniqueDrivers(self.inputLaps)
        output_data = self.delta_collectInfo(self.inputLaps, unique_drivers)
        output_data = self.sortDictionary(output_data)
        output_data = self.delta_find_DISQ_DISC(output_data)
        output_data = self.delta_filterDrivers(output_data, beforeDrivers, afterDrivers)
        output_data = self.delta_calcDelta(output_data)

        return output_data

    ####################################################################

    def requestLapsMulti(self):

        load_success = False

        try:
            self.initFuzzwah()
            self.lapsJson, self.fuzzResults = self.cache_load()
            load_success = True
        except FileNotFoundError:
            print('[laps_multi] Files do not exist')

        if not load_success:
            print('[laps_multi] Requesting subsession from iRacing API and Fuzzwah...')

            # Fuzzwah
            self.initFuzzwah()
            self.fuzzResults = self.fuzzInstance.requestResultsSimple()[1]

            # iRacingAPI
            racesJson = self.session.get('https://members-ng.iracing.com/data/results/lap_chart_data',
                                         params={"subsession_id": self.subsession_id, "simsession_number": "0"})
            racesDict = racesJson.json()
            racesJson_final = requests.get(racesDict["link"]).json()

            base_download_url = racesJson_final["chunk_info"]["base_download_url"]
            chunk_file_names = racesJson_final["chunk_info"]["chunk_file_names"][0]

            self.lapsJson = requests.get(base_download_url + chunk_file_names).json()

            self.cache_save()

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
            json.dump(self.lapsJson, a, indent=2)

        with open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/cache/" + str(
                self.subsession_id) + "_fuzzwah.json", "w") as f:
            json.dump(self.fuzzResults, f, indent=2)

        print("[laps_multi] Saved subsession \"" + str(self.subsession_id) + "\" to cache")

    def initFuzzwah(self):
        self.fuzzInstance = Fuzzwah(self.subsession_id)

    ####################################################################

    def convertTimeformatToSeconds(self, laptime):
        if not laptime == -1:
            return laptime / 10000
        else:
            return None

    def searchUsersCarClass(self, username):

        carclassid = None
        for results in self.fuzzResults:
            if results["name"] == username:
                carclassid = results["carclassid"]
                break
            else:
                continue
        return carclassid

    def filterByCarClass(self, carClassIdToFilterFor):
        fuzzNew = []
        fuzzNew_drivers = []
        inputNew = []

        for results in self.fuzzResults:

            if results["carclassid"] == carClassIdToFilterFor:
                fuzzNew.append(results)
                fuzzNew_drivers.append(results["name"])

        for drivers in fuzzNew_drivers:
            for lapdata in self.lapsJson:
                if drivers == lapdata["display_name"]:
                    inputNew.append(lapdata)

        return fuzzNew, inputNew

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

    def sortDictionary(self, lapsDict):
        lapsDict = list(sorted(lapsDict, key=lambda p: p["finish_position"]))

        for lapdata in lapsDict:
            if lapdata["finish_position"] == 0:
                lapsDict.remove(lapdata)
                lapsDict.append(lapdata)

        return lapsDict

    ####################################################################
    def bpm_collectInfo(self, laps_json, unique_drivers):
        lapsDict = []
        for driver in unique_drivers:

            laps = []
            sessionTime = []
            laps_completed_pos = []
            intDict = {
                "driver": driver,
                "finish_position": None,
                "result_status": None,
                "laps_completed": None,
                "laps": laps
            }
            lapsDict.append(intDict)

            # add "finish_position", "laps_completed" to intDict{} via requestLapsMulti()
            for record in laps_json:
                if record["display_name"] == driver:
                    seconds_per_lap = self.cleanAndConvertLapTimes(record["lap_time"], record["lap_number"])
                    laps_completed_pos.append(record["lap_position"])
                    intDict["laps"].append(seconds_per_lap)

            intDict["finish_position"] = laps_completed_pos[len(laps_completed_pos) - 1]
            intDict["laps_completed"] = len(laps_completed_pos) - 1

            # add "Running", "Disq" or "Disconnected" to intDict{} via FuzzwahAPI
            # add "carId" to intDict{} via FuzzwahAPI
            for fuzz in self.fuzzResults:
                if driver == fuzz["name"]:
                    intDict["result_status"] = fuzz["out"]

        return lapsDict

    ####################################################################

    def delta_cleanAndConvertLapTimes_Session(self, lap_time):
        return self.convertTimeformatToSeconds(lap_time)

    def delta_calcDelta(self, lapsDict):

        for i in range(0, len(lapsDict), 1):

            intDelta = []

            for s in range(0, len(lapsDict[i]["session_time"]), 1):
                delta = lapsDict[0]["session_time"][s] - lapsDict[i]["session_time"][s]
                if not delta == 0:
                    delta = round(delta, 2) * (-1)
                intDelta.append(delta)
            lapsDict[i]["delta"] = intDelta

        return lapsDict

    def delta_collectInfo(self, laps_json, unique_drivers):
        lapsDict = []
        for driver in unique_drivers:

            sessionTime = []
            delta = []
            laps_completed_pos = []
            intDict = {
                "driver": driver,
                "result_status": None,
                "laps_completed": None,
                "finish_position": None,
                "session_time": sessionTime,
                "delta": delta

            }
            lapsDict.append(intDict)

            # add "finish_position", "laps_completed" to intDict{} via requestLapsMulti()
            for record in laps_json:
                if record["display_name"] == driver:
                    seconds_per_lap = self.cleanAndConvertLapTimes(record["lap_time"], record["lap_number"])
                    sessionSeconds_per_lap = self.delta_cleanAndConvertLapTimes_Session(record["session_time"])
                    laps_completed_pos.append(record["lap_position"])
                    intDict["session_time"].append(sessionSeconds_per_lap)

            intDict["finish_position"] = laps_completed_pos[len(laps_completed_pos) - 1]
            intDict["laps_completed"] = len(laps_completed_pos) - 1

            # add "Running", "Disq" or "Disconnected" to intDict{} via FuzzwahAPI
            # add "carId" to intDict{} via FuzzwahAPI
            for fuzz in self.fuzzResults:
                if driver == fuzz["name"]:
                    intDict["result_status"] = fuzz["out"]

        return lapsDict

    def delta_find_DISQ_DISC(self, all_laptimes):

        finished = []
        disq_disc = []

        for lapdata in all_laptimes:
            if lapdata["result_status"] == "Running":
                finished.append(lapdata)
            else:
                continue

        for lapdata in all_laptimes:
            if lapdata["result_status"] == "Disqualified" or lapdata["result_status"] == "Disconnected":
                disq_disc.append(lapdata)
            else:
                continue

        return finished + disq_disc

    def delta_filterDrivers(self, data, beforeDrivers, afterDrivers):
        name = self.fuzzInstance.username



        if ((beforeDrivers or afterDrivers) == None) or ((beforeDrivers or afterDrivers) == 0):
            return data
        else:

            foundData = []
            foundIndex = 0

            # searching current driver
            for x in range(0, len(data), 1):
                if data[x]["driver"] == name:
                    foundIndex = x

            up_down = 1

            # adding driver - 1, then driver + 1, then driver -2, +2, -3, +3 to new list
            for i in range(0, beforeDrivers+1, 1):
                if i == 0:
                    foundData.append(data[foundIndex])
                else:
                    foundData.insert(0, data[foundIndex-up_down])
                    up_down += 1

        for data in foundData:
            print(data)


        return foundData








