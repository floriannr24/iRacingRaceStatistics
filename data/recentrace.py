import requests


class Recent_Race:

    def __init__(self, driver, race_nr, session):
        self.subsession_id = None
        self.driver = driver
        self.raceNr = race_nr * -1
        self.series_name = None
        self.winner_name = None
        self.track_name = None
        self.session_start_time = None
        self.requestRace(session, race_nr)

    def requestRace(self, session, race_nr):
        racesJson = session.get('https://members-ng.iracing.com/data/stats/member_recent_races', params={"search_term": self.driver.cust_id})
        racesDict = racesJson.json()
        racesJson_final = requests.get(racesDict["link"])
        racesDict_final = racesJson_final.json()["races"][race_nr]

        self.subsession_id = racesDict_final["subsession_id"]
        self.series_name = racesDict_final["series_name"]
        self.winner_name = racesDict_final["winner_name"]
        self.track_name = racesDict_final["track"]["track_name"]
        self.session_start_time = racesDict_final["session_start_time"]


# {{'season_id': 3852,
#   'series_id': 112,
#   'series_name': 'Production Car Sim-Lab Challenge',
#   'car_id': 67,
#   'car_class_id': 74,
#   'livery': {'car_id': 67, 'pattern': 0, 'color1': 'ffde00', 'color2': '000000', 'color3': '000000'},
#   'license_level': 9,
#   'session_start_time': '2022-10-17T19:30:00Z',
#   'winner_group_id': 40485,
#   'winner_name': 'Reuben Bonnici',
#   'winner_helmet': {'pattern': 14, 'color1': '46b8f4', 'color2': '4589f6', 'color3': 'fef8ec', 'face_type': 0, 'helmet_type': 0},
#   'winner_license_level': 18,
#   'start_position': 6,
#   'finish_position': 9,
#   'qualifying_time': 0,
#   'laps': 14,
#   'laps_led': 0,
#   'incidents': 2,
#   'club_points': 0,
#   'points': 28,
#   'strength_of_field': 2495,
#   'subsession_id': 51632947,
#   'old_sub_level': 166,
#   'new_sub_level': 186,
#   'oldi_rating': 2166,
#   'newi_rating': 2124,
#   'track': {'track_id': 166, 'track_name': 'Okayama International Circuit'}
