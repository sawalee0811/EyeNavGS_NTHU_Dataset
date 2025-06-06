import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from pathlib import Path
from statistics import mean
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ------------------------------- setting start ------------------------------ #
# color
color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
errorbar_color = "#3A3A3A"

# font
csfont = {'family':'Times New Roman', 'serif': 'Times' , 'size' : 23}
plt.rc('text', usetex=True)
plt.rc('font', **csfont)

# bar plot size
bar_width = 0.4
bar_btw_space = 0.04
bar_space = 0.2

# errorbar plot size
err_lw=1.5
err_capsize=4
err_capthick=1.5

# set fig size
figsize=(10, 4.8)
# -------------------------------- setting end ------------------------------- #

# path
input_folder = r"eye_gaze\all_user_output"
output_folder = r"eye_gaze"

records = []

for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        try:
            df = pd.read_csv(file_path)
            if len(df) > 1:
                last_row = df.iloc[-1]
                if str(last_row.get("timestep")).strip().lower() == "totaldistance":
                    total_distance = float(last_row.get("Distance", 0))
                    parts = filename.replace(".csv", "").split("_")
                    if len(parts) >= 4:
                        user = parts[0]
                        scene = parts[1]
                        records.append({
                            "scene": scene,
                            "user": user,
                            "total_distance": total_distance
                        })
        except Exception as e:
            print(f"cannot handle {filename}: {e}")

df_all = pd.DataFrame(records)
scene_order = df_all["scene"].drop_duplicates().tolist()

# === Average total distance per scene ===
df_avg = df_all.groupby("scene", as_index=False)["total_distance"].mean()
df_avg = df_avg.sort_values(by="total_distance", ascending=False)

# === Plot ===
plt.figure(figsize=figsize)

sns.set_palette(sns.color_palette(color_palette))

ax = sns.barplot(
    data=df_avg,
    x="scene",
    y="total_distance",
    order=scene_order,
    hue="scene",        
)

ax.set(xlabel='', ylabel='Average Total Distance (m)')
ax.set(ylim = (0, 55))

# Add value on each bar
for bar in ax.patches:
    bar: Rectangle
    height = bar.get_height()
    if height > 0:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f'{height:.1f}',
            ha='center',
            va='bottom',
            fontsize=9
        )

# plt.xlabel("")
# plt.ylabel(r"Average Total Distance (m)")
plt.xticks(rotation=45)

# auto save
plt.savefig(f'{output_folder}/bar_avg.png', dpi=300, bbox_inches='tight')

plt.tight_layout()
plt.show()
