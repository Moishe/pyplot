import itertools
import matplotlib.pyplot as plt
import numpy as np

dimensions = [210, 297]

boundaries = [
    {
        'radius': 100,
        'frequency': 1,
        'start': 0,
        'resolution': 256,
        'epicycle': {
            'radius': 6,
            'frequency': -16,
            'start': 0,
        }
    },
    {
        'radius': 80,
        'frequency': 1,
        'start': 0,
        'resolution': 256,
    }
]

def get_r(step, resolution):
    return float(step) / float(resolution) * (np.pi * 2)

def get_shell_coords(descriptor, radians):
    t = radians * descriptor['frequency'] + descriptor['start']
    xy = np.array([np.cos(t), np.sin(t)]) * descriptor['radius']

    if 'epicycle' in descriptor:
        return xy + get_shell_coords(descriptor['epicycle'], radians)

    return xy

def plot_shell_boundary(ax, descriptor):
    coords = []
    for i in range(0, descriptor['resolution']):
        r = get_r(i, descriptor['resolution'])
        xy = get_shell_coords(descriptor, r)
        coords.append(xy)
    x, y = zip(*coords)
    ax.plot(x, y)

def plot_shell_boundaries(ax):
    global boundaries
    for descriptor in boundaries:
        plot_shell_boundary(ax, descriptor)

def plot_shell_interference(ax, outer, inner):
    coords = []
    resolution = np.max([outer['resolution'], inner['resolution']])
    for i in range(0, resolution):
        r = get_r(i, resolution)
        for descriptor in [outer, inner]:
            xy = get_shell_coords(descriptor, r)
            coords.append(xy)
    x, y = zip(*coords)
    ax.plot(x, y)

def plot_shell_interferences(ax):
    global boundaries
    a, b = itertools.tee(boundaries)
    next(b, None)
    pairs = zip(a, b)
    for pair in pairs:
        plot_shell_interference(ax, pair[0], pair[1])

def plot():
    fig, ax = plt.subplots()
    ax.axis('off')
    plot_shell_boundaries(ax)
    plot_shell_interferences(ax)
    plt.show()

if __name__ == '__main__':
    plot()