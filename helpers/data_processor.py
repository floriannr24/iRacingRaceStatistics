from data.laps_multi import LapsMulti
from data.results_multi import results_multi


class DataProcessor:
    def __init__(self, subsession_id, session):
        self.subsession_id = self.unpackSubsessionIDs(subsession_id)
        self.session = session
        self.iRacing_lapdata = None
        self.iRacing_results = None

    def get_boxplotMulti_Data(self, name):

        # get session data from iRacingAPI + FuzzwahAPI
        self.iRacing_lapdata = LapsMulti(self.subsession_id, self.session).requestLapsMulti()
        self.iRacing_results = results_multi(self.subsession_id, self.session).requestResultsMulti()

        carclass_id = self.gen_searchUsersCarClass(name)  # search carclass id of user
        iRacing_lapdata_carclass, iRacing_results_carclass = self.gen_filterByCarClass(carclass_id)  # get only data for corresponding carclass
        unique_drivers = self.gen_findUniqueDrivers(iRacing_lapdata_carclass)  # find unique drivers in said carclass

        lapsDict = self.bpm_collectInfo(iRacing_lapdata_carclass, unique_drivers)  # collect info in dictionary
        output = self.gen_sortDictionary(lapsDict)  # sort dictionary by "laps completed" and "finish position"

        race_completed_raw = self.bpm_extractLaptimes(output, True)  # extract all data of completed races
        race_completed_clean = self.bpm_scanForInvalidTypes(race_completed_raw, -1, None)

        race_not_completed_raw = self.bpm_extractLaptimes(output, False)  # extract all data of not completed races
        race_not_completed_clean = self.bpm_scanForInvalidTypes(race_not_completed_raw, -1, None)  # scan for invalid lap-types (-1, 0, None)

        drivers = self.bpm_extractDrivers(output)  # extract a driver list
        number_of_laps = self.bpm_numberOfLapsInRace(output)  # calculate number of laps completed

        output = []

        output.append(race_completed_clean)  # tie everything together
        output.append(race_not_completed_clean)
        output.append(drivers)
        output.append(number_of_laps)

        return output

    def get_Delta_Data(self, beforeDrivers, afterDrivers):

        # get session data from iRacingAPI + FuzzwahAPI
        self.iRacing_lapdata = LapsMulti(self.subsession_id, self.session).requestLapsMulti()

        carclass_id = self.gen_searchUsersCarClass("Florian Niedermeier2")  # search carclass id of user
        iRacingData_carclass, fuzzData_carclass = self.gen_filterByCarClass(carclass_id)  # get only data for corresponding carclass
        unique_drivers = self.gen_findUniqueDrivers(iRacingData_carclass)  # find unique drivers in said carclass

        output_data = self.delta_collectInfo(iRacingData_carclass, unique_drivers)  # collect info in dictionary
        output_data = self.gen_sortDictionary(output_data)  # sort dictionary by "laps completed" and "finish position"
        output_data = self.delta_find_DISQ_DISC(output_data)  # find DISQ / DISC drivers and append them to the end of the dictionary
        # output_data = self.delta_filterDrivers(output_data, beforeDrivers, afterDrivers)
        output = self.delta_calcDelta(output_data)  # calculate delta time to first and add to dictionary

        return output

    def get_Pace_Data(self, name):

        outerDict = {}

        for i, id in enumerate(self.subsession_id):
            irData = LapsMulti(id, self.session).requestLapsMulti()
            metaData = results_multi(id, self.session).requestResultsMulti()

            output = self.pace_collectInfo(irData, name)
            output = self.gen_scanForInvalidTypes(output, -1, None)

            data = {}
            outerDict["race"+str(i)] = data
            data["laps"] = output
            data["metaData"] = metaData

        return outerDict

    ####################################################################

    def gen_searchUsersCarClass(self, username):

        carclassid = None

        for results in self.iRacing_results["session_results"][2]["results"]:
            if results["display_name"] == username:
                carclassid = results["car_class_id"]
                break
            else:
                continue
        return carclassid

    def gen_sortDictionary(self, lapsDict):
        secSortDict = list(sorted(lapsDict, key=lambda p: p["finish_position"]))  # secondary sort by key "finish_position"
        primSortDict = list(sorted(secSortDict, key=lambda p: p["laps_completed"], reverse=True))  # primary sort by key "laps_completed", descending

        for lapdata in primSortDict:
            if lapdata["finish_position"] == 0:
                lapsDict.remove(lapdata)
                lapsDict.append(lapdata)

        return primSortDict

    def gen_filterByCarClass(self, carClassIdToFilterFor):
        iRacing_results_new = []
        iRacing_results_drivers = []
        iRacingData_lapdate_new = []

        for results in self.iRacing_results["session_results"][2]["results"]:

            if results["car_class_id"] == carClassIdToFilterFor:
                iRacing_results_new.append(results)
                iRacing_results_drivers.append(results["display_name"])

        for drivers in iRacing_results_drivers:
            for lapdata in self.iRacing_lapdata:
                if drivers == lapdata["display_name"]:
                    iRacingData_lapdate_new.append(lapdata)

        return iRacingData_lapdate_new, iRacing_results_new

    def gen_findUniqueDrivers(self, laps_json):
        unique_drivers = set()
        for item in laps_json:
            unique_drivers.add(item["display_name"])
        return unique_drivers

    def gen_convertTimeformatToSeconds(self, laptime):
        if not laptime == -1:
            return laptime / 10000
        else:
            return None

    def gen_scanForInvalidTypes(self, laptimes, arg1, arg2):
        return [laptime for laptime in laptimes if laptime != arg1 if laptime != arg2]

    ####################################################################

    def bpm_extractLaptimes(self, all_laptimes, raceCompleted):

        numberOfDrivers = len(all_laptimes)
        drivers_raw = []

        if raceCompleted:
            laps = []
            for lapdata in all_laptimes:
                if lapdata["result_status"] == "Running":
                    laps.append(lapdata["laps"])
                    drivers_raw.append(lapdata["driver"])
                else:
                    continue
            return laps
        else:
            laps = []
            for lapdata in all_laptimes:
                if lapdata["result_status"] == "Disqualified" or lapdata["result_status"] == "Disconnected":
                    laps.append(lapdata["laps"])
                    drivers_raw.append(lapdata["driver"])
                else:
                    continue

            # fill up indices, so DISQ and DISC drivers are put to the last places in the diagram
            indicesToFillUp = numberOfDrivers - len(laps)
            for i in range(indicesToFillUp):
                laps.insert(0, "")
            return laps

    def bpm_cleanAndConvertLapTimes(self, lap_time, lap_number):
        if lap_number > 0:
            if not lap_time == -1:
                seconds = self.gen_convertTimeformatToSeconds(lap_time)
                return seconds
            if lap_time == -1:
                return None
        else:
            return lap_time

    def bpm_scanForInvalidTypes(self, all_laptimes, arg1, arg2):
        cleanLaps = []
        for laps in all_laptimes:
            cleanLaps.append([value for value in laps if value != arg1 if value != arg2])
        return cleanLaps

    def bpm_numberOfLapsInRace(self, reqLaps):
        for driver in reqLaps:
            if driver["result_status"] == "Running":
                return driver["laps_completed"]
            else:
                continue

    def bpm_extractDrivers(self, all_laptimes):

        drivers_comp = []
        drivers_notcomp = []

        for lapdata in all_laptimes:
            if lapdata["result_status"] == "Running":
                drivers_comp.append(lapdata["driver"])
            else:
                drivers_notcomp.append(lapdata["driver"])

        return drivers_comp + drivers_notcomp

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
                    seconds_per_lap = self.bpm_cleanAndConvertLapTimes(record["lap_time"], record["lap_number"])
                    laps_completed_pos.append(record["lap_position"])
                    intDict["laps"].append(seconds_per_lap)

            intDict["finish_position"] = laps_completed_pos[len(laps_completed_pos) - 1]
            intDict["laps_completed"] = len(laps_completed_pos) - 1

            # add "Running", "Disq" or "Disconnected" to intDict{}
            # add "carId" to intDict{}
            for fuzz in self.iRacing_results["session_results"][2]["results"]:
                if driver == fuzz["display_name"]:
                    intDict["result_status"] = fuzz["reason_out"]

        return lapsDict

    ####################################################################

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
        name = "Florian Niedermeier2"

        if ((beforeDrivers or afterDrivers) == None) or ((beforeDrivers or afterDrivers) == 0):
            return data

        foundIndex = 0

        # searching current driver
        for x in range(0, len(data), 1):
            if data[x]["driver"] == name:
                foundIndex = x

        # check if "beforeDrivers" and "afterDrivers" args are valid
        if beforeDrivers + 1 > data[foundIndex]["finish_position"] or afterDrivers > len(data) - 1:
            return data

        else:

            foundData = []

            for i in range(1, beforeDrivers + 1):
                foundData.append(data[foundIndex - (beforeDrivers + 1) + i])

            foundData.append(data[foundIndex])

            for i in range(1, afterDrivers + 1):
                foundData.append(data[foundIndex + i])

        return foundData

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
                    seconds_per_lap = self.bpm_cleanAndConvertLapTimes(record["lap_time"], record["lap_number"])
                    sessionSeconds_per_lap = self.gen_convertTimeformatToSeconds(record["session_time"])
                    laps_completed_pos.append(record["lap_position"])
                    intDict["session_time"].append(sessionSeconds_per_lap)

            intDict["finish_position"] = laps_completed_pos[len(laps_completed_pos) - 1]
            intDict["laps_completed"] = len(laps_completed_pos) - 1

            # add "Running", "Disq" or "Disconnected" to intDict{} via FuzzwahAPI
            # add "carId" to intDict{} via FuzzwahAPI
            for fuzz in self.iRacing_results:
                if driver == fuzz["name"]:
                    intDict["result_status"] = fuzz["out"]

        return lapsDict

    ####################################################################

    def pace_collectInfo(self, irdata, driverName):

        intList = []

        for lap in irdata:
            if lap["display_name"] == driverName:
                laptime = lap["lap_time"]
                laptime = self.gen_convertTimeformatToSeconds(laptime)
                intList.append(laptime)

        return intList

    def unpackSubsessionIDs(self, subsession_id):
        if len(subsession_id) > 1:
            return subsession_id
        else:
            return subsession_id[0]
