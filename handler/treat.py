from __future__ import division

import os
import pandas as pd
import numpy as np

#data_dir = './unzipped'
data_dir = '.' # test

def read_data(file):
	with open(data_dir + '/' + file) as f:
		print('Read file: ' + file)
		data = pd.read_csv(f)
		data = data.drop(columns = ['stoptime', 'name_localizedValue0', 'usertype', 'birth year', 'gender'])

		data = data.drop(columns = ['start station name', 'end station name', 'bikeid'])

		data.insert(0, 'date', [t.split()[0] for t in data['starttime']])
		data.insert(1, 'start_time', [t.split()[1] for t in data['starttime']])
		data = data.drop(columns = ['starttime'])
		return data

def classify_by_day(all_data):
	# print all_data
	groups = all_data.groupby('date')
	# gprint(groups)
	return groups

def gprint(groups):
	for name, group in groups:
		print name
		print group

def dprint(udict, tdict):
	keys = []
	for key in udict:
		keys.append(key)
	print keys

	taverages = []
	tdeviates = []
	for key in keys:
		times = tdict[key]
		if len(times) == 1:
			taverages.append(times[0])
			tdeviates.append(float('inf'))
		else:
			mean = sum(times) / len(times)
			squares = [(t - mean) ** 2 for t in times]
			var = sum(squares) / (len(times) - 1)
			taverages.append(mean)
			tdeviates.append(np.sqrt(var))
	print taverages
	print tdeviates

	print '['
	for t in range(48):
		tdis = []
		for key in keys:
			tdis.append(udict[key][t])
		print tdis
	print ']'

def classify_by_start(day_data):
	# print day_data
	groups = day_data.groupby('start station id')
	# gprint(groups)
	return groups

def station_usage(station_data):
	# print station_data
	sindex = station_data.index.values[0]
	lati, longi = station_data['start station latitude'][sindex], station_data['start station longitude'][sindex]
	print [lati, longi]
	counts = [0 for _ in range(48)] # half hours a slice
	for time in station_data['start_time']:
		ho, mi, se = time.split(':')
		# print ho,mi,se
		# print(time_index(int(ho),int(mi),int(se)))
		counts[time_index(int(ho),int(mi))] += 1
	print counts

def time_index(ho, mi):
	offset = 0
	if mi >= 30:
		offset = 1
	return ho * 2 + offset

def bi_station_usage(station_data):
	usage_dict = {}
	tsage_dict = {}
	# print station_data
	sindex = station_data.index.values[0]
	# lati, longi = station_data['start station latitude'][sindex], station_data['start station longitude'][sindex]
	# print [lati, longi]
	for i in xrange(sindex, sindex + len(station_data['start_time'])):
		try:
			time, dest, trans = station_data['start_time'][i], int(station_data['end station id'][i]), int(station_data['tripduration'][i])
			ho, mi, se = time.split(':')
			if dest in usage_dict.keys():
				usage_dict[dest][time_index(int(ho),int(mi))] += 1
				tsage_dict[dest].append(trans)
			else:
				usage_dict[dest] = [0 for _ in range(48)]
				usage_dict[dest][time_index(int(ho),int(mi))] += 1
				tsage_dict[dest] = [trans]
		except:
			pass
	dprint(usage_dict, tsage_dict)

def main():
	data_files = [file for file in os.listdir(data_dir) if file.find('.csv') > 0]
	# print(data_files)

	for data in data_files:
		dgroups = classify_by_day(read_data(data))
		for day, group in dgroups:
			print day
			sgroups = classify_by_start(group)
			for station, sg in sgroups:
				print station
				station_usage(sg)
				bi_station_usage(sg)
				print "----------"
				# break
			print "--------------------"
			# break

if __name__ == '__main__':
	main()