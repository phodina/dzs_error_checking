#!/usr/bin/python3

## \file dzs.py
## \brief Python module 
# Contains class for determining possible errors in electrical circuits

## \author Petr Hodina

# Add cmdline arguments -a (all) -t (truth table) -c (coverage table) ...
# Edit README
# Add License
# Add Parser (I'm not gonna do this)

## \brief Handles entire computation for given electrical circuit
class Circuit_Checker:

	## \brief Constructor
	# @param[in] inputs Number of inputs for electrical circuit
	def __init__ (self, inputs):
		
		## \brief Number of inputs
		self.inputs = inputs;
		## \brief Contains number of rows in matrices
		self.rows = int (2**self.inputs);
		
		# Initialize all matrices and vectors
		## \brief Matrix of all possible inputs and corresponding output
		self.truth_matrix = [[0 for i in range(self.inputs+1)] for i in range(self.rows)]
		## \brief Matrix containing output vectors for faulty inputs  
		self.error_matrix = [[0 for i in range((self.inputs+1)*2)] for i in range(self.rows)]
		## \brief Matrix containing differences between faulty and correct output
		self.diff_matrix = [[0 for i in range((self.inputs+1)*2)] for i in range(self.rows)]
		
		## \brief List of covered rows
		self.covered_rows = [[] for i in range(self.rows)]
		
		# Compute truth table
		self.compute_truth_table ()
		# Compute error table
		self.compute_error_table ()
		# Compute difference table
		self.compute_diff_table ()


	## \brief Logic function
	# Calculates the output of given electrical circuit
	# @param[in] in_v Vector of input values for calculation
	def logic_function (self, in_v):
		#output = (not ((in_v[0] and in_v[1] or (not (in_v[2] and in_v[3]))))) and in_v[3]
		#output = ((in_v[0] or in_v[1]) and (not(in_v[1] and in_v[2])))
		output = not ((in_v[0] and in_v[1]) or  in_v[2])
		#output = (in_v[0] and in_v[1]) or  in_v[2]
		if (output == True):
			return 1
		else:
			return 0

	## \brief Prints truth table
	def compute_truth_table (self):
		
		count = self.rows
		
		#Initialize the truth table
		for c in range (0, self.inputs):
			count = int (count/2)
			
			r = 0
			while r < self.rows:
				for i in range (0, count):
					self.truth_matrix[r][c] = 0
					r += 1
				for i in range (0, count):
					self.truth_matrix[r][c] = 1
					r += 1
		
		#Calculate output vector
		for r in range (0, self.rows):
			self.truth_matrix[r][self.inputs] = self.logic_function(self.truth_matrix[r]) 

	## \brief Computes error table
	def compute_error_table (self):

		for c in range ((self.inputs+1)*2):
			for r in range (self.rows):
				in_v = list(self.truth_matrix[r])
				# Compute output for each input equal to 0 and 1
				if (c < self.inputs *2):
					if (c%2 == 0):
						in_v[int(c/2)] = 0
					else:
						in_v[int(c/2)] = 1
					self.error_matrix[r][c] = self.logic_function (in_v)
				# Compute output for output equal to 0 and 1
				else:
					if (c%2 == 0):
						self.error_matrix[r][c] = 0
					else:
						self.error_matrix[r][c] = 1

	## \brief Computes difference table
	def compute_diff_table (self):
		# Find differeces between error table and correct output vector in truth table
		for r in range (self.rows):
			for c in range ((self.inputs+1)*2):
				if self.truth_matrix[r][self.inputs] != self.error_matrix[r][c]:
					self.diff_matrix[r][c] = 1
				else:
					self.diff_matrix[r][c] = 0
		
		error_sum = [0 for i in range(self.rows)]
		covered_inputs = []
		
		cols = 0
		# Check if inputs have errors
		for c in range ((self.inputs+1)*2):
			for r in range (self.rows):
				if self.diff_matrix[r][c] == 1:
					cols += 1
					break
			
		# Cycle through difference table until all inputs are covered
		i = 0	
		while i < cols:
		#while i < (self.inputs*2)+2 :
			# 
			error_sum = [0 for i in range(self.rows)]
			# Compute list of sums for each row
			for r in range (self.rows):
				# Compute only if row is not covered
				if not self.covered_rows[r]:
					for c in range ((self.inputs+1)*2):
						if self.diff_matrix[r][c] == 1:
							if not (c in covered_inputs):
								error_sum[r] += 1
				else:
					error_sum[r] = 0
			# Find the highest number of errors and return index of the row
			row_index = error_sum.index(max (error_sum))
			# Append covered inputs in covered row
			for c in range ((self.inputs+1)*2):
				if self.diff_matrix[row_index][c] == 1:
					if not(c in covered_inputs):
						self.covered_rows[row_index].append(c)
						covered_inputs.append(c)
						i+=1

	## \brief Prints truth table
	def show_truth_table (self):
		
		print ("Truth table")
		# Print table header
		for c in range (ord('a'), ord('a') + self.inputs):
			print (chr(c), "  ", end="")
		print ("y")
		# Print matrix values
		for r in range (self.rows):
			for c in range (self.inputs+1):
				print(self.truth_matrix[r][c], "  ", end="")
			print ("")

	## \brief Prints error table
	def show_error_table (self):
		print ("Error table")
		# Print table header
		for c in range (ord('a'), ord('a') + self.inputs):
			print (chr(c), "\b0  ", end="")
			print (chr(c), "\b1  ", end="")
		print ("y0  y1")
		# Print matrix values
		for r in range (self.rows):
			for c in range ((self.inputs+1)*2):
				
				print(self.error_matrix[r][c], "  ", end="")
			print ("")

	## \brief Prints difference table
	def show_diff_table (self):
		print ("Diff table")
		# Print table header
		for c in range (ord('a'), ord('a') + self.inputs):
			print (chr(c), "\b0  ", end="")
			print (chr(c), "\b1  ", end="")
		print ("y0  y1")
		# Print matrix values
		for r in range (self.rows):
			for c in range ((self.inputs+1)*2):
				print (self.diff_matrix[r][c], "  ", end="")
			print ("")

	## \brief Prints coverage table
	def show_coverage_table (self):
		print ("Coverage table")
		# Print table header
		for c in range (ord('a'), ord('a') + self.inputs):
			print (chr(c), "  ", end="")
		print ("y   Error")
		# Print matrix values
		for r in range (self.rows):
			# Print only rows that cover errors
			if self.covered_rows[r]:
				for c in range (self.inputs):
					print(self.truth_matrix[r][c], "  ", end="")
				# Print error names converted from list
				print (self.logic_function(self.truth_matrix[r]),"  ", end="")
				for e in self.covered_rows[r]:
					# Print output name
					if e > (self.inputs*2-1):
						print ("y", end="")
					# Print input name
					else:
						print (chr(ord('a') + int(e/2)), end="")
					if e%2:
						print ("1 ",end="")
					else:
						print ("0 ",end="")
				print ("")

if __name__ == '__main__':
	circuit = Circuit_Checker (5)
	circuit.show_truth_table ()
	circuit.show_error_table ()
	circuit.show_diff_table ()
	circuit.show_coverage_table ()
