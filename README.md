# EyeNavGS Dataset
This repository contains the dataset for 👁️NavGS: A 6-DoF Navigation Dataset and Record-n-Replay Software for Real-World 3DGS Scenes in VR

Zihao Ding¹, Cheng‑Tse Lee², Mufeng Zhu¹, Tao Guan¹, Yuan‑Chun Sun², Cheng‑Hsin Hsu², Yao Liu¹<br>
¹ Rutgers University | ² National Tsing Hua University<br>
\| [Webpage](https://symmru.github.io/EyeNavGS/) | [Full Paper](https://arxiv.org/abs/2506.02380)

## Overview
EyeNavGS provides high-fidelity user navigation traces in real-world 3D Gaussian Splatting (3DGS) scenes. The dataset is designed for research on VR-based navigation, behavior analysis, and neural rendering evaluation.
You can attach the software's source code [here](https://github.com/symmru/EyeNavGS_Software).

## Parameters
The following table summarizes the parameters used when capturing navigation traces.

These can be also found in scene_setting.csv.
| Dataset_Name | Quaternion (X Y Z W)           | Scale (float)       |
|--------------|--------------------------------|---------------------|
| truck        | -0.0872 0.0000 0.0000 0.9962   | --initial-scale 0.8 |
| treehill     | -0.2164 0.0000 0.0000 0.9763   | --initial-scale 1   |
| train        |  0.0872 0.0000 0.0000 0.9962   | --initial-scale 0.2 |
| stump        | -0.4226 0.0000 0.0000 0.9063   | --initial-scale 3   |
| room         | -0.2164 0.0000 0.0000 0.9763   | --initial-scale 2   |
| playroom     | -0.2164 0.0000 0.0000 0.9763   | --initial-scale 2   |
| bicycle      | -0.1305 0.0000 0.0000 0.9914   | --initial-scale 1   |
| drjohnson    | -0.2126 0.2126 0.6744 0.6744   | --initial-scale 1   |
| nyc          | -0.1305 0.0000 0.0000 0.9914   | --initial-scale 0.4 |
| london       | -0.0436 0.0000 0.0000 0.9990   | --initial-scale 0.4 |
| berlin       |  0.0435 0.0038 -0.0870 0.9952  | --initial-scale 0.6 |
| alameda      | -0.1736 0.0000 0.0000 0.9848   | --initial-scale 0.4 |

## Code
You can attach some code we use to analysis in  folder "_code".
