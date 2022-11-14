from helpers.diagram import Diagram, Configurator
from sessionbuilder.session_builder import SessionBuilder

my_sessionBuilder = SessionBuilder()
my_sessionBuilder.authenticate()
session = my_sessionBuilder.session

# driver1 = Driver("Florian Niedermeier2", session)
# cust_id = driver1.cust_id

subsession_id = 52167419

config = Configurator("bpm", "Florian Niedermeier2",
                      setYAxis=0,
                      minVal=0,
                      maxVal=0,
                      setYAxisInterval=1,
                      interval=0.5,
                      showDISC=1,
                      showLaptimes=0,
                      showMean=0,
                      px_width=800,
                      px_height=600)

Diagram(subsession_id, session, config)
