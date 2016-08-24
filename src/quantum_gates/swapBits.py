from qGate import QGate

class SwapBits(QGate):

  def apply(self, bits, register, numQubits):
    bits = self.check(bits)

    if len(bits) != 2:
      raise ValueError("Can only swap two bits")

    bitOne = bits[0]
    bitTwo = bits[1]
    bitOne = numQubits - bitOne - 1
    bitTwo = numQubits - bitTwo - 1

    result = [0.0 + 0.0j] * len(register)
    if bitOne >= numQubits:
      raise ValueError("Value in bits must be less than number of qubits")

    if bitTwo >= numQubits:
      raise ValueError("Value in bits must be less than number of qubits")

    for y in range(0, len(register)):
      valueOne = (y >> bitOne) & 1
      valueTwo = (y >> bitTwo) & 1
      if valueOne == valueTwo:
        result[y] += register[y]
      else:
        other = y ^ (1 << bitOne)
        other = other ^ (1 << bitTwo)
        result[other] += registe[y]
    return result