from helpers.configurator import Configurator
from helpers.diagram import Diagram
from sessionbuilder.session_builder import SessionBuilder

my_sessionBuilder = SessionBuilder()
my_sessionBuilder.authenticate()
session = my_sessionBuilder.session

# driver1 = Driver("Florian Niedermeier2", session)
# cust_id = driver1.cust_id

subsession_id = 52167419

config = Configurator(None, None, "delta")

Diagram(subsession_id, session, config)
