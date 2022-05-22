import numpy as np
import color
import ray
import intersection
import vector
import random


class Scene:
    # shape_list = []
    # material_list = []
    # light_point_list = []

    # static variables:
    MIN_CON = 1.0 / 256

    # lists of stuff at the scene.
    def __init__(self, shape_list: list, material_list: list, light_point_list: list, background: color.Color, reclvl, shade_rays ):
        self.shape_list = shape_list
        self.material_list = material_list
        self.light_point_list = light_point_list
        self.background = background
        self.rec_lvl = reclvl
        self.shade_ray = shade_rays

    def ray_cast(self, r: ray.Ray):
        minDistanceSq = float('inf')
        closest_intersection = None
        # check every shape for intersection, find the minimal one
        for i in range(len(self.shape_list)):
            inter = self.shape_list[i].intersect(r, False)
            if inter is not None:
                vec = vector.minus(r.start_point, inter.inter_point)
                distance_sq = vector.dot_product(vec, vec)
                if distance_sq < minDistanceSq:
                    minDistanceSq = distance_sq
                    closest_intersection = inter
        return closest_intersection

    # what is the color of a point?
    def compute_color(self, input_intersection: intersection.Intersection, rec_count, contribution):
        if (input_intersection is None) or (rec_count == self.rec_lvl) or (contribution < self.MIN_CON):
            return self.background
        mat = input_intersection.material
        currColor = color.Color(0, 0, 0)

        mul_c_bg = self.background.mul_color(mat.diffuse)
        mul_s_bg = mul_c_bg.mul_scalar(mat.trans)
        currColor = currColor.plus(mul_s_bg)

        inter_point = input_intersection.inter_point
        # calculate every light_point in the list
        for light_point in self.light_point_list:
            revLightDir = vector.normalized(vector.minus(light_point.position, inter_point))
            lightRefDir = vector.normalized(vector.reflect(revLightDir, input_intersection.normal))
            start = vector.add(inter_point, vector.multiply(revLightDir, 0.001))
            illumination = 1.0
            invCountOfShadeRays = 1.0 / self.shade_ray
            shadeRayFraction = 1.0 / self.shade_ray / self.shade_ray * light_point.shadow
            lightWidthR = vector.multiply(vector.some_perpendicular(revLightDir), light_point.radius)
            lightWidthD = vector.multiply(vector.cross_product(lightWidthR, vector.normalized(revLightDir)),
                                          light_point.radius)
            # rayLength = None
            # for every shade ray pair:
            for i in range(self.shade_ray):
                for j in range(self.shade_ray):
                    randomUp = random.random()
                    randomRight = random.random()
                    vec = vector.multiply(lightWidthD,
                                          ((-self.shade_ray / 2 + j + randomUp - 0.5) * invCountOfShadeRays))
                    vec2 = vector.multiply(lightWidthR,
                                           ((-self.shade_ray / 2 + i + randomRight - 0.5) * invCountOfShadeRays))
                    nearestLightPoint = vector.add(light_point.position, vector.add(vec, vec2))
                    # Reverse the direction of the shadow
                    revShadeDir = vector.normalized(vector.minus(nearestLightPoint, start))
                    rayLength = vector.vector_len(vector.minus(start, nearestLightPoint))
                    lightLeftInRay = 1.0
                    for s in self.shape_list:
                        currRay = ray.Ray(vector.add(start, vector.multiply(revShadeDir, 0.01)), revShadeDir)
                        shadowHit = s.intersect(currRay, True)
                        if shadowHit is not None and vector.vector_len(
                                vector.minus(shadowHit.inter_point, start)) < rayLength:
                            lightLeftInRay *= s.material.trans
                            if lightLeftInRay < 0:
                                lightLeftInRay = 0
                                break
                    illumination -= shadeRayFraction * (1 - lightLeftInRay)

            if illumination > 0:
                # computation of diffuse light
                diffuseColor = light_point.color.mul_color(
                    mat.diffuse.mul_scalar(vector.dot_product(input_intersection.normal, revLightDir)))
                # computation of specular light
                specularColor = light_point.color.mul_color(mat.specular.mul_scalar(
                    light_point.specular * pow(abs(vector.dot_product(lightRefDir, input_intersection.direction)),
                                               mat.phong)))
                currColor = currColor.plus(diffuseColor.plus(specularColor).mul_scalar((1 - mat.trans) * illumination))

        # now reflection color
        refDirHit = vector.reflect(input_intersection.direction, input_intersection.normal)
        ray2 = ray.Ray(vector.add(input_intersection.inter_point, vector.multiply(refDirHit, 0.001)), refDirHit)
        rayReflection = self.ray_cast(ray2)
        reflectionColor = mat.reflection.mul_color(
            self.compute_color(rayReflection, rec_count + 1, contribution * mat.reflection.gray_scale()))
        currColor = currColor.plus(reflectionColor)
        if mat.trans > 0:
            rayRec = ray.Ray(
                vector.add(input_intersection.inter_point, vector.multiply(input_intersection.direction, 0.01)),
                input_intersection.direction)
            currNext = self.ray_cast(rayRec)
            currColor = currColor.plus(
                self.compute_color(currNext, rec_count + 1, contribution * mat.trans).mul_scalar(mat.trans))
        return currColor
