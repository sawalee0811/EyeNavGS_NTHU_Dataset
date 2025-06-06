import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from pathlib import Path
from statistics import mean
import matplotlib.pyplot as plt

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
figsize=(16, 6)
# -------------------------------- setting end ------------------------------- #

# path
input_folder = r"K:\eye_gaze\all_user_output"
output_folder = r"K:\eye_gaze"

# parsing
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
            print(f" cannot handle {filename}: {e}")


df_all = pd.DataFrame(records)
scenes = sorted(df_all['scene'].unique())
users = sorted(df_all['user'].unique(), key=lambda x: int(x.replace("user", "")))

# draw
plt.figure(figsize=figsize)

sns.set_palette(sns.color_palette(color_palette))

ax = sns.barplot(
    data=df_all,
    x="scene",
    y="total_distance",
    hue="user",
    hue_order=users,
    #errorbar=None
)
ax.set(xlabel='', ylabel='Total Distance (m)')
ax.set(ylim = (0, 100))
plt.xticks(rotation=45)

# legend 
plt.legend(title="", fontsize=12, title_fontsize=2, ncol=5, loc="upper left")

# auto save
plt.savefig(f'{output_folder}/bar_all.png', dpi=300, bbox_inches='tight')

plt.tight_layout()
plt.show()
