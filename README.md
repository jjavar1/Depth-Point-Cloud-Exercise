# Cylinder Volume Estimation from Point Cloud

## Overview
This project showcases a method for estimating the volume of a ***horizontally*** aligned cylinder using a 3D point cloud. The project utilizes Python, Open3D, and HDBSCAN to efficiently process point cloud data. It segments the data based on height, applies clustering techniques, and accurately calculates the volume of the point cloud cylinder.


## Prerequisites
- Python 3.8-3.11 (Python 3.12 not supported)
- Open3D
- NumPy
- HDBSCAN
- scikit-learn

## Installation
Clone and install the required packages using pip:

```bash
git clone https://github.com/jjavar1/DepthPointCloud.git
cd depthpointcloud
pip install -r requirements.txt

## Installation
To run:

```bash
pythoin volume_exercise_1.py

## Methodology:
1. Height Segmentation: Filters the point cloud to only include points within a specific height range.

2. Clustering: HDBSCAN clusters segmented points based on spatial proximity.

3. Volume Calculation: Estimates the volume of the detected cylinder based on geometric properties extracted from the cluster.