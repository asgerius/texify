import sys
sys.path.append(sys.path[0] + "/..")
from logger import Logger, NullLogger
from dataclasses import dataclass

@dataclass
class DataGenerator:

	def __init__(self):
		self.b = 2
		self.a
		2.and(3)

dg = DataGenerator()
print(dg.__dict__)
print(DataGenerator.a)


