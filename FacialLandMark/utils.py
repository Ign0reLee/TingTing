import cv2

import numpy as np
from collections import OrderedDict

def rect_to_bb(rect):
    
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    
    return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
    
    coords = np.zeros((shape.num_parts, 2), dtype=dtype)
    
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    
    return coords