import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "quantum_gates"))

import collections
import math
import numpy as np

from optimizedQuantumRegister import QReg

x = QReg(8, True)
print x