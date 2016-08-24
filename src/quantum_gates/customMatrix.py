import numpy as np
import cmath

from qGate import QGate
from ..quantumRegister import degreeOfAccuracy

class CustomMatrix(QGate):

  def __init__(self, matrix):

    if not isinstance(matrix, list):
      raise TypeError("matrix must be a two dimensional list of numbers")

    for x in matrix:
      if not isinstance(x, list):
        raise TypeError("matrix must be a two dimensional list of numbers")
      for y in x:
        if not isinstance(y, (complex, int, float)):
          raise TypeError("matrix must be a two dimensional list of numbers")

    if not self.isSquare(matrix):
      raise ValueError("matrix must be a square matrix")

    if not self.isPowerOfTwo(len(matrix)):
      raise ValueError("the dimensions of the matrix must be a power of two")

    if not self.isUnitary(matrix):
      raise ValueError("matrix must be unitary (U^-1 = U*)")

    self.matrix = matrix

  def isSquare(self, matrix):
    size = len(matrix)
    for x in matrix:
      if size != len(x):
        return False
    return True

  def isPowerOfTwo(self, value):
    return not value & (value - 1)

  def isUnitary(self, matrix):
    conjugate = []
    for i in range(0, len(matrix)):
      row = []
      for j in range(0, len(matrix)):
        row.append(matrix[j][i].conjugate())
      conjugate.append(row)
    product1 = np.around(np.matrix(conjugate) * np.matrix(matrix), decimals=degreeOfAccuracy)
    product2 = np.around(np.matrix(matrix) * np.matrix(conjugate), decimals=degreeOfAccuracy)
    
    if (product1 == np.identity(len(matrix))).all() \
      and (product2 == np.identity(len(matrix))).all():
      return True
    return False

  def apply(self, register, bits, numQubits):
    bits = self.check(bits)

    if len(bits) == 0:
      #multiply self.matrix * register
      if len(register) != len(self.matrix):
        raise ValueError("Too many qubits in register, not " + \
          "big enough matrix")

      return (np.matrix(self.matrix) * np.transpose(np.matrix(register))).tolist()

    if 2 ** len(bits) != len(self.matrix):
      raise ValueError("Number of bits must be log of " + \
        "length of matrix")

    result = [0.0 + 0.0j] * len(register)
    for y in range(0, len(register)):
      
      if register[y] == 0:
        continue

      #calculate column
      columnIndex = 0
      for x in bits:
        if x < 0 or x >= numQubits:
          raise ValueError("Bits must be index of qubit")
        columnIndex = (columnIndex << 1) +  ((y >> (numQubits - x - 1)) & 1)

      column = []
      for rows in self.matrix:
        column.append(rows[columnIndex])

      #convert columnIndex where all bit in bits is set to 0 -> rowIdx
      rowIdx = y;
      for x in bits:
        rowIdx = rowIdx & (~(1 << (numQubits - x - 1)));

      for idx in range(0, len(column)):      
        value = column[idx]
        if value == 0:
          continue
        
        row = rowIdx
        
        for z in range(0, len(bits)):
          if (idx >> (len(bits) - z - 1)) & 1:
            #put a one in bit[z] in row
            row |= (1 << (numQubits - bits[z] - 1))
        
        result[row] += value*register[y]

    return result

