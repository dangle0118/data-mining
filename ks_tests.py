import os
import math
from decimal import *
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
directory = 'result'
directory2 = 'result_tf_idf_mit'
#dir_result = 'compare_result_mit'  # result folder for ks_test
dir_result = 'sample'		# result folder for x_test
bound = 0.4
poly_degree = 3

def ks_test(data1, data2, addr):
	

	temp= stats.ks_2samp(data1, data2)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(data1,'b+', label = 'data1')
	ax.plot(data2,'k-', label = 'data2')
	#plt.plot(data1, data2)
	plt.savefig(dir_result + '/' + addr+'.png')
	plt.close()
	return temp


def run_ks_test(input1, input2, name1, name2):
	data1 = []
	data2 = []
	f = open(input1, 'r')
	a = f.readline()
	count = 0
	for line in f:
		#if count <390:
			data1.append(float(line.split('\t')[1]))
		#	count += 1
	f.close()
	f = open(input2, 'r')
	count = 0
	a = f.readline()
	for line in f:
		#if count < 390:
			data2.append(float(line.split('\t')[1]))
		#	count += 1
	f.close()

	#addr = input1+'_'+ name
	addr = name1 + '/' + name1+'_'+ name2
	
	temp = ks_test(data1, data2, addr)
	#temp = chi_square_test(data1, data2, addr)
	#temp = correl_test(data1, data2, addr)
	
	print temp

def linear_regress(data1, data2, addr):
	fig = plt.figure()
	ax = fig.add_subplot(111)

	xi = np.arange(0, len(data2))
	slope, intercept, r_value, p_value, std_err = stats.linregress(xi, data2)
	line = slope * xi + intercept
	ax.plot(line, 'r-', label = 'regress data2')

	xi = np.arange(0, len(data1))
	slope, intercept, r_value, p_value, std_err = stats.linregress(xi, data1)
	line = slope * xi + intercept

	ax.plot(line, 'b-', label = 'regress data1')

	plt.legend(loc = 'best')
	plt.savefig(dir_result + '/' + addr+'.png')
	plt.close()
	

def poly_regress(data1, data2, addr):
	fig = plt.figure()
	ax = fig.add_subplot(111)	

	xi = np.arange(0, len(data1))
	z = np.polyfit(xi, np.array(data1), poly_degree)
	func_data1 = np.poly1d(z)
	ax.plot(func_data1(xi),'b-', label = 'data1')
	#ax.plot(data1, 'ro', label = 'data1')

	xi = np.arange(0, len(data2))
	z = np.polyfit(xi, np.array(data2), poly_degree)
	func_data2 = np.poly1d(z)
	ax.plot(func_data2(xi),'r-', label = 'data2')
	#ax.plot(data2, 'r+', label = 'data2')
	

	plt.legend(loc = 'best')
	plt.savefig(dir_result + '/' + addr+'.png')
	plt.close()

	return func_data1, func_data2
	

def chi_square_test(data1, data2, addr):
	
	xi = np.arange(0, len(data1))
	xj = np.arange(0, len(data2))
	
	#temp= stats.chisquare(np.array(data1), np.array(data2))
	
	#linear_regress(data1, data2, addr)

	func_data1, func_data2 = poly_regress(data1, data2, addr)

	return stats.ks_2samp(func_data1(xi), func_data2(xj))
	

def correl_test(data1, data2, addr):
	

	temp= stats.pearsonr(np.array(data1), np.array(data2))

	fig = plt.figure()
	ax = fig.add_subplot(111)
	#ax.plot(data1,'r', label = 'data1')
	#ax.plot(data2,'b', label = 'data2')
	plt.plot(data1, data2, 'r,')
	plt.savefig(dir_result + '/' + addr+'.png')
	plt.close()
	return temp

def run_chi_square_test(input1, input2, name1, name2, g):
	data1 = []
	data2 = []
	temp = {}
	temp1 = []
	f = open(input2, 'r')
	a = f.readline()
	for line in f:
		 temp[line.split('\t')[0]] = float(line.split('\t')[1])
	f.close()
	f = open(input1, 'r')
	a = f.readline()
	for line in f:
		word = line.split('\t')[0]
		temp1.append(word)
		if word in temp:
			data1.append(float(line.split('\t')[1]))
			data2.append(temp[word])
	

	#for word in temp:
	#	if word not in temp1:
	#		data1.append(float(bound))
	#		data2.append(float(bound))
	#for word in temp1:
	#	if not temp.has_key(word):
	#		data1.append(float(bound))
	#		data2.append(float(bound))
	f.close()
	
	addr = name1 + '/' + name1+'_'+ name2
	d_value, p_value = chi_square_test(data1, data2, addr)
	#result = correl_test(data1, data2, addr)
	g.write('{0} \t {1} \t {2}\n'.format(name2, d_value, p_value))


def main():
	

	for roots, dirs, files in os.walk(directory):
		for file in files:
			input1 = os.path.join(directory, file)

			if not os.path.exists(os.path.join(dir_result, file)):
				os.makedirs(os.path.join(dir_result, file))
			addr = os.path.join(dir_result, file)
			addr = os.path.join(addr, file)
			g = open(addr, 'w')
			for roots2, dirs2, files2 in os.walk(directory):
				for file2 in files2:
					if file != file2:
						input2 = os.path.join(directory, file2)
						print file, file2
						run_chi_square_test(input2, input1, file, file2, g)
						#run_ks_test(input2, input1, file, file2)
			g.close()



if __name__ == "__main__":
	main()





                                   



