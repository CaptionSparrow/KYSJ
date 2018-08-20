# https://blog.csdn.net/theonegis/article/details/51037850
# http://www.labri.fr/perso/nrougier/teaching/matplotlib/
# https://matplotlib.org/api/animation_api.html

''' This file is used to generate animation'''

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

SIZE_MIN = 20
SIZE_MAX = 20 ** 2
LINE_MIN = 0.2
LINE_MAX = 2.0
NS = 4

pos = np.random.uniform(0, 1, (NS, 2))
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
    global size, scat, line

    # New axis over the whole figure, no frame and a 1:1 aspect ratio
    ax = fig.add_axes([0, 0, 1, 1], frameon = False, aspect = 1)

    # Ring sizes
    size = np.linspace(SIZE_MIN, SIZE_MAX, NS)

    # Scatter plot
    scat = ax.scatter(pos[:,0], pos[:,1], s=size, facecolors=color)
    line = generate_lines(ax)

    # Ensure limits are [0,1] and remove ticks
    ax.set_xlim(0, 1), ax.set_xticks([])
    ax.set_ylim(0, 1), ax.set_yticks([])

def update(frame):
    global size
    # Each ring is made larger
    size += (SIZE_MAX - SIZE_MIN) / NS

    # line = ax.plot([0.5,0.8],[0.5,0.7], color ='red', linewidth=1.5, linestyle="-")
    # line.set_data([0.3,0.3],[0.5,0.8])
    # line.set_linewidth(LINE_MIN)

    # Reset specific ring
    # i = frame % NS
    # size[i] = SIZE_MIN
    if frame % 50 == 0:
        for i in range(NS):
            size[i] = SIZE_MIN

    # Update scatter object
    # scat.set_edgecolors(color)
    scat.set_sizes(size)
    scat.set_offsets(pos)

    # Return the modified object
    objects = tuple(line + [scat])
    return objects

def showAnimation():
    init()
    anim = animation.FuncAnimation(fig, update, interval = 50, blit = True, frames = 200)
    plt.show()

def main():
    showAnimation()

if __name__ == '__main__':
    main()