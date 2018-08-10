from __future__ import division

import numpy as np

def allprint(pos, peak, dvpeak, terminal, distributions):
	for key in pos:
		print key
		print pos[key]
		print peak[key]
		print [np.sqrt(var) for var in dvpeak[key]]
		for dest in terminal[key]:
			mean = terminal[key][dest][0] / terminal[key][dest][2]
			# (b-len(a)*mean**2) / (len(a)-1)
			if terminal[key][dest][2] == 1:
				var = float('inf')
			else:
				var = (terminal[key][dest][1] - terminal[key][dest][2] * mean**2) / (terminal[key][dest][2] - 1)
			terminal[key][dest] = [mean, np.sqrt(var)]
		print terminal[key]
		for distribution in distributions[key]:
			print distribution
		print '------------------------------'

def treatline(line):
	if line.startswith('Read') or len(line.split('-')) > 2:
		# print line
		return 0, None
	elif not line.startswith('[') and not line.startswith(']'):
		return 1, int(line)
	elif not line == '[' and not line == ']':
		resoto = eval(line.replace('inf', "float('inf')"))
		return 2, resoto
	elif line == '[':
		return 3, None
	elif line == ']':
		return 4, None
	else:
		return -1, None

def main():
	positions = {}        # station position
	peaks = {}            # average # of bikes from the station each time
	dvpeaks = {}          # deviate # of bikes from the station each time
	count = {}
	terminals = {}        # terminal station ids and their transport time
	distributions = {}    # distribution onver terminals at each time

	with open('eachDay.txt') as f:
		for line in f.readlines():
			handle, infos = treatline(line.replace('\n', ''))
			# print handle
			if handle == 0:
				continue
			elif handle == 1:
				key = infos
				flag = 0
			elif handle == 2 and flag == 0:
				positions[key] = infos
				flag = 1
			elif handle == 2 and flag == 1:
				if key not in peaks:
					peaks[key] = [n for n in infos]
					dvpeaks[key] = [n ** 2 for n in infos]
					count[key] = 1
				else:
					peaks[key] = [peaks[key][i] + infos[i] for i in range(len(infos))]
					dvpeaks[key] = [dvpeaks[key][i] + infos[i]**2 for i in range(len(infos))]
					count[key] += 1
				flag = 2
			elif handle == 2 and flag == 2:
				tempterms = [dest for dest in infos]
				# print tempterms
				flag = 3
			elif handle == 2 and flag == 3:
				if key not in terminals:
					terminals[key] = {}
				# print tempterms
				for i in xrange(len(tempterms)):
					if tempterms[i] not in terminals[key]:
						terminals[key][tempterms[i]] = [infos[i], infos[i]**2, 1]
					else:
						terminals[key][tempterms[i]][0] += infos[i]
						terminals[key][tempterms[i]][1] += infos[i] ** 2
						terminals[key][tempterms[i]][2] += 1
				flag = 4
			elif handle == 2 and flag == 4:
				flag = 5
			elif handle == 3:
				if key not in distributions:
					distributions[key] = [{} for _ in xrange(48)]
				tflag = 0
			elif handle == 2 and flag == 5:
				for i in xrange(len(tempterms)):
					dest = tempterms[i]
					if dest not in distributions[key][tflag]:
						distributions[key][tflag][dest] = infos[i]
					else:
						distributions[key][tflag][dest] += infos[i]
				distributions[key][tflag]
				tflag += 1
			elif handle == 4:
				flag = 0
				tflag = 0
				continue
			elif handle == -1:
				# continue
				print line.replace('\n', '')
				break

	for key in peaks:
		peaks[key] = [n / count[key] for n in peaks[key]]
		# (b-len(a)*mean**2) / (len(a)-1)
		if count[key] == 1:
			dvpeaks[key] = [float('inf') for _ in dvpeaks[key]]
		else:
			dvpeaks[key] = [(dvpeaks[key][i] - count[key] * peaks[key][i]**2) / (count[key] - 1) for i in range(len(dvpeaks[key]))]
	allprint(positions, peaks, dvpeaks, terminals, distributions)

if __name__ == '__main__':
	main()