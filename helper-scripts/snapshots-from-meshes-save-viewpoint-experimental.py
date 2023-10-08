import json

import open3d as o3d


def save_viewpoint(ply_path, viewpoint_path):
    # Load point cloud
    pcd = o3d.io.read_point_cloud(ply_path)

    # Visualize and save viewpoint
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=800, height=600)  # Specify window size
    vis.add_geometry(pcd)
    vis.run()
    
    # Get camera model matrix and field of view
    param = vis.get_view_control().convert_to_pinhole_camera_parameters()
    cam = param.intrinsic.get_model_matrix()
    fov = param.intrinsic.get_fov()
    
    # Save viewpoint to file
    viewpoint_data = {
        'cam': cam.tolist(),  # Converting numpy array to list to store in json
        'fov': fov
    }
    
    with open(viewpoint_path, 'w') as f:
        json.dump(viewpoint_data, f)
    
    vis.destroy_window()
    
# Example usage
ply_file_path = "/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scannned-data-single-img-50-qual-90-processed/evaluations/nerfacto/5000/evaluation/CCL-scannned-data-single-img-50-qual-90-processed.precision.ply"
viewpoint_path = "saved_viewpoint.json"
save_viewpoint(ply_file_path, viewpoint_path)
