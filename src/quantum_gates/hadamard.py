import math

from qGate import QGate

class Hadamard(QGate):

  def apply(self, register, bits, numQubits):

    bits = self.check(bits)

    const = 1/math.sqrt(2)
    
    for x in bits:
      result = [0.0 + 0.0j] * len(register)
      if x >= numQubits:
        raise ValueError("Value in bits must be less than number of qubits")

      for y in range(0, len(register)):
        other = y ^ (1 << (numQubits - x - 1))
        if (y >> (numQubits - x - 1)) & 1:
          result[y] -= const*register[y]
          result[other] += const*register[y]
        else:
          result[y] += const*register[y]
          result[other] += const*register[y]
      register = result

    return register