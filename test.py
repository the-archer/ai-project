

class A():
	def __init__(self, **args):
		self.Qval={}

	def getQ(self):
		self.Qval["sim"]=2
		print self.Qval


b = A()
b.getQ()