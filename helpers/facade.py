from data.laps_multi import LapsMulti


class Facade:
    def __init__(self, subession_Id, session):
        self.requestedLaps = LapsMulti(subession_Id, session).lapsDict
        self.outputLaps = self.get_boxplotMulti_Data()

    def get_boxplotMulti_Data(self):
        outputlaps = []

        race_completed_raw = self.extractLaptimes(self.requestedLaps, True)
        race_completed_clean = self.scanForInvalidTypes(race_completed_raw, -1, None)

        race_not_completed_raw = self.extractLaptimes(self.requestedLaps, False)
        race_not_completed_clean = self.scanForInvalidTypes(race_not_completed_raw, -1, None)

        drivers_raw = self.extractDrivers(self.requestedLaps)
        number_of_laps = self.numberOfLapsInRace(self.requestedLaps)

        outputlaps.append(race_completed_clean)
        outputlaps.append(race_not_completed_clean)
        outputlaps.append(drivers_raw)
        outputlaps.append(number_of_laps)

        return outputlaps

    def numberOfLapsInRace(self, reqLaps):
        for driver in reqLaps:
            if driver["result_status"] == "Running":
                return driver["laps_completed"]
            else:
                continue

    def extractDrivers(self, all_laptimes):

        drivers = []
        for lapdata in all_laptimes:
            drivers.append(lapdata["driver"])
        return drivers

    def extractLaptimes(self, all_laptimes, raceCompleted):

        numberOfLapsInRace = all_laptimes[0]["laps_completed"]
        numberOfDrivers = len(all_laptimes)

        if raceCompleted:
            laps = []
            for lapdata in all_laptimes:
                if lapdata["result_status"] == "Running":
                    laps.append(lapdata["laps"])
                else:
                    continue
            return laps

        else:
            laps = []
            for lapdata in all_laptimes:
                if lapdata["result_status"] == "Disqualified" or lapdata["result_status"] == "Disconnected":
                    laps.append(lapdata["laps"])
                else:
                    continue

            indicesToFillUp = numberOfDrivers - len(laps)
            for i in range(indicesToFillUp):
                laps.insert(0, "")
            return laps

    def scanForInvalidTypes(self, all_laptimes, arg1, arg2):
        cleanLaps1 = []
        cleanLaps2 = []
        for laps in all_laptimes:
            cleanLaps1.append([value for value in laps if value != arg1])
        for laps in cleanLaps1:
            cleanLaps2.append([value for value in laps if value != arg2])
        return cleanLaps2



