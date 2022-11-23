from diagrams.boxplot_multi import BoxplotMulti
from diagrams.delta_multi import DeltaMulti
from diagrams.pace_compare import PaceCompare
from helpers.data_processor import DataProcessor


class Diagram:

    def __init__(self, subession_id, session, config):
        self.data = self.get_Output(subession_id, session, config)

    def get_Output(self, subsession_id, session, config):
        match config.typeOfDiagram:
            case "bpm":
                dataprocessor = DataProcessor(subsession_id, session)  # create dataprocessor object
                data = dataprocessor.get_boxplotMulti_Data(config.name)  # get, process and return data
                bpm = BoxplotMulti(data, config)  # create diagram
                return bpm
            case "delta":
                dataprocessor = DataProcessor(subsession_id, session)
                data = dataprocessor.get_Delta_Data(0, 0)
                return DeltaMulti(data, 950, 600)
            case "pace":
                dataprocessor = DataProcessor(subsession_id, session)
                data = dataprocessor.get_Pace_Data(config.name)
                return PaceCompare(data, config)


class Configurator:
    def __init__(self, typeOfDiagram, name, **options):
        self.typeOfDiagram = typeOfDiagram
        self.name = name
        self.options = options
