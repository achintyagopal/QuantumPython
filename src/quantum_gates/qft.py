import math

from qGate import QGate
from hadamard import Hadamard
from controlGate import Control
from phaseShift import PhaseShift
from swapBits import SwapBits

class QuantumFourierTransform(QGate):

  def apply(self, register, bits, numQubits):
    if bits == []:
      return

    bits = self.check(bits)

    register = self.__qft(register, bits, numQubits)
    #swap bits
    for x in range(0, len(bits)/2 - 1):
      SwapBits().apply(register, [bits[x], bits[len(bits) - 1 - x]])

    return register

  def __qft(self, register, bits, numQubits):

    bit = bits[0]
    n = len(bits)
    register = Hadamard().apply(register, bit, numQubits)
  
    if n > 1:
      bits.pop(0)
      for x in range(0, len(bits)):
        register = Control(PhaseShift(math.pi/(2 ** (x))), bits[x]).apply(register, bit, numQubits)
      register = self.__qft(register, bits, numQubits)
    elif n < 1:
      raise TypeError("Programmer fucked up")

    return register