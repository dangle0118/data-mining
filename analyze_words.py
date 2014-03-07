#compute tf-idf first



import os
import re
import operator
import math
from decimal import *
import matplotlib.pyplot as plt
from ks_tests import *

#directory = 'mit'
directory = 'enron_mail_20110402/maildir'
dir_result = 'result_duplicated_prob'
#dir_result = 'result_tf_idf_mit'
stop_file = 'stop_word'
global tf_idf 
tf_idf = {}
bound = 6






def get_stop_word():
	f = open(stop_file, 'r')
	temp = f.read().split('\n')
	return temp
	

def process_mess(mess):
	temp = mess.replace('\n',' ')
	temp = temp.replace('\r', ' ')
	temp = temp.split(' ')
	return temp
	
def check_word(pattern, word, stop_list):	
	temp = re.match(pattern, word)
	if ( temp != None ) and (temp.group() == word) and ( word not in stop_list) :

		
		return True
	else:
		
		return False


def sum_word(word_list):
	temp = 0
	for i in word_list:
		if word_list[i] > bound:
			temp = temp + word_list[i]
	return temp

def prob_word(total, word_list):
	rank = []
	temp = []
	count = 0

	for i in range(len(word_list) -1, len(word_list) - bound, -1):
		
		temp.append((math.log((Decimal(word_list[i][1]) / Decimal(total)) ) * 100))
		count +=1
		rank.append(math.log(count))
	
	#print temp
	return temp, rank


def plot_zipf_law(list, rank, addr):
	plt.plot(list, rank, 'ro')
	plt.savefig(addr+'.png')
	plt.close()



def tf(list, max):

	temp = {}
	for i in list:
		temp[i] = Decimal(list[i]) / Decimal(max)
	return temp

def idf(word, N):
	return math.log(Decimal(N) / Decimal(word))


def find_max(list):
	temp = 0
	word = ''
	for i in list :
		if list[i] > temp:
			temp = list[i]
			word = list[i]
	#print word
	#print temp
	return temp

def cal_idf_list(idf_list, list):
	temp = {}
	for i in range(len(list)):
		if idf_list.has_key(list[i][0]):
			idf_list[list[i][0]] = idf_list[list[i][0]] + 1
		else:
			idf_list[list[i][0]] = 1
		

def compute_tf_idf(tf_list, idf_list, N):
	#for document in tf_list:
	#	temp = tf_list[document]
		#addr_result = os.path.join(dir_tf, document)
		#print addr_result
		#f = open(addr_result, 'w')

	for word in tf_list:

		idf_No = math.log(Decimal(N) / Decimal(idf_list[word]), 2)

		if not tf_idf.has_key(word):
			tf_idf[word] = []
		tf_idf[word].append(Decimal(tf_list[word]) * Decimal(idf_No))
		
		#f.write("{0} \t {1} \ {2}\n".format(word, Decimal(result), temp[word]))
		#f.close()
		
		#f = open('idf_list','w')
		#for word in idf_list:
		#if idf_No > 1:
		#	print ("{0} \t {1}\n".format(word, idf_No))
		#f.close()



def delete_bottom_list(list):
	i = 0
	while (list[i][1] < 6):
		del(list[i])
	print list[1]
	
	



def main():
	user = ""
	idf_list = {}	
	tf_list = {}
	file_count = 0
	words_list = {}
	
	stop_list = []
	stop_list = get_stop_word()
	#print stop_list
	
	getcontext().prec = 3
	pattern = re.compile('[a-zA-Z0-9]+', re.IGNORECASE)
	for root, dirs, files in os.walk(directory):
		print root
		if dirs == []:
			
			for file in files:

				file_count = file_count + 1
				
				addr = os.path.join(root, file)
				
				f = open(addr, 'r')
				mess = f.read()
				temp1 = {}
				mess = process_mess(mess)
				
				for raw_word in mess:
					word = raw_word.lower()
					if check_word(pattern, word, stop_list):
				#		if not (temp1.has_key(word)):
				#			temp1[word] = 1

						if temp1.has_key(word):
							temp1[word] += 1
						else:
							temp1[word] = 1									 
				f.close()

				for word in temp1:
					if idf_list.has_key(word):
						idf_list[word] += 1
					else:
						idf_list[word] = 1						
				
				max_word = find_max(temp1)
				tf_list[addr]  = tf(temp1, max_word)
				temp1.clear()



		else:
			temp = root.split('/')		
			print temp	

			if (len(temp) == 3):
				print "{0}\t{1}".format(temp[2],user)
				
				if user == "":
					user = temp[2]
					continue
				if (temp[2] != user):
					
					#addr_result = os.path.join(dir_result, user)
					addr_result = os.path.join(dir_result, user)
					print addr_result
					g = open(addr_result, 'w')
					
					result = {}
					#for document in tf_list:						
					#	compute_tf_idf(tf_list[document], idf_list, file_count)
					#for word in tf_idf:
					#	a = max(tf_idf[word])
					#	if ( a <= 4) and ( a >= 0.5):
					#		result[word] = max(tf_idf[word])
					total = sum_word(idf_list)

					total_word = 0 
					for word in idf_list:
						if idf_list[word] > bound:
							result[word] = (Decimal(idf_list[word]) / Decimal(file_count))
							

					temp_sorted_words_list = sorted(result.iteritems(), key = operator.itemgetter(1))	
					
					sorted_words_list = []
					for i in range(len(temp_sorted_words_list)):
						

						sorted_words_list.append(temp_sorted_words_list[i])
						total_word += 1

				# create list with only 1 word for each probability						
						#if (temp_sorted_words_list[i][1] == temp_sorted_words_list[i-1][1]) and ( i > 0 ):
						#	continue
						#else:
						#	sorted_words_list.append(temp_sorted_words_list[i])
						#	total_word += 1

					

					#sorted_words_list = sorted(words_list.iteritems(), key = operator.itemgetter(1))
					#delete_bottom_list(sorted_words_list)

					#max_word = find_max(sorted_words_list)
					#tf_list[user]  = tf(sorted_words_list, max_word)
					#cal_idf_list(idf_list, sorted_words_list)
					
					

				#	compute_tf_idf(tf_list, idf_list, file_count)

					


					#total = sum_word(sorted_words_list)
					#prob_list, rank_list = prob_word(total, sorted_words_list)

					#plot_zipf_law(prob_list, rank_list, addr_result)


					#for i in range(len(prob_list)):
					#	g.write("{0} \n".format(prob_list[i]))
					g.write("{0}\t{1}\t{2}\n".format(total, file_count, total_word))
					for i in range(len(sorted_words_list)-1 , 0, -1):
						
						g.write("{0} \t {1}\n".format(sorted_words_list[i][0], sorted_words_list[i][1]))
						
					g.close()

					tf_idf.clear()
					tf_list.clear()
					idf_list.clear()
					file_count = 0
					result.clear()
					user = temp[2];
					#words_list.clear()

	#compute_tf_idf(tf_list, idf_list, file_count)

if __name__ == "__main__":
	main()














	
