class Frank(object):
	def __init__(self, bob):
		self.bob = bob
	def __cmp__(self, other):
		return self.bob - other.bob

franky = Frank(10)
franklin = Frank(2)
franks_list = [franky, franklin]
print min(franks_list).bob