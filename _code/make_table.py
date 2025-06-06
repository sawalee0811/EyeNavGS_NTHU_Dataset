import os
import pandas as pd
import numpy as np

# path
input_folder = r"K:\eye_gaze\all_user_output"

# init for all scenes position
scene_pos = {}

# run CSVs
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        try:
            parts = filename.replace(".csv", "").split("_")
            if len(parts) >= 4:
                user = parts[0]
                scene = parts[1]
                df = pd.read_csv(file_path)
                if all(col in df.columns for col in ["PositionX", "PositionY", "PositionZ"]):
                    x_vals = df["PositionX"].dropna().values
                    y_vals = df["PositionY"].dropna().values
                    z_vals = df["PositionZ"].dropna().values

                    if scene not in scene_pos:
                        scene_pos[scene] = {"X": [], "Y": [], "Z": []}

                    scene_pos[scene]["X"].extend(x_vals)
                    scene_pos[scene]["Y"].extend(y_vals)
                    scene_pos[scene]["Z"].extend(z_vals)
        except Exception as e:
            print(f"cannot handle {filename}: {e}")

# Make table
scenes_sorted = sorted(scene_pos.keys())
rows = ["Position X", "Position Y", "Position Z"]
data = []

for axis in ["X", "Y", "Z"]:
    row = []
    for scene in scenes_sorted:
        values = scene_pos[scene][axis]
        if len(values) > 0:
            min_val = np.min(values)
            max_val = np.max(values)
            row.append(f"({min_val:.2f}, {max_val:.2f})")
        else:
            row.append("(N/A)")
    data.append(row)

summary_df = pd.DataFrame(data, index=rows, columns=scenes_sorted)

# output
print(summary_df)

# export
summary_df.to_csv(r"K:\eye_gaze\XYZrange_table.csv")
