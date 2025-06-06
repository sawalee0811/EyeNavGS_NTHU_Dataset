import bpy
import math
import mathutils

scene_configs = {
    "truck":     {"position": (-2, 1.8, -4), "quaternion": (-0.0872, 0.0, 0.0, 0.9962), "scale": 0.8},
    "treehill":  {"position": (2, 1, 2),     "quaternion": (-0.2164, 0.0, 0.0, 0.9763), "scale": 1},
    "train":     {"position": (2, 0, 3),     "quaternion": (0.0872, 0.0, 0.0, 0.9962),  "scale": 0.2},
    "stump":     {"position": (-1, 1.1, -2), "quaternion": (-0.4226, 0.0, 0.0, 0.9063), "scale": 3},
    "room":      {"position": (0, 1.1, 0),   "quaternion": (-0.2164, 0.0, 0.0, 0.9763), "scale": 2},
    "playroom":  {"position": (0, 0.8, 0),   "quaternion": (-0.2164, 0.0, 0.0, 0.9763), "scale": 2},
    "kitchen":   {"position": (0.6, 0.7, 0), "quaternion": (-0.3420, 0.0, 0.0, 0.9397), "scale": 5},
    "garden":    {"position": (4, 1.7, 1),   "quaternion": (-0.2588, 0.0, 0.0, 0.9659), "scale": 1},
    "flowers":   {"position": (0, 0, -2),    "quaternion": (0.1305, 0.0, 0.0, 0.9914),  "scale": 1},
    "drjohnson": {"position": (0, 1.5, 0),   "quaternion": (0.2126, -0.2126,0.6744, 0.6744), "scale": 1},
    "counter":   {"position": (0, 1, -0.3),  "quaternion": (-0.3007, 0.0, 0.0, 0.9537), "scale": 4},
    "bonsai":    {"position": (0.7, 1, -1),  "quaternion": (-0.3420, 0.0, 0.0, 0.9397), "scale": 3},
    "bicycle":   {"position": (0, 0, 0),     "quaternion": (-0.1305, 0.0, 0.0, 0.9914), "scale": 1},
}

flip_x = mathutils.Quaternion((1, 0, 0), math.radians(180))

for name, config in scene_configs.items():
    obj = bpy.data.objects.get(name)
    if obj:
        obj.rotation_mode = 'QUATERNION'
        qx, qy, qz, qw = config["quaternion"]
        orig_quat = mathutils.Quaternion((qw, qx, qy, qz))
        
        if name == "drjohnson":
            final_quat =  orig_quat
        else:
            final_quat = flip_x @ orig_quat

        obj.rotation_quaternion = final_quat
        #obj.location = config["position"]
        obj.scale = (config["scale"],) * 3
    else:
        print(f"cannot find: {name}")
