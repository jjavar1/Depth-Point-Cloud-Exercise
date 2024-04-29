import numpy as np
import open3d

def visualize_open3d(pts):
    # check if the point cloud array is in the right shape.
    shape = pts.shape
    if shape[1] == 3:
        pass
    else:
        pts = np.transpose(pts)
    pc = open3d.geometry.PointCloud()
    pc.points = open3d.utility.Vector3dVector(pts)

    # visualize in open3d
    open3d.visualization.draw_geometries([pc])

def get_object_volume_from_pointcloud(points):

    # TODO: return the object volume estimation in (cm^3)
    vol = None

    return vol

if __name__ == "__main__":
    # Load in Point Clouds - (x,y,z) coordinate points in meters
    points = np.load("data/PointCloud_143122066753.npy")

    # TODO: Estimate the volume of the object
    volume = get_object_volume_from_pointcloud(points)

    # Visualize in Open3D
    visualize_open3d(points)
    
    

    