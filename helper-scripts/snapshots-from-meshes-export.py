import json
import time

import numpy as np
import open3d as o3d


def generate_snapshot(ply_path, image_path, viewpoint_path, zoom_factor=5):
    # Load point cloud
    pcd = o3d.io.read_point_cloud(ply_path)

    # Visualize Point Cloud
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)

    # Read camera params
    param = o3d.io.read_pinhole_camera_parameters('saved_viewpoint.json')
    ctr = vis.get_view_control()
    ctr.convert_from_pinhole_camera_parameters(param)

    # Updates
    vis.update_geometry()
    vis.poll_events()
    vis.update_renderer()

    # Capture image
    time.sleep(1)
    vis.capture_screen_image('cameraparams.png')
    # image = vis.capture_screen_float_buffer()

    # Close
    vis.destroy_window()


# Example usage
ply_file_path = "/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scannned-data-single-img-50-qual-90-processed/evaluations/nerfacto/5000/evaluation/CCL-scannned-data-single-img-50-qual-90-processed.precision.ply"
output_image_path = "output_snapshot.png"
viewpoint_path = "saved_viewpoint.json"

generate_snapshot(ply_file_path, output_image_path, viewpoint_path)


# generate_snapshot(ply_file_path, output_image_path, viewpoint_path)

ply_file_path = "/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scannned-data-single-img-50-qual-90-processed/evaluations/nerfacto/5000/evaluation/CCL-scannned-data-single-img-50-qual-90-processed.precision.ply"

