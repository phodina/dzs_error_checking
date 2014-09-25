#!/usr/bin/python3

class Circuit_Checker:
	
	def __init__ (self, inputs):
		self.inputs = inputs;
		self.rows = int (2**self.inputs);
		
		self.count = self.rows
		
		self.truth_matrix = [[0 for i in range(self.inputs)] for i in range(self.rows)]
		self.error_matrix = [[0 for i in range((self.inputs+1)*2)] for i in range(self.rows)]
		self.diff_matrix = [[0 for i in range((self.inputs+1)*2)] for i in range(self.rows)]
		
		self.error_sum = [0 for i in range(self.rows)]
		self.covered_rows = [[] for i in range(self.rows)]
		self.covered_inputs = []
		
		for c in range (0, self.inputs):
			self.count = int (self.count/2)
			
			r = 0
			while r < self.rows:
				for i in range (0, self.count):
					self.truth_matrix[r][c] = 0
					r += 1
				for i in range (0, self.count):
					self.truth_matrix[r][c] = 1
					r += 1
	
	def logic_function (self, in_v):
		output = ((in_v[0] or in_v[1]) and (not(in_v[1] and in_v[2])))
		#output = not ((in_v[0] and in_v[1]) or  in_v[2])
		#output = (in_v[0] and in_v[1]) or  in_v[2]
		if (output == True):
			return 1
		else:
			return 0
		
	def show_error_table (self):

		for c in range ((self.inputs+1)*2):
			for r in range (self.rows):
				in_v = list(self.truth_matrix[r])
				if (c < self.inputs *2):
					if (c%2 == 0):
						in_v[int(c/2)] = 0
					else:
						in_v[int(c/2)] = 1
					self.error_matrix[r][c] = self.logic_function (in_v)
				else:
					if (c%2 == 0):
						self.error_matrix[r][c] = 0
					else:
						self.error_matrix[r][c] = 1
		
		print ("Error table")
		
		for c in range (ord('a'), ord('a') + self.inputs):
			print (chr(c), "\b0  ", end="")
			print (chr(c), "\b1  ", end="")
		# New line
		print ("y0  y1")
		
		for r in range (self.rows):
			for c in range ((self.inputs+1)*2):
				
				print(self.error_matrix[r][c], "  ", end="")
			print ("")
	
	def show_diff_table (self):
		
		for r in range (self.rows):
			for c in range ((self.inputs+1)*2):
				if self.logic_function(self.truth_matrix[r]) != self.error_matrix[r][c]:
					self.diff_matrix[r][c] = 1
				else:
					self.diff_matrix[r][c] = 0
		
		i = 0
		while i < (self.inputs*2)+2 :
			
			self.error_sum = [0 for i in range(self.rows)]
			
			for r in range (self.rows):
				if not self.covered_rows[r]:
					for c in range ((self.inputs+1)*2):
						if self.diff_matrix[r][c] == 1:
							if not (c in self.covered_inputs):
								self.error_sum[r] += 1
				else:
					self.error_sum[r] = 0

			row_index = self.error_sum.index(max (self.error_sum))

			for c in range ((self.inputs+1)*2):
				if self.diff_matrix[row_index][c] == 1:
					if not(c in self.covered_inputs):
						self.covered_rows[row_index].append(c)
						self.covered_inputs.append(c)
						i+=1
		
		print ("Diff table")
		for c in range (ord('a'), ord('a') + self.inputs):
			print (chr(c), "\b0  ", end="")
			print (chr(c), "\b1  ", end="")
		# New line
		print ("y0  y1")
		
		for r in range (self.rows):
			for c in range ((self.inputs+1)*2):
				print (self.diff_matrix[r][c], "  ", end="")
			print ("")
	
	def show_coverage_table (self):
		print ("Coverage table")
		
		for c in range (ord('a'), ord('a') + self.inputs):
			print (chr(c), "  ", end="")
		print ("y   Error")
		for r in range (self.rows):
			if self.covered_rows[r]:
				for c in range (self.inputs):
					print(self.truth_matrix[r][c], "  ", end="")

				print (self.logic_function(self.truth_matrix[r]),"  ", end="")
				for e in self.covered_rows[r]:
					if e > (self.inputs*2-1):
						print ("y", end="")
					else:
						print (chr(ord('a') + int(e/2)), end="")
					if e%2:
						print ("1 ",end="")
					else:
						print ("0 ",end="")
				print ("")
		
	def show_truth_table (self):
		
		print ("Truth table")
		
		for c in range (ord('a'), ord('a') + self.inputs):
			print (chr(c), "  ", end="")
		# New line
		print ("y")
		
		for r in range (self.rows):
			for c in range (self.inputs):
				print(self.truth_matrix[r][c], "  ", end="")

			print (self.logic_function(self.truth_matrix[r]))
		

if __name__ == '__main__':
	circuit = Circuit_Checker (3)
	circuit.show_truth_table ()
	circuit.show_error_table ()
	circuit.show_diff_table ()
	circuit.show_coverage_table ()
