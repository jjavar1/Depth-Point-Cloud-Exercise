import unittest
from volume_exercise_1 import estimate_cylinder_volume
import numpy as np
import logging
import open3d as o3d

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

class TestVolumeEstimation(unittest.TestCase):
    def test_cylinder_volume_estimation(self):
        logging.debug("Starting test for cylinder volume estimation")
        
        # create a point cloud that resembles a "perfect" cylinder
        mesh_cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=1, height=5)
        pcd = mesh_cylinder.sample_points_poisson_disk(number_of_points=1000)

        # calculate estimated vol
        estimated_volume = estimate_cylinder_volume(pcd)
        expected_volume = np.pi * 1**2 * 5 * 1e6  # Volume in cm³, given radius=1 and height=5
        
        logging.debug(f"Calculated estimated volume: {estimated_volume}")
        logging.debug(f"Expected volume: {expected_volume}")

        # error margin
        self.assertAlmostEqual(estimated_volume, expected_volume, delta=expected_volume*0.1)  # Allow 10% error

        logging.debug("Test for cylinder volume estimation completed")

if __name__ == "__main__":
    unittest.main()
