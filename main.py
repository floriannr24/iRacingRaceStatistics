from helpers.diagram import Diagram, Configurator
from sessionbuilder.session_builder import SessionBuilder

my_sessionBuilder = SessionBuilder()
my_sessionBuilder.authenticate()
session = my_sessionBuilder.session

# driver1 = Driver("Florian Niedermeier2", session)
# cust_id = driver1.cust_id

#subsession_id = [52384481]
subsession_id = [52310798, 52312291, 52332675, 52333422,
                 52348632, 52349354, 52365324, 52380557,
                 52382905, 52384481, 52396190, 52396926]

config = Configurator("pace", "Florian Niedermeier2",
                      setYAxis=0,
                      minVal=63,
                      maxVal=80,
                      setYAxisInterval=1,
                      interval=0.250,
                      showDISC=1,
                      showLaptimes=1,
                      showMean=0,
                      px_width=800,
                      px_height=600)

Diagram(subsession_id, session, config)


