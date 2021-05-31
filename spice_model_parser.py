import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Spice.Parser import SpiceParser

from PySpice.Spice.NgSpice.Shared import NgSpiceShared


ngspice = NgSpiceShared.new_instance()

f = open("yourstudentnumber.cir")
cir = "".join(f.readlines())

ngspice.load_circuit(cir)
f.close()

print(cir)