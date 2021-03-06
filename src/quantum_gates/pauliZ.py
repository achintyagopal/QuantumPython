from qGate import QGate

class PauliZ(QGate):

  def apply(self, register, bits, numQubits):
    
    bits = self.check(bits)

    for x in bits:
      result = [0.0 + 0.0j] * len(register)
      if x >= numQubits:
        raise ValueError("Value in bits must be less than number of qubits")

      for y in range(0, len(register)):
        other = y ^ (1 << (numQubits - x - 1))
        if (y >> x) & 1:
          result[y] -= register[y]
        else:
          result[y] += register[y]
      register = result

    return register
