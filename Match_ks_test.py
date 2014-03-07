import os

ks_test_directory = 'sample'
upper_bound = 0.25


class ks_data:
	def __init__(self):
		self.data = {}

	def add_data(self, user, prob):
		self.data[user] = float(prob)

class ks_list:
	
	path = '/home/ubuntu/data_mining/sample_matching/'
	def __init__(self):
		self.list = {}
		self.match_list = {}

	def add(self, user, data):
		self.list[user] = data

	def find_match_result(self):
		for user in self.list:
			path = os.path.join(self.path, user)
			path = os.path.join(path, user)
			f = open(path, 'r')
			data = self.list[user].data
			for line in f:
				match_user = line.split('\t')[0]
				if data.has_key(match_user):
					if self.match_list.has_key(user):
						self.match_list[user][match_user] = line.split('\t')[3]
					else:
						self.match_list[user] = {match_user:line.split('\t')[3]}
			f.close()

	def find_positive_matching(self):
		for user in self.match_list:
			temp = self.match_list[user]
			for match_user in temp:
				if temp[match_user] > 














def exec_ks_data(target_path):
	try:
		ks_user = ks_data()
		f = open(target_path, 'r')
		for line in f:
			temp = line.split('\t')
			if (float(temp[1]) <= upper_bound):
				ks_user.add_data(temp[0], temp[1])				
		f.close()
		return ks_user
	except IOError:
		print "error"



def main():
	
	ks_result = ks_list()
	for roots, dirs, files in os.walk(ks_test_directory):
		for file in files:
			if not '.png' in file:
				target_path = os.path.join(ks_test_directory, file)
				target_path = os.path.join(target_path, file)
				print "reading file {}".format(file)				
				temp = exec_ks_data(target_path)
				ks_result.add(file, temp)
	ks_result.find_match_result()



if __name__ == "__main__":
	main()