import math
import numpy as np
import sys

def make_tooth(pitch, depth):
    points = []
    indices = []
    extent = pitch/2
    chamfer = pitch/6
    slope = pitch/18

    for z in [0, depth]:
        points.append([-extent, -extent - chamfer, z])
        points.append([-extent, -extent, z])
        points.append([-extent + chamfer, -extent + chamfer, z])
        points.append([-extent + chamfer + slope, extent - chamfer * 2, z])
        points.append([-extent + chamfer * 2, extent - chamfer, z])
        points.append([0, extent - chamfer, z])
        points.append([chamfer - slope, extent - chamfer * 2, z])
        points.append([chamfer, -extent + chamfer, z])
        points.append([chamfer * 2, -extent, z])
        points.append([extent, -extent, z])
        points.append([extent, -extent - chamfer, z])

    off = 11
    for idx in range(1, 11):
        indices.append([idx + off, idx + 1 + off, idx + 1, idx])

    indices.append([22, 12, 1, 11])

    indices.append([1, 2, 10, 11])
    indices.append([2, 3, 8, 9])
    indices.append([3, 4, 7, 8])
    indices.append([4, 5, 6, 7])

    indices.append([22, 21, 13, 12])
    indices.append([20, 19, 14, 13])
    indices.append([19, 18, 15, 14])
    indices.append([18, 17, 16, 15])

    return points, indices



def make_taurus(radius1, radius2, grain, arc_degrees=360):
    points = []
    texcoords = []
    indices = []
    angle = math.pi * 2 / grain
   
    arc_steps = int(grain * arc_degrees/360)

    for index1 in range(arc_steps + 1):
        angle1 = index1 * angle
        matrix = np.array(
            [
                [math.cos(angle1), -math.sin(angle1), 0],
                [math.sin(angle1), math.cos(angle1), 0],
                [0, 0, 1],
            ]
        )
        for index2 in range(grain + 1):
            angle2 = index2 * angle
            
            init_pt = np.array(
                [
                    math.sin(angle2) * radius2 - radius1, 
                    0, 
                    -math.cos(angle2) * radius2 - radius1
                ]
            )
            
            fin_pt = np.matmul(matrix, init_pt)
            points.append(fin_pt)
            
            texcoords.append((index2/grain, index1/grain))
            this_index = len(points)
            ul_nabe = this_index - 1
            lr_nabe = this_index - (grain + 1)
            ll_nabe = lr_nabe - 1
            if index1 and index2:
                indices.append((ll_nabe, ul_nabe, this_index, lr_nabe))

    return points, indices, texcoords


def rotate(points, arc_degrees, axis_index):
    """
    rotate by some number of degrees around x, y, or z
    """
    deg_to_rad = math.pi / 180
    arc_rad = deg_to_rad * arc_degrees

    # z axis case
    matrix = np.array(
        [
            [math.cos(arc_rad), -math.sin(arc_rad), 0],
            [math.sin(arc_rad), math.cos(arc_rad), 0],
            [0, 0, 1],
        ]
    )
    if axis_index == 0:
        pass
    if axis_index == 1:
        pass

    new_points = []
    for point in points:
        new_points.append(np.matmul(matrix, point))
    
    return new_points


def translate(points, tx, ty, tz):
    """
    translate an object by xyz
    """
    for point in points:
        point[0] += tx
        point[1] += ty
        point[2] += tz

    return points

def scale(points, sx, sy, sz):
    """
    translate an object by xyz
    """
    for point in points:
        point[0] *= sx
        point[1] *= sy
        point[2] *= sz

    return points

def merge_geo(points1, indices1, texcoords1, points2, indices2, texcoords2):
    offset = len(points1)

    points1.extend(points2)
    texcoords1.extend(texcoords2)

    for face in indices2:
        indices1.append([i + offset for i in face]) 

    return points1, indices1, texcoords1


def make_ess(major, minor):
    points1, indices1, texcoords1 = make_taurus(
       major, minor, 64, 270 
    )
    points2, indices2, texcoords2 = make_taurus(
       major, minor, 64, 270 
    )
    points1 = rotate(points1, 90, 2)
    points2 = rotate(points2, -90, 2)

    points1 = translate(points1, 0, major, 0)
    points2 = translate(points2, 0, -major, 0)

    points1 = scale(points1, 1, 0.5, 1)
    points2 = scale(points2, 1, 0.5, 1)

    return merge_geo(points1, indices1, texcoords1, points2, indices2, texcoords2)

    
def make_gear(radius, pitch, depth):
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = make_tooth(pitch, depth)
        new_points = translate(new_points, 0, radius, 0)
        new_points = rotate(new_points, arc_per_tooth * tooth, 2)

        points, indices, _ = merge_geo(points, indices, [], new_points, new_indices, [])    

    return points, indices


def save_obj(fname, points, indices, texcoords=None):
    with open(fname, "w") as handle:
        for point in points:
            handle.write("v {0} {1} {2}\n".format(point[0], point[1], point[2]))
        
        if texcoords:
            for uv in texcoords:
                handle.write("vt {0} {1}\n".format(uv[0], uv[1]))

            for index in indices:
                handle.write("f {0}/{0} {1}/{1} {2}/{2} {3}/{3}\n".format(index[0], index[1], index[2], index[3]))
        else:
            for index in indices:
                handle.write("f {0} {1} {2} {3}\n".format(index[0], index[1], index[2], index[3]))


if __name__ == "__main__":

    # points, indices, texcoords = make_ess(20, 7)
    # save_obj(sys.argv[1], points, indices, texcoords) 

    points, indices = make_gear(10, 3, 10)
    save_obj(sys.argv[1], points, indices) 
