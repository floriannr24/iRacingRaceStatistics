import json
import requests
import numpy
from ir_webstats_rc.client import iRWebStats

class Fuzzwah:
    def __init__(self, subsession_id):
        self.subsession_id = subsession_id
        self.username = self.getCredentials()["email"]
        self.password = self.getCredentials()["password"]
        self.cus_tId = self.getCredentials()["cust_id"]

        irw = iRWebStats()
        irw.login(username=self.username, password=self.password)
        print(irw.cars_driven(custid=self.cus_tId))


    def getCredentials(self):
        return json.load(
            open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/sessionbuilder/files/credentials.json"))


    def requestResultsSimple(self, session):
        print("hello")

