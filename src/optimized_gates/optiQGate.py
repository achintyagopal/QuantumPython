from abc import ABCMeta, abstractmethod

class QGate(object):
  metaclass = ABCMeta

  @abstractmethod
  def apply(self, register, bits, numQubits):
    pass

  def check(self, bits):
    pass