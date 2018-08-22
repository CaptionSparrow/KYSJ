# FILE = 'stations.txt'
FILE = 'tiny_stat.txt'

def line_handler(line):
	if line.startswith('-'):
		return 0, None
	elif not line.startswith('[') and not line.startswith('{'):
		return 1, int(line)
	elif line.startswith('[') or line.startswith('{'):
		resoto = eval(line.replace('inf', "float('inf')"))
		return 2, resoto
	else:
		return -1, None

def read_stations():
	positions = {}
	outBikes = {}
	outdeviates = {}
	transitions = {}
	distributions = {}

	with open(FILE) as f:
		for line in f.readlines():
			line = line.replace('\n', '')
			handle, infos = line_handler(line)
			# print(handle)
			if handle == 0:
				flag = 0
				tflag = 0
				continue
			elif handle == 1:
				# print(infos)
				key = infos
				flag = 0
				tflag = 0
			elif handle == 2 and flag == 0:
				positions[key] = infos
				flag = 1
			elif handle == 2 and flag == 1:
				outBikes[key] = infos
				flag = 2
			elif handle == 2 and flag == 2:
				outdeviates[key] = infos
				flag = 3
				# if key == 2023:
				# 	print(infos)
				# 	print(outdeviates[key])
				# 	break
			elif handle == 2 and flag == 3:
				transitions[key] = infos
				flag = 4
				tflag = 0
				distributions[key] = [{} for _ in range(48)]
			elif handle == 2 and flag == 4:
				distributions[key][tflag] = infos
				tflag += 1
			elif handle == -1:
				print(line)
				break

	return positions, outBikes, outdeviates, transitions, distributions

def main():
	positions, outBikes, outdeviates, transitions, distributions = read_stations()
	print(positions)
	print(outBikes)
	print(outdeviates)
	print(transitions)
	print(distributions)

if __name__ == '__main__':
	main()