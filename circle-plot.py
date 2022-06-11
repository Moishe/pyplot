import itertools
import matplotlib.pyplot as plt
import numpy as np
import svgwrite
from svgwrite import cm, mm

dimensions = [210, 297]

boundaries = [
    {
        'radius': 100,
        'frequency': 1,
        'start': 0,
        'resolution': 1024,
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
        'resolution': 512,
        'epicycle': {
            'radius': 3,
            'frequency': 12,
            'start': 0
        }
    },
    {
        'radius': 60,
        'frequency': 1,
        'start': 0,
        'resolution': 256,
        'epicycle': {
            'radius': 2,
            'frequency': 24,
            'start': 0
        }
    }
]

paths = {}

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
    return coords

def plot_shell_boundaries(ax):
    global boundaries
    for idx, descriptor in enumerate(boundaries):
        coords = plot_shell_boundary(ax, descriptor)
        paths["boundary-%d" % idx] = coords

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
    return coords

def plot_shell_interferences(ax):
    global boundaries
    a, b = itertools.tee(boundaries)
    next(b, None)
    pairs = zip(a, b)
    for idx, pair in enumerate(pairs):
        coords = plot_shell_interference(ax, pair[0], pair[1])
        paths["interference-%d" % idx] = coords

def make_svg_file(name, path):
    name = "output/%s.svg" % name
    dwg = svgwrite.Drawing(filename=name, debug=True, width='%dmm' % dimensions[0], height='%dmm' % dimensions[1])
    lines = dwg.add(dwg.g(id='lines', stroke='black', stroke_width='0.1'))

    translated_path = [(p[0] + dimensions[0] / 2, p[1] + dimensions[1] / 2) for p in path]
    translated_path.append(translated_path[0])

    a, b = itertools.tee(translated_path)
    next(b, None)
    pairs = zip(a, b)

    for pair in pairs:
        lines.add(dwg.line(start=(pair[0][0] * mm, pair[0][1] * mm),
                           end=(pair[1][0] * mm, pair[1][1] * mm)))

    dwg.save()

def plot():
    fig, ax = plt.subplots()
    ax.axis('off')
    plot_shell_boundaries(ax)
    plot_shell_interferences(ax)

    for name in paths:
        make_svg_file(name, paths[name])

    plt.show()

if __name__ == '__main__':
    plot()