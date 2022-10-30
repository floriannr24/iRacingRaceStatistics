import json
import requests
import numpy
from ir_webstats_rc.client import iRWebStats

class Fuzzwah:
    def __init__(self, subsession_id):
        self.subsession_id = subsession_id
        self.email = self.getCredentials()["email"]
        self.password = self.getCredentials()["password"]
        self.cust_Id = self.getCredentials()["cust_id"]
        self.username = self.getCredentials()["username"]
        self.irw = iRWebStats()
        self.irw.login(username=self.email, password=self.password)
        self.resultsSimple = self.requestResultsSimple()

    def getCredentials(self):
        return json.load(
            open("C:/Users/FSX-P/IdeaProjects/iRacingRaceStatistics/sessionbuilder/files/credentials.json"))

    def requestResultsSimple(self):
        return self.irw.event_results(self.subsession_id)


