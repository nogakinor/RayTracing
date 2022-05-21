import numpy as np
import vector
from camera import Camera
from color import Color
from material import Material
from sphere import Sphere
from plane import Plane
from lightpoint import LightPoint
from scene import Scene
from cube import Cube
from ray import Ray
import random
import time
from PIL import Image


# static class
class RayTracer:
    # ********** fields init with default values **********
    # TODO: get these from input
    image_width = 500
    image_height = 500

    # Todo what is this

    def __init__(self):
        self.camera = None
        self.scene = None

    def parseScene(self, sceneFileName):
        f = open(sceneFileName)

        lineNum = 0
        print("Started parsing scene file " + sceneFileName)
        materialList = []  # of materials
        shapeList = []  # of shapes
        lightPointList = []  # of light points
        backGround = 0  # Will be Color from input

        shadeRays = 0
        recLvl = 0
        line = f.readline()
        for line in f:
            line = line.strip()
            lineNum += 1
            if not line or (line[0] == '#'):  # This line in the scene file is a comment
                continue
            else:
                code = line[0:3].lower()
                # Split according to white space characters:
                params = line[3:].strip().lower().split()
                if code == "cam":
                    position = np.array([float(params[0]), float(params[1]), float(params[2])])
                    lookAt = np.array([float(params[3]), float(params[4]), float(params[5])])
                    up = np.array([float(params[6]), float(params[7]), float(params[8])])
                    self.camera = Camera(position, lookAt, up, float(params[9]), float(params[10]))
                    print("Parsed camera parameters (line {l})".format(l=lineNum))
                elif code == "set":
                    backGround = Color(float(params[0]), float(params[1]), float(params[2]))
                    shadeRays = int(params[3])
                    recLvl = int(params[4])
                    print("Parsed general settings (line {l})".format(l=lineNum))
                elif code == "mtl":
                    diffuse = Color(float(params[0]), float(params[1]), float(params[2]))
                    specular = Color(float(params[3]), float(params[4]), float(params[5]))
                    reflection = Color(float(params[6]), float(params[7]), float(params[8]))
                    material = Material(diffuse, specular, reflection, float(params[9]), float(params[10]))
                    # TODO add iterator to materials
                    # https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
                    materialList.append(material)
                    print("Parsed material (line {l})".format(l=lineNum))
                elif code == "sph":
                    center = np.array([float(params[0]), float(params[1]), float(params[2])])
                    sphere = Sphere(center, float(params[3]), materialList[int(params[4]) - 1])
                    # TODO add iterator to Spheres
                    # https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
                    shapeList.append(sphere)
                    print("Parsed sphere (line {l})".format(l=lineNum))
                elif code == "pln":
                    currVector = np.array([float(params[0]), float(params[1]), float(params[2])])
                    plane = Plane(currVector, float(params[3]), materialList[int(params[4]) - 1])
                    # TODO add iterator to Planes
                    # https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
                    shapeList.append( plane)
                    print("Parsed plane (line {l})".format(l=lineNum))
                elif code == "box":
                    center = np.array([float(params[0]), float(params[1]), float(params[2])])
                    scale = float(params[3])
                    material_index = int(params[4])
                    box = Cube(center, np.array([scale,scale,scale]), materialList[material_index-1])
                    shapeList.append(box)
                    print("Parsed Box (line {l})".format(l=lineNum))
                elif code == "lgt":
                    vctr = np.array([float(params[0]), float(params[1]), float(params[2])])
                    color = Color(float(params[3]), float(params[4]), float(params[5]))
                    light = LightPoint(vctr, color, float(params[6]), float(params[7]), float(params[8]))
                    # TODO add iterator to Light
                    # https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
                    lightPointList.append( light)
                    print("Parsed light (line {l})".format(l=lineNum))
                else:
                    print("ERROR: Did not recognize object: {c} (line {l})".format(c=code, l=lineNum))
        currScene = Scene(shapeList, materialList, lightPointList, backGround, recLvl, shadeRays)
        self.scene = currScene
        print("Finished parsing scene file " + sceneFileName)

    # TODO
    def renderScene(self, outputFileName):
        start_time = time.time()
        rgb_data = self.ray_casting_scene(self.camera, self.scene, self.image_width, self.image_height)
        self.save_image(self.image_width, rgb_data, outputFileName)
        end_time = time.time()
        render_time = end_time - start_time
        print("finished")

    # TODO
    def ray_casting_scene(self, c: Camera, scene: Scene, width, height):
        screen_height = c.screen_w / width * height
        rgb_data_size = self.image_width * self.image_height * 3
        pixel_to_the_right = vector.multiply(c.right, c.screen_w / width)
        pixel_to_down = vector.multiply(c.up, -screen_height / height)
        vec1 = vector.multiply(c.look_at, c.screen_d)
        vec2 = vector.multiply(c.right, -c.screen_w / 2)
        vec3 = vector.multiply(c.up, screen_height / 2)
        curScreenPoint = vector.add(vector.add(c.position, vec1), vector.add(vec2, vec3))
        curScreenPoint = vector.add(curScreenPoint, vector.multiply(pixel_to_the_right, 0.5))
        curScreenPoint = vector.add(curScreenPoint, vector.multiply([pixel_to_down], 0.5))
        rgb_data = [0] * rgb_data_size

        for y in range(height):
            for x in range(width):
                rayDirection = vector.normalized(vector.minus(curScreenPoint, c.position))
                intersection = scene.ray_cast(Ray(c.position, rayDirection))
                curScreenPointColor = scene.compute_color(intersection, 0, 1)
                pixel_id = (y * self.image_height + x) * 3
                rgb_data[pixel_id] = curScreenPointColor.get_red()
                rgb_data[pixel_id + 1] = curScreenPointColor.get_green()
                rgb_data[pixel_id + 2] = curScreenPointColor.get_blue()
                curScreenPoint = vector.add(curScreenPoint, pixel_to_the_right)
            curScreenPoint = vector.minus(curScreenPoint, vector.multiply(pixel_to_the_right, width))
            curScreenPoint = vector.add(curScreenPoint, pixel_to_down)
        rgb_nparray = np.asarray(rgb_data)
        rgb_nparray = rgb_nparray.reshape(self.image_width, self.image_height, 3)
        return rgb_nparray

    def save_image(self, width: int, image: list, file_name):
        try:
            image = np.clip(image, 0,1)
            result = Image.fromarray(np.uint8(image * 255), mode='RGB')
            result.show()
            result.save(file_name)
        except:
            print("error occured when tried to save image in {f}".format(f = file_name))
