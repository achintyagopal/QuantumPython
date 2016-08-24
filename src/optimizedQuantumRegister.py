import random
import cmath

from quantumRegister import QReg as SimpleQReg

from quantum_gates.qGate import QGate

maxQubits = 16
degreeOfAccuracy = 1.0e-8


def isOne(value):
  return value >= 1.0 - degreeOfAccuracy and value <= 1.0 + degreeOfAccuracy

""" Quantum register """


class QReg(object):

  def __init__(self, numQubits, bypassError=False, accuracy=8):

    if not isinstance(numQubits, int):
      raise "numQubits must an integer"

    if numQubits > maxQubits and not bypassError:
      raise TypeError("numQubits is too large")

    if not isinstance(bypassError, bool):
      raise TypeError("bypassError must be a boolean")

    if not isinstance(accuracy, int):
      raise TypeError("degreeOfAccuracy must an int")

    degreeOfAccuracy = accuracy
    self.__bypassError = bypassError
    self.__numQubits = numQubits
    self.__register = []
    for _ in range(0, numQubits):
      self.__register.append(SimpleQReg(1, accuracy=accuracy))

  def getRegister(self):
    return self.__register

  def __str__(self):
    pass

  def apply(self, gate, bits=None):
    pass

  def measure(self, bits):
    pass

  def append(self, bits):

    if isinstance(bits, QReg):
      self.__register.append(bits)
      return

    if isinstance(bit, SimpleQReg):
      bits = bits.getRegister()

    if not isinstance(bit, list):
      raise TypeError("Bits must a quantum register or a list")

  def __zeroProb(self, bit):
    pass

  def __oneProb(self, bit):
    pass

  def __measured(self, bit, value):
    pass

  def __renormalize(self):
    pass
