# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import RayTracer
import argparse

# TODO: change accordingly
def get_args():
    """A Helper function that defines the program arguments."""
    parser = argparse.ArgumentParser(description='Image resizing application, supporting multiple different resizing '
                                                 'methods including [Nearest neighbor interpolation, '
                                                 'Seam Carving, Seam Carving with Feed Forward Implementation.')
    parser.add_argument('--image_path', type=str, help='The input image path')
    parser.add_argument('--output_dir', type=str, help='The output directory')
    parser.add_argument('--height', type=int, help='The output image height size')
    parser.add_argument('--width', type=int, help='The output image width size')
    parser.add_argument('--resize_method', type=str, help='The resizing method. Supported methods are '
                                                          '[nearest_neighbor, seam_carving].')
    parser.add_argument('--use_forward_implementation', action='store_true',
                        help='If set and seam_carving is used as a resizing method, then the forward-looking '
                             'implementation is used.')
    # default out prefix is img
    parser.add_argument('--output_prefix', type=str, help='Output filename prefix.', default='img')
    args = parser.parse_args()
    return args


def main(args):
    # Use a breakpoint in the code line below to debug your script.
    ray_tracer = RayTracer()

# TODO - count expected args and throw exception
    if len(args) < 2:
        return "not enough arguments"

    scene_file_name = args.scene_file_name
    output_file_name = args.output_file_name

    if len(args) > 3:
        ray_tracer.image_width = args.image_width
        ray_tracer.image_height = args.image_height

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = get_args()
    main(args)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
