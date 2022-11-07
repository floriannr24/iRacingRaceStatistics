from diagram.boxplot_multi import BoxplotMulti
from diagram.delta_multi import DeltaMulti
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


#boxplotmulti = BoxplotMulti(fac.get_Output(config.data))

# diagram = Diagram(config)
# (facete returning diagram according to config)