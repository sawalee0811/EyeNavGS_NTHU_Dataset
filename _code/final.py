import bpy
import math
import mathutils
import csv

#Settings
csv_path = r"\eye_gaze\user8_fixed\user8_stump_fws.csv"  # path
scene_name = "stump"                              # witch scene
fps = 30        # set fps
obj = bpy.data.objects.get(scene_name)

#Scene parameter
scene_configs = {
    "truck":     {"flip_x": True, "quaternion": (-0.0872, 0.0, 0.0, 0.9962), "scale": 0.8},
    "treehill":  {"flip_x": True, "quaternion": (-0.2164, 0.0, 0.0, 0.9763), "scale": 1},
    "train":     {"flip_x": True, "quaternion": (0.0872, 0.0, 0.0, 0.9962),  "scale": 0.2},
    "stump":     {"flip_x": True, "quaternion": (-0.4226, 0.0, 0.0, 0.9063), "scale": 3},
    "room":      {"flip_x": True, "quaternion": (-0.2164, 0.0, 0.0, 0.9763), "scale": 2},
    "playroom":  {"flip_x": True, "quaternion": (-0.2164, 0.0, 0.0, 0.9763), "scale": 2},
    "kitchen":   {"flip_x": True, "quaternion": (-0.3420, 0.0, 0.0, 0.9397), "scale": 5},
    "garden":    {"flip_x": True, "quaternion": (-0.2588, 0.0, 0.0, 0.9659), "scale": 1},
    "flowers":   {"flip_x": True, "quaternion": (0.1305, 0.0, 0.0, 0.9914),  "scale": 1},
    "drjohnson": {"flip_x": False, "quaternion": (0.2126, -0.2126,0.6744, 0.6744), "scale": 1},
    "counter":   {"flip_x": True, "quaternion": (-0.3007, 0.0, 0.0, 0.9537), "scale": 4},
    "bonsai":    {"flip_x": True, "quaternion": (-0.3420, 0.0, 0.0, 0.9397), "scale": 3},
    "bicycle":   {"flip_x": True, "quaternion": (-0.1305, 0.0, 0.0, 0.9914), "scale": 1},
}

#Rotate the scene
scene_data = scene_configs[scene_name]
qx, qy, qz, qw = scene_data["quaternion"]
scene_quat = mathutils.Quaternion((qw, qx, qy, qz))

if scene_data.get("flip_x", True):
    flip_x = mathutils.Quaternion((1, 0, 0), math.radians(180))
    scene_rot = flip_x @ scene_quat
else:
    scene_rot = scene_quat

obj.rotation_quaternion = scene_rot
obj.scale = (scene_data["scale"],) * 3


# Rotate the cam and visualize the trace
cam = bpy.data.objects.get("Camera")
if cam is None:
    raise ValueError("No Camera finded!")

cam.rotation_mode = 'QUATERNION'

# Read CSV and insert keyframe base on timestep
with open(csv_path, newline='') as csvfile:
    reader = list(csv.DictReader(csvfile))

    for row in reader:
        if row['ViewIndex'] != '0':  # view in left_eye
            continue
        timestep_ms = float(row['timestep'])
        frame = round((timestep_ms / 1000.0) * fps)

        # user quaternion（w, x, y, z）
        data_quat = mathutils.Quaternion((
            float(row['QuaternionW']),
            float(row['QuaternionX']),
            float(row['QuaternionY']),
            float(row['QuaternionZ'])
        ))

        # Rotate user quat
        final_quat = scene_quat @ data_quat

        # user position
        user_pos = mathutils.Vector((
            float(row['PositionX']),
            float(row['PositionY']),
            float(row['PositionZ'])
        ))
        
        final_pos = scene_quat @ user_pos

        # Set Cam
        cam.location = final_pos
        cam.rotation_quaternion = final_quat
        cam.keyframe_insert(data_path="location", frame=frame)
        cam.keyframe_insert(data_path="rotation_quaternion", frame=frame)
        