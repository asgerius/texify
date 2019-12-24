import numpy as np


class Function:

	fun: callable
	args: list
	tex: str

	def __init__(self, args: list):

		self.args = args

	def __call__(self):

		return self.fun(*[arg() for arg in self.args])

	def __str__(self):

		return f"Function {self.__class__.__name__} with args: " + ", ".join(x.__class__.__name__ for x in self.args)

class Value:

	value: str
	tex: str

	def __init__(self, value: str, tex: str):

		self.value = value
		self.tex = tex

	def __call__(self):

		try:
			return float(self.value)
		except ValueError as e:
			raise ValueError(str(e) + f" in leaf with value {self.value}")

	def __str__(self):

		return f"Value {self.value}"

class Add(Function):

	@staticmethod
	def fun(x, y):
		return x + y

a = Value("2", "asdsd")
b = Value("3", "asd")
c = Add([a, Value("4", "asd")])
print(a)
print(b)
print(c)
add = Add([b, c])
print(add)
print(add())

