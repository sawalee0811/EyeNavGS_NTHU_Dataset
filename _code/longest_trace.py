import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from pathlib import Path
from statistics import mean
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R


# ------------------- plotting template apply ------------------- #

# font
csfont = {'family':'Times New Roman', 'serif': 'Times' , 'size' : 18}
plt.rc('text', usetex=True)
plt.rc('font', **csfont)

figsize = (8, 5)
# -------------------------------------------------------------- #

# Read CSV
df = pd.read_csv(rf"Path\to\Your\csv")
output_folder = rf"eye_gaze"

# Normalize scale for consistent axes
all_x, all_y, all_z = df['PositionX'], df['PositionY'], df['PositionZ']
min_val = min(all_x.min(), all_y.min(), all_z.min())
max_val = max(all_x.max(), all_y.max(), all_z.max())

def plot_view(df_subset, view_label, color):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    # Draw trajectory
    ax.plot(
        df_subset['PositionX'],
        df_subset['PositionZ'],
        df_subset['PositionY'],
        color=color, linewidth=1, label=f'ViewIndex {view_label}'
    )

    ax.set_xlabel(r'\textbf{Left-Right (X)(m)}', labelpad=10)
    ax.set_ylabel(r'\textbf{Front-Back (Z)(m)}', labelpad=10)
    ax.set_zlabel(r'\textbf{Up-Down (Y)(m)}', labelpad=10)

    center_x = all_x.mean()
    center_y = all_z.mean()  # new Y ←  Z
    center_z = all_y.mean()  # new Z ←  Y

    range_x = all_x.max() - all_x.min()
    range_y = all_z.max() - all_z.min()
    range_z = all_y.max() - all_y.min()
    max_range = max(range_x, range_y, range_z) / 2

    ax.set_xlim(center_x - max_range, center_x + max_range)
    ax.set_ylim(center_y - max_range, center_y + max_range)
    ax.set_zlim(center_z - max_range, center_z + max_range)


    ax.tick_params(labelsize=10)
    ax.view_init(elev=25, azim=135)

    # auto save
    plt.savefig(f'{output_folder}/3D_trace.png', dpi=300)

    plt.tight_layout()
    plt.show()

# Plot left eye (ViewIndex 0)
plot_view(df[df['ViewIndex'] == 0], view_label=0, color='#1f77b4')

