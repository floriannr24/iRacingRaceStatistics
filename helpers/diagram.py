from pip._internal.utils.misc import enum

from data.laps_multi import LapsMulti
from diagram.boxplot_multi import BoxplotMulti
from diagram.delta_multi import DeltaMulti


class Diagram:
    def __init__(self, subession_id, session, config):
        self.subsession_id = subession_id
        self.session = session
        self.config = config.data
        self.inputLaps = None
        self.inputSessionTimes = None
        self.get_Output()

    def get_Output(self):
        match self.config[2]:
            case "bpm":
                return self.get_boxplotMulti_Data()
            # case "bps":
            #   return self.get_boxplotSingle_Data()
            case "delta":
                return self.get_Delta_Data(self.config[0], self.config[1])

    def get_boxplotMulti_Data(self):

        self.inputLaps = LapsMulti(self.subsession_id, self.session).masterBoxPlotMulti()

        output = []

        race_completed_raw = self.extractLaptimes(self.inputLaps, True)
        race_completed_clean = self.scanForInvalidTypes(race_completed_raw, -1, None)

        race_not_completed_raw = self.extractLaptimes(self.inputLaps, False)
        race_not_completed_clean = self.scanForInvalidTypes(race_not_completed_raw, -1, None)

        drivers = self.extractDrivers(self.inputLaps)
        number_of_laps = self.numberOfLapsInRace(self.inputLaps)

        output.append(race_completed_clean)
        output.append(race_not_completed_clean)
        output.append(drivers)
        output.append(number_of_laps)

        return BoxplotMulti(output, 800, 600)

    def get_Delta_Data(self, beforeDrivers, afterDrivers):
        output = LapsMulti(self.subsession_id, self.session).masterDelta(beforeDrivers, afterDrivers)
        return DeltaMulti(output, 950, 600)

    def numberOfLapsInRace(self, reqLaps):
        for driver in reqLaps:
            if driver["result_status"] == "Running":
                return driver["laps_completed"]
            else:
                continue

    def extractDrivers(self, all_laptimes):

        drivers_comp = []
        drivers_notcomp = []

        for lapdata in all_laptimes:
            if lapdata["result_status"] == "Running":
                drivers_comp.append(lapdata["driver"])
            else:
                drivers_notcomp.append(lapdata["driver"])

        return drivers_comp + drivers_notcomp

    def extractLaptimes(self, all_laptimes, raceCompleted):

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

    def scanForInvalidTypes(self, all_laptimes, arg1, arg2):
        cleanLaps1 = []
        cleanLaps2 = []
        for laps in all_laptimes:
            cleanLaps1.append([value for value in laps if value != arg1])
        for laps in cleanLaps1:
            cleanLaps2.append([value for value in laps if value != arg2])
        return cleanLaps2
