import open3d as o3d
from PIL import Image


def generate_snapshot(ply_path, image_path, viewpoint_path, crop_percent=32):
    # Load point cloud and saved viewpoint
    pcd = o3d.io.read_point_cloud(ply_path)
    param = o3d.io.read_pinhole_camera_parameters(viewpoint_path)

    # Create visualization, set viewpoint, and capture image
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=800, height=600, visible=True) 
    vis.add_geometry(pcd)
    vis.get_view_control().convert_from_pinhole_camera_parameters(param)
    vis.get_render_option().point_size = 0.5
    
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    # Capture and save image
    vis.capture_screen_image(image_path, do_render=True)
    vis.destroy_window()

    # Open image with Pillow
    im = Image.open(image_path)

    # Calculate the crop box
    width, height = im.size
    new_width = width * crop_percent / 100
    new_height = height * crop_percent / 100
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    
    # Crop and save the image
    im_cropped = im.crop((left, top, right, bottom))
    im_cropped.save(image_path)

# Example usage with your paths
ply_file_path = "/work/mech-ai/arbab/tanksandtemples-eval/TanksAndTemples/python_toolbox/evaluation/data/CCL-scannned-data-single-img-50-qual-90-processed/evaluations/nerfacto/5000/evaluation/CCL-scannned-data-single-img-50-qual-90-processed.precision.ply"
output_image_path = "output_snapshot-compromise.png"
viewpoint_path = "saved_viewpoint.json"

generate_snapshot(ply_file_path, output_image_path, viewpoint_path)
