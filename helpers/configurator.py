from helpers.facade import Facade


class Configurator:
    def __init__(self, driversBefore, driversAfter, typeOfDiagram):
        self.data = [driversBefore, driversAfter, typeOfDiagram]