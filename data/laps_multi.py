import requests

from data.fuzzwah import Fuzzwah


class LapsMulti:
    def __init__(self, subsession_id, session):
        self.subsession_id = subsession_id
        self.session = session
        self.inputLaps = None
        self.lapsJson = None
        self.fuzzResults = Fuzzwah(subsession_id).resultsSimple[1]
        self.lapsDict = self.requestLapsMulti(session)


    def requestLapsMulti(self, session):
        racesJson = session.get('https://members-ng.iracing.com/data/results/lap_chart_data',
                                params={"subsession_id": self.subsession_id, "simsession_number": "0"})
        racesDict = racesJson.json()
        racesJson_final = requests.get(racesDict["link"]).json()

        base_download_url = racesJson_final["chunk_info"]["base_download_url"]
        chunk_file_names = racesJson_final["chunk_info"]["chunk_file_names"][0]

        self.lapsJson = requests.get(base_download_url + chunk_file_names).json()

        ########## t e m p #########
        # self.inputLaps = json.load(
        #     open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/data/files/results_lap_chart_data_MULTIUSER.json"))

        self.fuzzResults, self.inputLaps = self.filterByCar(67)

        unique_drivers = self.findUniqueDrivers(self.inputLaps)
        lapsDict = self.collectInfo(self.inputLaps, unique_drivers)

        return self.sortDictionary(lapsDict)

    def sortDictionary(self, lapsDict):
        lapsDict = list(sorted(lapsDict, key=lambda p: p["finish_position"]))

        for lapdata in lapsDict:
            if lapdata["finish_position"] == 0:
                lapsDict.remove(lapdata)
                lapsDict.append(lapdata)

        return lapsDict

    def filterByCar(self, carIdToFilterFor):
        fuzzNew = []
        fuzzNew_drivers = []
        inputNew = []

        for results in self.fuzzResults:
            if results["carid"] == carIdToFilterFor:
                fuzzNew.append(results)
                fuzzNew_drivers.append(results["name"])


        for drivers in fuzzNew_drivers:
            for lapdata in self.lapsJson:
                if drivers == lapdata["display_name"]:
                    inputNew.append(lapdata)

        return fuzzNew, inputNew







        return fuzzNew, inputNew

    def collectInfo(self, laps_json, unique_drivers):
        lapsDict = []
        for driver in unique_drivers:

            laps = []
            laps_completed_pos = []
            intDict = {
                "driver": driver,
                "finish_position": None,
                "result_status": None,
                "laps_completed": None,
                "car_id": None,
                "laps": laps
            }
            lapsDict.append(intDict)

            # add "finish_position", "laps_completed" to intDict{} via requestLapsMulti()
            for record in laps_json:
                if record["display_name"] == driver:
                    seconds = self.cleanAndConvertLapTimes(record["lap_time"], record["lap_number"])
                    laps_completed_pos.append(record["lap_position"])
                    intDict["laps"].append(seconds)
            intDict["finish_position"] = laps_completed_pos[len(laps_completed_pos) - 1]
            intDict["laps_completed"] = len(laps_completed_pos) - 1

            # add "Running", "Disq" or "Disconnected" to intDict{} via FuzzwahAPI
            # add "carId" to intDict{} via FuzzwahAPI
            for fuzz in self.fuzzResults:
                if driver == fuzz["name"]:
                    intDict["result_status"] = fuzz["out"]
                    intDict["car_id"] = fuzz["car"]

        return lapsDict

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
