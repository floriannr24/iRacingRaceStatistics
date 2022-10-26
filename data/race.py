import requests


class Race:

    def __init__(self, subsession_id, session):
        self.subsession_id = subsession_id
        self.series_name = None
        self.winner_name = None
        self.track_name = None
        self.requestRace(session)

    def requestRace(self, session):
        racesJson = session.get('https://members-ng.iracing.com/data/results/lap_data', params={"subsession_id": self.subsession_id, "simsession_number":"0"})
        racesDict = racesJson.json()
        racesJson_final = requests.get(racesDict["link"])
        print(racesJson_final.text)





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
