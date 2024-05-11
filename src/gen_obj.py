import math
import numpy as np
import sys

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

if __name__ == "__main__":
    points, indices, texcoords = make_taurus(
        int(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
        int(sys.argv[5])
    )
   
    with open(sys.argv[1], "w") as handle:
        for point in points:
            handle.write("v {0} {1} {2}\n".format(point[0], point[1], point[2]))
       
        for uv in texcoords:
            handle.write("vt {0} {1}\n".format(uv[0], uv[1]))

        for index in indices:
            handle.write("f {0}/{0} {1}/{1} {2}/{2} {3}/{3}\n".format(index[0], index[1], index[2], index[3]))
