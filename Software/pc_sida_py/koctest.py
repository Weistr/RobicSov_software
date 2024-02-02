import kociemba
import time
import serial
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

import skimage
from skimage import draw
from skimage import morphology
from skimage import data

from copy import deepcopy
from copy import deepcopy
import heapq

motionResult = kociemba.solve('BFUUUUDDFLFFLRRLDDRBUFFULDUDRFUDLDRRRBBLLLFRBRDUBBBFFL')
print("**************Kociemba动作**************")
print(motionResult)