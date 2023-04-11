import matplotlib.pyplot as plt
from statistics import mean
import sys
import numpy as np
import os.path
import os
import glob

def read_txt(txt):
	data = open(txt,'r')
	line = data.readline()

	number_of_videos = [float(line.split()[2].strip())]

	aed_list = [float(line.split()[5].strip())]
	points = []

	while line:
		line = data.readline()
		if not line:
			break
		data_per_line = line.split()
		video_no = float(data_per_line[2].strip())
		aed = float(data_per_line[5].strip())
		number_of_videos.append(video_no)
		aed_list.append(aed)
		points.append((video_no,aed))
	return [number_of_videos,aed_list]

def calculate_improvement(default_list,list_poisson):
	total_improved_videos = 0
	for i in range(len(default_list)):
		if list_poisson[i] <= default_list[i]:
			total_improved_videos+=1
	improvement = total_improved_videos/len(default_list)
	print(f"Improvement = {improvement}")
	print(f"{total_improved_videos} out of {len(default_list)}")

def calculate_improvement_SSIM(default_list,list_poisson):
	total_improved_videos = 0
	for i in range(len(default_list)):
		if list_poisson[i] >= default_list[i]:
			total_improved_videos+=1
	improvement = total_improved_videos/len(default_list)
	print(f"Improvement = {improvement}")
	print(f"{total_improved_videos} out of {len(default_list)}")


dirs = []

rootdir = 'C:/Users/Vasilis Stergiou/Desktop/Results post Poisson'
for it in os.scandir(rootdir):
    if it.is_dir():
    	for subdir in os.scandir(it.path):
    		if (subdir.is_dir()):
    			dirs.append(subdir.path)

rootdir_defaults = 'C:/Users/Vasilis Stergiou/Desktop/Results post Poisson/No_Poisson_No_Gauss'

default_dirs = []
default_data = []

for it in os.scandir(rootdir_defaults):
	if it.is_dir():
		for subdir in os.scandir(it.path):
			if not subdir.is_dir() and 'txt' in subdir.path:
				default_dirs.append(subdir.path)
				print(subdir.path)
				measurements = read_txt(subdir.path)
				default_data.append(measurements[1])

print(len(default_data))
print()
data_per_category = {}
data_per_category_plots = {}


labels = []

for d in dirs:

	stats = []

	for name in glob.glob(f'{d}/*.txt'):
		if 'stats' in name or 'No_Poisson_No_Gauss' in name or 'aed' in name or 'AED' in name:
			continue

		category = name.split('\\')[1]
		dataset = name.split('\\')[2]

		if f'{category}_{dataset}' not in data_per_category:
			data_per_category[f'{category}_{dataset}'] = []

		if f'{category}_{dataset}' not in data_per_category_plots:
			data_per_category_plots[f'{category}_{dataset}'] = []

		file = name.split('\\')[3].split('.')[0]
		measurements = read_txt(name)

		videos = measurements[0]
		measurement = measurements[1]
		#print(name)
		if f'{category}_{dataset}' not in labels:
			labels.append(f'{category}_{dataset}')

		data_per_category_plots[f'{category}_{dataset}'].append(measurement)

		if 'L1' in name:
			print(name)	
			print(np.median(np.array(measurement)))
			#print(np.median(np.array(measurement)))		
			data_per_category[f'{category}_{dataset}'].append(np.median(np.array(measurement)))
			data_per_category[f'{category}_{dataset}'].append(np.median(np.array(measurement)))
			continue
		data_per_category[f'{category}_{dataset}'].append(np.median(np.array(measurement)))

data_vectors = [[] for i in range(6)]

bars = ('AED\nbefore',
		'AED\nafter',
		'L1\nbefore',
		'L1\nafter',
		'SSIM\nbefore',
		'SSIM\nafter')

for k,v in data_per_category.items():
	if ('Poisson_Gauss' in k or 'Poisson_No_Gauss'):
		print(k)
		print(v)
	'''
	os.mkdir(f'{k}_plots')
	for i in range(1,len(v),2):
		vector = [v[i-1],v[i]]
		title = ' '.join(k.split('_'))
		bars_vector = [bars[i-1],bars[i]]
		bars_vector_title = ' '.join([bars[i-1].replace('\n',' '),bars[i].replace('\n',' ')])
		bars_vector_title = bars_vector_title.split(' ')[0]
		#print(bars_vector_title)
		y_pos = np.arange(len(vector))
		plt.figure()
		plt.title(title)
		plt.bar(y_pos,vector)
		plt.ylabel("Numerical Value")
		plt.xticks(y_pos, bars_vector)
		#plt.show()
		plt.savefig(f'{k}_plots/{title} {bars_vector_title}.png')
	'''