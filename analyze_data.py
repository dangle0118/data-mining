import os
import math
import operator
import matplotlib.pyplot as plt
import numpy as np

# we ignore words that appear too little,  < 10

directory = 'result_duplicated_prob'
dir_result = 'sample_matching'


class Data_store:
	def __init__(self,word, value):
		self.value = value
		self.list = [word]
		self.bound = 0.01

	def check_prob(self, value):
		if (self.value - value <= self.bound):
			return True
		return False

	def check_word(self, word):
		if word in self.list:
			return True
		return False

	def add(self, word):
		self.list.append(word)



class list_data:
	def __init__(self):
		self.list = []

	def check_prob(self, value):
		count = 0
		for data in self.list:
			if data.check_prob(value):
				return count
			count += 1
		return -1

	def add_existed_data(self, position, word):
		self.list[position].add(word)

	def add_new_data(self, word, value):
		self.list.append(Data_store(word, value))

	def get_length(self):
		return len(self.list)


def run_matching(target_list, compared_list):
	count = 0
	#for compared in compared_list.list:
	#	result = target_list.check_prob(compared.value)
	#	if result != -1:
	#		for word in compared.list:
	#			if target_list.list[result].check_word(word):
	#				count += 1
	#				break
	
	for word in compared_list:
		result = target_list.check_prob(compared_list[word])
		if result != -1:
			if target_list.list[result].check_word(word):
				count += 1


	return count

def exec_input(file):
	f = open(file, 'r')
	list_input = list_data()
	count = 0
	temp = f.readline()
	for line in f:
		word = line.split('\t')[0] 
		value = float(line.split('\t')[1])
		if count != 0:
			temp = list_input.check_prob(value)
			if (temp == -1):
				list_input.add_new_data(word, value)
			else:
				list_input.add_existed_data(temp, word)
				#count += 1
		else:
			count += 1
			list_input.add_new_data(word, value)
	return list_input

def get_compared_input(file):
	f = open(file, 'r')
	temp = f.readline()
	list = {}
	count = 0
	for line in f:
		count += 1
		word = line.split('\t')[0] 
		value = float(line.split('\t')[1])
		list[word] = value
	return list, count
		


def main():
	for roots, dirs, files in os.walk(directory):
		for file in files:
			target_path = os.path.join(directory, file)

			if not os.path.exists(os.path.join(dir_result, file)):
				os.makedirs(os.path.join(dir_result, file))
			addr = os.path.join(dir_result, file)
			addr = os.path.join(addr, file)
			g = open(addr, 'w')
		# get input from the target file	
			target_list = exec_input(target_path)
			for roots2, dirs2, files2 in os.walk(directory):
				for file2 in files2:
					if file != file2:
						compared_path = os.path.join(directory, file2)
						print file, file2
		#get input from the compared file
						#compared_list = exec_input(compared_path)
						compared_list, numb_compared = get_compared_input(compared_path)
						result = run_matching(target_list, compared_list)
						g.write('{0} \t {1} \t {2} \t {3}\n'.format(
													file2, 
													result, 
													numb_compared,													
													float(float(result) / float(numb_compared)))
													)											 

			g.close()



if __name__ == "__main__":
	main()


#	f = open('result_first_list.txt', 'w')

#	for s in first_list:
		
#		first_list[s] = (min(first_list[s]))
#	sorted_words_list = sorted(first_list.iteritems(), key = operator.itemgetter(1))

#	for i in range(len(sorted_words_list) - 1, 0, -1):
#		f.write("{0} \t {1} \n".format(sorted_words_list[i][0], sorted_words_list[i][1]))
	

#	f.close()

#	f = open('result_sec_list.txt', 'w')

#	for s in sec_list:
#		sec_list[s] = (min(sec_list[s]))
#	sorted_words_list = sorted(sec_list.iteritems(), key = operator.itemgetter(1))

#	for i in range(len(sorted_words_list) - 1, 0, -1):
#		f.write("{0} \t {1}\n".format(sorted_words_list[i][0], sorted_words_list[i][1]))
	
#	f.close()


