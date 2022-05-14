import raytracer
import sys


# The code should run in the command line (you need to send a directory with
# all the python code files) and accept 4 parameters. For example:
# python RayTracer.py scenes\Spheres.txt scenes\Spheres.png 500 500
# those final two are optional, default value is 500x500
def main():
    ray_tracer = raytracer.RayTracer()
    scene_file_name = ""
    output_file_name = ""

    # TODO - count expected args and throw exception
    if len(sys.argv) < 2:
        print("not enough arguments")
        return
    if len(sys.argv) == 2:
        # Default width and height are 500x500
        width = 500
        height = 500
        scene_file_name = sys.argv[0]
        output_file_name = sys.argv[1]
    if len(sys.argv) == 3:
        print("input 2 arguments or 4")
        return
    if len(sys.argv) == 4:
        # We got optional arguments
        width = sys.argv[3]
        height = sys.argv[4]
        scene_file_name = sys.argv[0]
        output_file_name = sys.argv[1]
    if len(sys.argv) > 4:
        print("too many arguments")
        return

    # TODO send the arguments to the ray Tracer
    ray_tracer.parseScene(scene_file_name)
    ray_tracer.renderScene(output_file_name)


# Main Function Run
if __name__ == '__main__':
    main()
