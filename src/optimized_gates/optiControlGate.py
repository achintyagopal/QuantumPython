from qGate import QGate

from ..quantum_gates.controlGate import Control as SimpleControl

class Control(QGate):

  def __init__(self, gate, controlBits):
    self.gate = SimpleControl(gate, controlBits)

  def apply(self, register, bits, numQubits):
    pass