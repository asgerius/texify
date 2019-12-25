import numpy as np


class Function:

	fun: callable
	args: list
	tex: callable
	# Priority for parentheses
	# 0: +, -
	# 1: *
	# 2: /
	# 3: ^, functions
	priority: int = 3

	leftpar = r"\left("
	rightpar = r"\right)"

	def __init__(self, args: list):

		if not (type(args) == list or type(args) == tuple):
			args = [args]
		self.args = args

	def __call__(self):

		return self.fun(*[arg() for arg in self.args])

	def __str__(self):

		return f"Function {self.__class__.__name__} with args: " + ", ".join(x.__class__.__name__ for x in self.args)

class Value:

	def __init__(self, value):

		self.value = value

	def __call__(self):

		return self.value

	def __str__(self):

		return f"Value {self.value}"
	
	def tex(self, _):

		return str(self.value)

class Matrix(Value):

	value: np.ndarray

	def __str__(self):

		return f"Matrix {self.value}"
	
	def _isvector(self):

		return len(self.value.squeeze()) == 1

	def tex(self, _):

		left = r"\left[\begin{array}"
		right = r"\end{array}\right]"
		if self._isvector():
			mat = np.array2string(self.value, seperator=r"\\")
		else:
			mat = np.apply_along_axis(lambda x: "&".join([str(y) for y in x]), 0, self.value)
			mat = np.array2string(mat, seperator=r"\\")
		return left + mat + right

class Add(Function):

	priority = 0

	@staticmethod
	def fun(x, y):
		return x + y
	
	def tex(self, parent_priority: int = 3):
		tex = f"{self.args[0].tex(self.priority)} + {self.args[1].tex(self.priority)}"
		if self.priority < parent_priority:
			tex = self.leftpar + tex + self.rightpar
		return tex

class Subtract(Function):

	priority = 0

	@staticmethod
	def fun(x, y):
		return x - y
	
	def tex(self, parent_priority: int = 3):
		tex = f"{self.args[0].tex(self.priority)} - {self.args[1].tex(self.priority)}"
		if self.priority < parent_priority:
			tex = self.leftpar + tex + self.rightpar
		return tex

class Multiply(Function):

	priority = 1

	@staticmethod
	def fun(x, y):
		return np.dot(x, y)
	
	def tex(self, parent_priority: int = 3):
		tex = f"{self.args[0].tex(self.priority)} \\cdot {self.args[1].tex(self.priority)}"
		if self.priority < parent_priority:
			tex = self.leftpar + tex + self.rightpar
		return tex

class Divide(Function):

	priority = 2

	@staticmethod
	def fun(x, y):
		return x / y
	
	def tex(self, parent_priority: int = 3):
		tex = f"\\frac{{{self.args[0].tex(self.priority)}}}{{{self.args[1].tex(self.priority)}}}"
		if self.priority < parent_priority:
			tex = self.leftpar + tex + self.rightpar
		return tex

class Pow(Function):

	@staticmethod
	def fun(x, y):
		return x ** y
	
	def tex(self, parent_priority: int = 3):
		tex = f"{self.args[0].tex(self.priority)} ^ {{{self.args[1].tex(self.priority)}}}"
		if self.priority < parent_priority:
			tex = self.leftpar + tex + self.rightpar
		return tex

class Sin(Function):

	@staticmethod
	def fun(x):
		return np.sin(x)
	
	def tex(self, parent_priority: int = 3):
		return f"\\sin{self.leftpar}{self.args[0].tex(self.priority)}{self.rightpar}"

if __name__ == "__main__":
	# Test 2 + sin(3 * (4 + 2))
	a = Value(2)
	b = Value(3)
	c = Value(4)
	d = Add([a, c])
	e = Multiply([b, d])
	f = Add([a, Sin(e)])
	print(f())
	print(f.tex(0))

