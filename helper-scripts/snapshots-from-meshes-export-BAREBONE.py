import open3d as o3d


def generate_snapshot(ply_path, image_path, viewpoint_path):
    # Load point cloud and saved viewpoint
    pcd = o3d.io.read_point_cloud(ply_path)
    param = o3d.io.read_pinhole_camera_parameters(viewpoint_path)
    
    # Create visualization, set viewpoint, and capture image
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=800, height=600, visible=True)  # Specify window size
    vis.add_geometry(pcd)
    vis.get_view_control().convert_from_pinhole_camera_parameters(param)
    #change field of view
    vis.get_render_option().point_size = 0.5
    
    # Update geometry, poll events, update renderer
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.run()
    # Capture and save image
    vis.capture_screen_image(image_path, do_render=True)  # Ensure rendering
    vis.destroy_window()

# Example usage
ply_file_path = "/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scannned-data-single-img-50-qual-90-processed/evaluations/nerfacto/5000/evaluation/CCL-scannned-data-single-img-50-qual-90-processed.precision.ply"
output_image_path = "output_snapshot.png"
viewpoint_path = "helper-scripts/saved_viewpoint.json"

generate_snapshot(ply_file_path, output_image_path, viewpoint_path)

ply_file_path = "/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scannned-data-single-img-50-qual-90-processed/evaluations/nerfacto/5000/evaluation/CCL-scannned-data-single-img-50-qual-90-processed.precision.ply"
