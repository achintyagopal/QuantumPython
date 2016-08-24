from quantum_gates.qGate import QGate
import random
import cmath

maxQubits = 16
degreeOfAccuracy = 8

def isOne(value):
  return value >= 1.0 - (10 ** (-1 * degreeOfAccuracy)) and value <= 1.0 + (10 ** (-1 * degreeOfAccuracy))

""" Quantum register """
class QReg(object):

  def __init__(self, numQubits, bypassError = False, accuracy = 8):

    if not isinstance(numQubits, int):
      raise TypeError("numQubits must an integer")

    if numQubits > maxQubits and not bypassError:
      raise TypeError("numQubits is too large")

    if not isinstance(bypassError, bool):
      raise TypeError("bypassError must be a boolean")

    if not isinstance(accuracy, int):
      raise TypeError("degreeOfAccuracy must an int")
    
    degreeOfAccuracy = accuracy
    self.__bypassError = bypassError
    self.__numQubits = numQubits
    self.__register = [0.0 + 0.0j]*(2**self.__numQubits)
    self.__register[0] = 1

  def getRegister(self):
    return self.__register

  def __str__(self):
    value = ""
    for x in range(0, 2 ** self.__numQubits):
      y = self.__register[x]
      if y == 0:
        continue

      #check if can remove certain amount of accuracy from numbers
      if value == "":
        value = str(y) + "|" + str(x) + ">"
      else:
        value += " + " + str(y) + "|" + str(x) + ">"
    return value

  def apply(self, gate, bits=None):
    if bits == None:
      bits = []
      for x in range(0, self.__numQubits):
        bits.append(x)

    if not isinstance(gate, QGate):
      raise TypeError("gate must be of type QGate")

    self.__register = gate.apply(self.__register, bits, self.__numQubits)
    return self

  def measure(self, bits):

    bits = QGate().check(bits)
    
    measurements = []
    for bit in bits:

      bit = self.__numQubits - bit - 1

      if bit >= self.__numQubits:
        raise ValueError("Value in bits must be less than number of qubits")

      measure = random.random()
      measuredValue = 0
      if self.__zeroProb(bit) <= measure:
        measuredValue = 1
        
      self.__register = self.__measured(bit, measuredValue)
      measurements.append(measuredValue)
      self.__register = self.__renormalize()

    return measurements

  def append(self, bits):

    if isinstance(bits, QReg):
      bits = QReg.getRegister()

    if not isinstance(bits, list):
      raise TypeError("bits must be a list")

    if len(bits) & (len(bits) - 1):
      raise ValueError("length of list of bits must be a power of two")

    for bit in bits:
      if not isinstance(bit, (int, complex, float)):
        raise TypeError("values in bit list must a number")

    totalProb = 0
    for bit in bits:
      totalProb += bit * (bit+0j).conjugate()
    totalProb = totalProb.real
    
    if not isOne(totalProb):
      raise ValueError("Total probability of a bit must equal 1 " + \
        "not " + str(totalProb))

    self.__numQubits += len(bin(len(bits) - 1)) - 2
  
    if self.__numQubits > maxQubits and not self.__bypassError:
      raise TypeError("numQubits is too large")
    
    result = []
    for x in self.__register:
      for y in bits:
        result.append(x*y)

    self.__register = result

  def __zeroProb(self, bit):

    prob = 0
    for y in range(0, len(self.__register)):
      other = y ^ (1 << bit)
      if not (y >> bit) & 1:
        prob += self.__register[y] * self.__register[y].conjugate()
    return prob.real

  def __oneProb(self, bit):
    prob = 0
    for y in range(0, len(self.__register)):
      other = y ^ (1 << bit)
      if (y >> bit) & 1:
        prob += self.__register[y] * self.__register[y].conjugate()
    return prob.real

  def __measured(self, bit, value):
    for y in range(0, len(self.__register)):
      if (y >> bit) & 1 != value:
        self.__register[y] = 0
    return self.__register

  def __renormalize(self):
    value = 0
    for y in self.__register:
      value += y * y.conjugate()

    const = 1/cmath.sqrt(value)
    for y in range(0, len(self.__register)):
      self.__register[y] *= const
    return self.__register