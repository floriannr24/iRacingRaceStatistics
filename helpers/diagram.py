from diagrams.boxplot_multi import BoxplotMulti
from diagrams.delta_multi import DeltaMulti
from helpers.data_processor import DataProcessor


class Diagram:
    def __init__(self, subession_id, session, config):
        self.get_Output(subession_id, session, config)

    def get_Output(self, subsession_id, session, config):
        match config.typeOfDiagram:
            case "bpm":
                dataprocessor = DataProcessor(subsession_id, session)  # create dataprocessor object
                data = dataprocessor.get_boxplotMulti_Data()  # get, process and return data
                return BoxplotMulti(data, config)  # create diagram
            case "delta":
                dataprocessor = DataProcessor(subsession_id, session)
                data = dataprocessor.get_Delta_Data(0, 0)
                return DeltaMulti(data, 950, 600)


class Configurator:
    def __init__(self, typeOfDiagram, **options):
        self.typeOfDiagram = typeOfDiagram
        self.options = options
