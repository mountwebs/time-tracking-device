import math

points = [[3, 4, 5], [6, 3, 8], [20, 1, 2], [8, 10, 20]]
currentPoint = [8, 10, 2]


def dist_3d(a, b):
    ''' Finds distance between two 3d coordinates '''
    # Formula: sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    dist = 0
    for i in range(3):
        dist += (a[i] - b[i])**2
    return math.sqrt(dist)


def get_index_shortest_dist(set_point, points):
    ''' Returns index of shortest distance between points '''
    dists = []
    for point in points:
        dists.append(dist_3d(set_point, point))
    return dists.index(min(dists))


print(get_index_shortest_dist(currentPoint, points))
