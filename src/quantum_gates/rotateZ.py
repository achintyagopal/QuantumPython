import math

from qGate import QGate

# [ e^-i\phi    0   ]
# [    0     e^i\phi]
class RotateZ(QGate):
  def __init__(self, angle):
    # check angle is real
    if not isinstance(angle, (int, float)):
      raise TypeError("angle must a real number")

    self.angle = angle
  
  def apply(self, register, bits, numQubits):

    bits = self.check(bits)

    const = math.e ** (1j * self.angle/2)
    for x in bits:
      result = [0.0 + 0.0j] * len(register)
      if x >= numQubits:
        raise ValueError("Value in bits must be less than number of qubits")

      for y in range(0, len(register)):
        other = y ^ (1 << (numQubits - x - 1))
        if (y >> (numQubits - x - 1)) & 1:
          result[y] += const * register[y]
        else:
          result[y] += const.conjugate() * register[y]
      register = result

    return register