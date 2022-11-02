import requests

from data.driver import Driver
from data.laps_multi import LapsMulti
from data.laps_single import LapsSingle
from data.race import Race
from data.recentrace import Recent_Race
from data.fuzzwah import Fuzzwah
from diagram.boxplot_multi import BoxplotMulti
from diagram.delta import Delta

from helpers.facade import Facade
from sessionbuilder.session_builder import SessionBuilder

my_sessionBuilder = SessionBuilder()
my_sessionBuilder.authenticate()
session = my_sessionBuilder.session

# driver1 = Driver("Florian Niedermeier2", session)
# cust_id = driver1.cust_id

subsession_id = 51489010
fac = Facade(subsession_id, session)

#boxplotmulti = BoxplotMulti(fac.get_Output("bpm"))

delta = Delta(fac.get_Output("delta"))
