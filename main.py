import requests

from data.driver import Driver
from data.laps_multi import LapsMulti
from data.laps_single import LapsSingle
from data.race import Race
from data.recentrace import Recent_Race
from diagram.boxplot_multi import BoxplotMulti
from sessionbuilder.session_builder import SessionBuilder

my_sessionBuilder = SessionBuilder()
my_sessionBuilder.authenticate()
session = my_sessionBuilder.session

#driver1 = Driver("Florian Niedermeier2", session)
#cust_id = driver1.cust_id

#recentrace = Recent_Race(driver1, 0, session)
subsession_id = 51015041
#https://members.iracing.com/membersite/member/EventResult.do?subsessionid=51015041&custid=817320


lapsmulti = LapsMulti(subsession_id, session)

# for laps in lapsmulti.lapsDict:
#     print(laps)

boxplotmulti = BoxplotMulti(lapsmulti.lapsDict)


















