import math
import csv
import mathutils

# CONFIG
input_csv = r"K:\TEST\user1_fixed\user1_truck_fws.csv"
output_csv = r"K:\TEST\corrected\user1_truck_fws_corrected_left.csv"
fps = 37
scene_name = "truck"

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

# Scene quaternion
qx, qy, qz, qw = scene_configs[scene_name]["quaternion"]
scene_rot = mathutils.Quaternion((qw, qx, qy, qz))


# Output columns
fieldnames = [
    'ViewIndex',
    'PositionX', 'PositionY', 'PositionZ',
    'QuaternionW', 'QuaternionX', 'QuaternionY', 'QuaternionZ',
    'EulerX', 'EulerY', 'EulerZ',
    'timestep', 'Distance'
]

# Main
data_rows = []

with open(input_csv, newline='') as infile:
    reader = list(csv.DictReader(infile))

    prev_pos = None
    for row in reader:
        if row['ViewIndex'] != '0':
            continue

        # original  data
        user_pos = mathutils.Vector((
            float(row['PositionX']),
            float(row['PositionY']),
            float(row['PositionZ'])
        ))
        user_quat = mathutils.Quaternion((
            float(row['QuaternionW']),
            float(row['QuaternionX']),
            float(row['QuaternionY']),
            float(row['QuaternionZ'])
        ))

        # rotate
        pos = scene_rot @ user_pos
        quat = scene_rot @ user_quat
        euler = quat.to_euler()

        # dist this move
        if prev_pos is None:
            dist = 0.0
        else:
            dist = (pos - prev_pos).length
        prev_pos = pos.copy()

        data_rows.append({
            'ViewIndex': row['ViewIndex'],
            'PositionX': pos.x,
            'PositionY': pos.y,
            'PositionZ': pos.z,
            'QuaternionW': quat.w,
            'QuaternionX': quat.x,
            'QuaternionY': quat.y,
            'QuaternionZ': quat.z,
            'EulerX': math.degrees(euler.x),
            'EulerY': math.degrees(euler.y),
            'EulerZ': math.degrees(euler.z),
            'timestep': row['timestep'],
            'Distance': dist
        })
        
# Export
with open(output_csv, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_rows)

print(f"Exported to: {output_csv}")