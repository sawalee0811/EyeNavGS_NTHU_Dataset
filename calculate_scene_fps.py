"""
This script calculates the average FPS for each scene in a structured dataset.
It separates traces by left and right eye, filters by frame interval threshold, and averages across users.

"""

import pandas as pd
import os
from pathlib import Path

# === USER CONFIGURATION ===
DATASET_PATH    = Path(rf"Path\to\Your\Data")  # <-- CHANGE THIS for your data
FPS_LIMIT       = 80
MIN_INTERVAL_MS = 1000.0 / FPS_LIMIT  # 12.5 ms
OUTPUT_CSV      = DATASET_PATH.parent  / "scene_average_fps.csv"


# === Function: Filter timesteps based on minimum frame interval ===
def filter_timesteps(timesteps: pd.Series, min_interval: float) -> pd.Series:
    filtered = [timesteps.iloc[0]]
    last_time = timesteps.iloc[0]
    for t in timesteps.iloc[1:]:
        if (t - last_time) >= min_interval:
            filtered.append(t)
            last_time = t
    return pd.Series(filtered)


# === Function: Compute FPS for a single eye trace ===
def compute_eye_fps(timesteps: pd.Series) -> float:
    if len(timesteps) < 2:
        return 0.0
    timesteps = timesteps.sort_values().reset_index(drop=True)
    filtered = filter_timesteps(timesteps, MIN_INTERVAL_MS)
    duration = (filtered.iloc[-1] - filtered.iloc[0]) / 1000.0  # in seconds
    frame_count = len(filtered)
    return frame_count / duration if duration > 0 else 0.0


# === Function: Process a single user trace and return average FPS ===
def compute_user_fps(csv_path: Path) -> float:
    try:
        df = pd.read_csv(csv_path, usecols=["ViewIndex", "timestep"])
    except Exception as e:
        print(f"[Error] Failed to load {csv_path.name}: {e}")
        return 0.0

    fps_list = []
    for eye in [0, 1]:  # 0: left, 1: right
        eye_data = df[df["ViewIndex"] == eye]["timestep"]
        if eye_data.empty:
            print(f"  [Warning] No data for eye {eye} in {csv_path.name}")
            continue
        fps = compute_eye_fps(eye_data)
        fps_list.append(fps)

    if len(fps_list) == 2:
        return sum(fps_list) / 2.0
    elif fps_list:
        return fps_list[0]
    else:
        return 0.0


# === Main Function: Process all scenes and write results ===
def calculate_all_scene_fps(dataset_path: Path, output_csv: Path):
    scene_results = []
    all_fps = []

    for scene_dir in sorted(dataset_path.iterdir()):
        if not scene_dir.is_dir():
            continue

        print(f"\n[Scene] Processing: {scene_dir.name}")
        user_fps_list = []

        #for file in scene_dir.glob("user*_fws.csv"):
        for file in scene_dir.glob("user*_*.csv"):
            print(f"  [User File] {file.name}")
            fps = compute_user_fps(file)
            print(f"    → User FPS: {fps:.2f}")
            if fps > 0:
                user_fps_list.append(fps)
                all_fps.append(fps)

        if user_fps_list:
            avg_scene_fps = round(sum(user_fps_list) / len(user_fps_list), 2)
            print(f"[Scene Average] {scene_dir.name}: {avg_scene_fps} FPS")
            scene_results.append({"SceneName": scene_dir.name, "avg_FPS": avg_scene_fps})
        else:
            print(f"[Warning] No valid user FPS data found in {scene_dir.name}")

    # Add overall average row
    if all_fps:
        overall_avg = round(sum(all_fps) / len(all_fps), 2)
        print(f"\n[Overall Average FPS] Across All Scenes: {overall_avg} FPS")
        scene_results.append({"SceneName": "Overall_Average", "avg_FPS": overall_avg})

    # Write to CSV
    df_result = pd.DataFrame(scene_results)
    df_result.to_csv(output_csv, index=False)
    print(f"\n[Done] Scene FPS results written to: {output_csv}")


    # Write to CSV
    df_result = pd.DataFrame(scene_results)
    df_result.to_csv(output_csv, index=False)
    print(f"\n[Done] Scene FPS results written to: {output_csv}")


# === Entry Point ===
if __name__ == "__main__":
    calculate_all_scene_fps(DATASET_PATH, OUTPUT_CSV)
