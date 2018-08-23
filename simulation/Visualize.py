''' This file is used to generate animation'''

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

SIZE_MIN = 50
SIZE_MAX = 500
SIZE_INI = 1000
LINE_MIN = 0.2 # 0
LINE_MAX = 2.0 # 10
NS = 4

INIT = 500
DATAS = []

# pos = np.random.uniform(0, 1, (NS, 2))
pos = np.array([[0.76,0.66], [0.23,0.48], [0.31,0.12], [0.46,0.83]])
color = np.ones((NS, 4)) * (0, 0, 0, 1)
color[:,0] = np.linspace(0, 0.5, NS)
color[:,1] = np.linspace(0, 0.8, NS)
color[:,2] = np.linspace(0, 1, NS)

fig = plt.figure(num = "Bike Simulation", figsize=(6,6), facecolor='white')

def generate_lines(ax):
    lines = []
    for s in range(NS):
        for i in range(NS):
            line, = ax.plot([pos[s,0],pos[i,0]],[pos[s,1],pos[i,1]], color ='blue', linewidth=LINE_MIN, linestyle="-")
            lines.append(line)

    return lines

def init():
    global size, scat, line, time, day

    # print(pos)

    # New axis over the whole figure, no frame and a 1:1 aspect ratio
    ax = fig.add_axes([0, 0, 1, 1], frameon = False, aspect = 1)

    # Ring sizes
    size = np.linspace(SIZE_INI, SIZE_INI, NS)

    # Scatter plot
    scat = ax.scatter(pos[:,0], pos[:,1], s=size, facecolors=color)
    line = generate_lines(ax)

    # Ensure limits are [0,1] and remove ticks
    ax.set_xlim(0, 1), ax.set_xticks([])
    ax.set_ylim(0, 1), ax.set_yticks([])

    # Set time
    day = 0
    time = 0

def update(frame):
    global size, time, day
    # Each ring is made larger
    # size += (SIZE_MAX - SIZE_MIN) / NS

    # Set line widths
    # for i in range(NS):
    #     for j in range(NS):
    line[1].set_linewidth(10)

    # Reset specific ring
    for i in range(NS):
        o_size = size[i] #/ 2 #(size[i] - 50) / 4.5
        n_size = o_size - sum([DATAS[day][time][i][j] for j in range(NS)]) \
                + sum([DATAS[day][time][j][i] for j in range(NS)])
        if n_size < 0:
            print(n_size)
        size[i] = n_size #* 2 # * 4.5 + 50

    # Update scatter object
    # scat.set_edgecolors(color)
    scat.set_sizes(size)
    scat.set_offsets(pos)

    time += 1
    if time >= 48:
        time = 0
        day += 1
    if day >= 10:
        day = 0
        size = np.linspace(SIZE_INI, SIZE_INI, NS)

    # Return the modified object
    objects = tuple(line + [scat])
    return objects

def showAnimation():
    init()
    anim = animation.FuncAnimation(fig, update, interval = 50, blit = True, frames = 200)
    plt.show()

def get_transdata():
    with open('data/transports') as f:
        for line in f.readlines():
            data = eval(line.replace('\n', ''))
            DATAS.append(data)

def main():
    get_transdata()
    showAnimation()

if __name__ == '__main__':
    main()