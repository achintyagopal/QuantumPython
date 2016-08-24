from qGate import QGate

class Control(QGate):

  def __init__(self, gate, controlBits):
    if not isinstance(gate, QGate):
      raise TypeError("gate must be of type QGate")

    controlBits = self.check(controlBits)
    
    self.gate = gate
    self.controlBits = controlBits

  def apply(self, register, bits, numQubits):

    result = [0.0 + 0.0j] * len(register)
  
    bits = self.check(bits)

    for y in range(0, len(register)):
      control = True
      for x in self.controlBits:       
        if not (y >> (numQubits - x - 1)) & 1:
          control = False
          break
      if control:
        result[y] += register[y]

    
    result = self.gate.apply(result, bits, numQubits)
    
    for y in range(0, len(register)):
      control = True
      for x in self.controlBits:       
        if not (y >> (numQubits - x - 1)) & 1:
          control = False
          break
      if not control:
        result[y] += register[y]

    return result  