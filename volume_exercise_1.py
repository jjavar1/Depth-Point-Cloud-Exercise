import numpy as np
import open3d as o3d
import hdbscan

def visualize_open3d(pcd):
    """
    Visualize the point cloud using Open3D.

    Parameters:
        pcd (open3d.geometry.PointCloud): The point cloud to visualize.
    """
    o3d.visualization.draw_geometries([pcd])

def apply_hdbscan_clustering(points, min_cluster_size=15, min_samples=1):
    """
    Applies HDBSCAN clustering to the points and returns cluster labels.

    Parameters:
        points (numpy.ndarray): Array of points to cluster.
        min_cluster_size (int): The minimum size of clusters.
        min_samples (int): The minimum number of samples in a neighborhood for a point to be considered a core point.

    Returns:
        tuple: A tuple containing:
            - labels (numpy.ndarray): The cluster labels for each point.
            - clusterer (hdbscan.HDBSCAN): The HDBSCAN clusterer instance.
    """
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
    labels = clusterer.fit_predict(points)
    return labels, clusterer

def segment_object_by_height(pcd, z_min, z_max):
    """
    Segment the point cloud by a specified height range.

    Parameters:
        pcd (open3d.geometry.PointCloud): The point cloud to segment.
        z_min (float): Minimum height value for segmentation.
        z_max (float): Maximum height value for segmentation.

    Returns:
        tuple: A tuple containing:
            - segmented_pcd (open3d.geometry.PointCloud): The segmented point cloud.
            - mask (numpy.ndarray): Boolean mask used for segmentation.
    """
    points = np.asarray(pcd.points)
    # crating a boolean mask that selects points within the range
    mask = (points[:, 2] > z_min) & (points[:, 2] < z_max)
    return pcd.select_by_index(np.where(mask)[0]), mask

def estimate_cylinder_volume(pcd):
    """
    Estimates the volume of a horizontally aligned cylinder given a point cloud.

    Parameters:
        pcd (open3d.geometry.PointCloud): The point cloud of the cylinder.

    Returns:
        float: The estimated volume of the cylinder in cubic centimeters.
    """
    points = np.asarray(pcd.points)
    max_point = points.max(axis=0)
    min_point = points.min(axis=0)
    
    # calculate radius and height based on the pt cloud extents
    radius = max(max_point[0] - min_point[0], max_point[1] - min_point[1]) / 2
    height = max_point[2] - min_point[2]
    
    # cylindrical volume formula
    volume = np.pi * (radius ** 2) * height
    return volume * 1e6  # Convert to cm³

def get_object_volume_from_pointcloud(np_points, min_cluster_size, min_samples, z_min=0.01, z_max=0.12):
    """
    Calculate the volume of the largest cylinder-like cluster within a point cloud.

    Parameters:
        np_points (numpy.ndarray): The numpy array of point cloud data.
        min_cluster_size (int): The minimum size of clusters for HDBSCAN.
        min_samples (int): The minimum number of samples in a neighborhood for a point to be considered a core point.
        z_min (float): The minimum z-value for height segmentation.
        z_max (float): The maximum z-value for height segmentation.

    Returns:
        float: The volume of the largest identified cylinder in cubic centimeters.
    """
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np_points)
    
    # segment point cloud based on height limits to isolate the cylinder
    object_pcd, mask = segment_object_by_height(pcd, z_min, z_max)
    # apply clustering to ONLY segmented points (HBDscan is better for this due to memory limits)
    segmented_points = np_points[mask]
    labels, _ = apply_hdbscan_clustering(segmented_points, min_cluster_size, min_samples)
    
    # identify the largest cluster as its most likely to be the cylinder
    largest_cluster_idx = np.argmax(np.bincount(labels[labels >= 0]))
    cylinder_points = segmented_points[labels == largest_cluster_idx]
    cylinder_pcd = o3d.geometry.PointCloud()
    cylinder_pcd.points = o3d.utility.Vector3dVector(cylinder_points)
    
    # lets visualize to make sure
    visualize_open3d(cylinder_pcd)
    
    return estimate_cylinder_volume(cylinder_pcd)

if __name__ == "__main__":
    points = np.load("data/PointCloud_143122066753.npy")
    volume_cm3 = get_object_volume_from_pointcloud(points, 15, 1)
    print(f"The estimated volume of the object is {volume_cm3:.2f} cm³")
