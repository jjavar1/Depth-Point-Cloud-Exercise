# Cylinder Volume Estimation from Point Cloud

## Overview
This project showcases a method for estimating the volume of a ***horizontally*** aligned cylinder using a 3D point cloud. The project utilizes Python, Open3D, and HDBSCAN to efficiently process point cloud data. It segments the data based on height, applies clustering techniques, and accurately calculates the volume of the point cloud cylinder.

The volume result should be printed in the console, and the cylinder visualization should be opened.

**Note: the output will only show after closing the visualization window, this is to adhere to the method requirements**


## Prerequisites
- Python 3.8-3.11 (Python 3.12 not supported)
- Open3D
- NumPy
- HDBSCAN

## Installation
Clone and install the required packages using pip:
It is highly recommended to use a virtual environment for using this project.

```bash
git clone https://github.com/jjavar1/Depth-Point-Cloud-Exercise.git
pip install -r requirements.txt
```

## Installation
To run:

```bash
python volume_exercise_1.py
```

To test:

```bash
python volume_exercise_test.py
```

## Methodology:
1. Height Segmentation: Filters the point cloud to only include points within a specific height range.

2. Clustering: HDBSCAN clusters segmented points based on spatial proximity.

3. Volume Calculation: Estimates the volume of the detected cylinder based on geometric properties extracted from the cluster.

## Thoughts and Pitfalls
### Thoughts
- First checked if the npy had color information in its coordinates, upon inspection it was just an array of the points and the z,y,z coordinates.

- The height information is embedded in the npy.

- Doing the volume calculation just based on height and histogram data was not conclusive enough as there could be outliers that are not the cylinder.

- Looked up clustering algorithms, tried DBSCAN. DBSCAN took too much memory even after voxel downsampling (almost 20gb of memory!)

- Instead went with HBDSCAN (doesnt require distance matrix to be stored in memory - much faster, less than 250mb of memory)

- Since the clustering algorithm would just cluster the floor (since the points are in a large cluster), I used the histogram points of the max/minumum height data.

- After filtering, the cluster data only pointed to the cylinder.

### Pitfalls
- This assumes the cylinder orientaion and position. If it varies to much accross datasets, the segmentation might miss it or incorrectly segment another object.

- HDBSCAN params need to be fine tuned (density, distribution, noise level). May result in over/under segmentation.

- Accuracy is dependant on the quality and density of the point cloud.

- Computationally, might be a little too much for what we're trying to do.


