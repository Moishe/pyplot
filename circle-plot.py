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

def get_shell_coords(descriptor, radians):
    t = radians * descriptor['frequency'] + descriptor['start']
    xy = np.array([np.cos(t), np.sin(t)]) * descriptor['radius']

    if 'epicycle' in descriptor:
        return xy + get_shell_coords(descriptor['epicycle'], radians)

    return xy

def plot_shell_boundary(descriptor, ax):
    coords = []
    for i in range(0, descriptor['resolution']):
        r = float(i) / (float(descriptor['resolution'] - 1)) * (np.pi * 2) * descriptor['frequency']
        xy = get_shell_coords(descriptor, r)
        coords.append(xy)
    x, y = zip(*coords)
    ax.plot(x, y)

def plot_shell_interference(idx):
    if idx == 0:
        return # no interference at outermost layer

def plot():
    fig, ax = plt.subplots()
    ax.axis('off')
    for descriptor in boundaries:
        plot_shell_boundary(descriptor, ax)
    plt.show()

if __name__ == '__main__':
    plot()