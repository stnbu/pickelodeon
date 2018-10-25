
import math
import numpy as np

def to_rad(deg):
    deg = deg % 360
    coef = 2 * math.pi / 360
    return coef * deg

#https://stackoverflow.com/a/6802723/10291833
def rotation_matrix():
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = [-9, 1, 1.4]
    theta = math.pi / 4.0
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.3)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


#import collections
#Point = collections.namedtuple('Point', 'x y z')

m = rotation_matrix()
def fix_facet(f):
    normal = tuple(np.dot(m, f.normal))
    vertices = []
    for i in f.vertices:
        vertices.append(np.dot(m, i))
    facet = stl.Facet(normal, vertices)
    return facet


if __name__ == '__main__':

    import stl
    import os

    i = 0
    while i < 2 * math.pi:

        i += 0.1
        frame = '%02f' % (i,)

        door = stl.read_binary_file(open('/home/mburr/tmp/pov/door.stl.ORIG', 'rb'))
        facets = []
        for facet in door.facets:
            facet = fix_facet(facet)
            facets.append(facet)
        new_door = stl.Solid('new_door_01', facets)
        stl.binary.write(new_door, open('door.%s.stl' % frame, 'wb'))
        os.system('stl2pov door.%s.stl' % frame)
        content = open('door.pov.template').read() % {'name': 'foo'}
        open('door.%s.pov' % frame, 'wb').write(content)
        break
