from qGate import QGate

class CustomGate(QGate):

  def validatePair(self, gateBitPair):
    if not isinstance(gateBitPair, tuple):
      raise TypeError("gatebitpair must be a pair")

    if len(gateBitPair) != 2:
      raise ValueError("gatebitpair must be a tuple of size two a.k.a. a pair")

    gate, bit = gateBitPair

    if not isinstance(gate, QGate):
      raise TypeError("first value of pair must be a QGate")

    if isinstance(bit, int):
      bit = [bit]
    
    if not isinstance(bit, list):
      raise TypeError("second value of pair must be int or list")

    for x in bit:
      if not isinstance(x, int):
        raise TypeError("second value of pair must be int or list of ints")

    if bit < 0:
      raise ValueError("bit must be a positive integer")

  def __init__(self, gateBitPairs):
    if isinstance(gateBitPairs, tuple):
      gateBitPairs = [gateBitPairs]

    if not isinstance(gateBitPairs, list):
      raise TypeError("gateBitPairs must be a list")

    for pair in gateBitPairs:
      self.validatePair(pair)

    self.gateBitPairs = gateBitPairs

  def apply(self, register, bits, numQubits):
    for gate, bit in self.gateBitPairs:
      register = gate.apply(register, bit, numQubits)
    return register