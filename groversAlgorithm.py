import math
import random

from src.quantumRegister import QReg

from src.quantum_gates.customMatrix import CustomMatrix
from src.quantum_gates.controlGate import Control
from src.quantum_gates.customGate import CustomGate
from src.quantum_gates.hadamard import Hadamard
from src.quantum_gates.pauliX import PauliX

def getSearchBit(numQubits):
  searchBit = int(random.random() * (numQubits))
  print "The correct answer is " + `searchBit`
  return searchBit

""" numQubits is the number of bits the index could be, returned 
is a gate which handles numQubits + 1 bits where the last is flipped 
if the first numQubits bits are equal to the index """
def randOracle(numQubits):
  searchBit = getSearchBit(2 ** numQubits)
  controlBits = []
  notControlBits = []
  for x in range(0, numQubits):
    if (searchBit >> x) & 1:
      controlBits.append(numQubits - x - 1)
    else:
      notControlBits.append(numQubits - x - 1)

  bits = []
  for x in range(0, numQubits):
    bits.append(x)

  if notControlBits == []:
    return CustomGate([(Control(PauliX(), bits), numQubits)])
  else:
    return CustomGate([(PauliX(), notControlBits),(Control(PauliX(), bits), numQubits),(PauliX(), notControlBits)])

def randOracle2(numQubits):
  searchBit = getSearchBit(2 ** numQubits)

  matrix = []
  for x in range(0, 2 ** numQubits):
    row = []
    for y in range(0, 2 ** numQubits):
      if x == y:
        if y == searchBit:
          row.append(-1)
        else:
          row.append(1)
      else:
        row.append(0)
    matrix.append(row)
  return CustomMatrix(matrix)

def createDiffusionOperator(numQubits):
  matrix = []
  for x in range(0, 2**numQubits):
    row = []
    for y in range(0, 2**numQubits):
      if x == y:
        if x == 0:
          row.append(1)
        else:
          row.append(-1)
      else:
        row.append(0)
    matrix.append(row)
  return CustomMatrix(matrix)

def correct(oracle, guess, numQubits):
  
  if guess == None:
    return False

  print "Guess: " + `guess`
  tempRegister = QReg(numQubits)
  length = len(bin(guess)) - 2
  for x in range(0, length):
    if (guess >> x) & 1:
      tempRegister.apply(PauliX(), numQubits - x - 1)

  tempRegister.append([1,0])
  tempRegister.apply(oracle, [])

  measuredSet = tempRegister.measure(numQubits)
  return measuredSet == [1]

numQubits = 8
guess = None
oracle = randOracle(numQubits)
diffusion = createDiffusionOperator(numQubits)

bits = []
for x in range(0, numQubits):
  bits.append(x)

while not correct(oracle, guess, numQubits):
  
  register = QReg(numQubits + 1)

  #initialize
  register.apply(PauliX(), numQubits)

  #first step, hadamard
  register.apply(Hadamard())

  #repeat sqrt(n) times
  # for _ in range(0, int(math.ceil(math.sqrt(2 ** numQubits))) - 1):
    #second step, apply oracle
  register.apply(oracle)

  #third step, grover diffusion operator
  register.apply(Hadamard(), bits)
  register.apply(diffusion, bits)
  register.apply(Hadamard(), bits)

  measureSet = register.measure(bits)
  guess = 0
  for x in measureSet:
    guess = (guess << 1) | x

# import inspect
# print inspect.getsource(Hadamard)