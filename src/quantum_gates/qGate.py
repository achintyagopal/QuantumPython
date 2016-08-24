from abc import ABCMeta, abstractmethod

class QGate(object):
  metaclass = ABCMeta

  @abstractmethod
  def apply(self, register, bits, numQubits):
    pass

  def check(self, bits):
    if isinstance(bits, int):
      bits = [bits]

    if not isinstance(bits, list):
      raise TypeError("bits must be a list of ints or an int")

    for x in bits:      
      if not isinstance(x, int):
        raise TypeError("bits must be a list of ints")
      if x < 0:
        raise ValueError("ints in bits must be a positive integer")

    return bits