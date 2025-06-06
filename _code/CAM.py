import bpy
import math
import mathutils
import numpy as np
import json
from pathlib import Path
scene = bpy.context.scene
cam = scene.objects['Camera']

#"stump":     {"position": (-1, 1.1, -2), "quaternion": (-0.4226, 0.0, 0.0, 0.9063), "scale": 3},

cam.rotation_mode = 'QUATERNION'

qx, qy, qz, qw = ( -0.4226,0.0,0.0,0.9063)
orig_quat = mathutils.Quaternion((qw, qx, qy, qz))

#qx, qy, qz, qw = config["quaternion"]
#orig_quat = mathutils.Quaternion()

#user data

data_quat = mathutils.Quaternion(( 0.343712,0.137304,0.850561,0.373572))
data_pos = mathutils.Vector((-15.187, -9.01246, 9.80008))

#dataset quat * scene quat
final_quat =   orig_quat @ data_quat
final_pos = orig_quat @ data_pos

#dataset pos
cam.location = final_pos
cam.rotation_quaternion = final_quat

