import numpy as np
import Color
import ray
import Intersection
import vector
import random

class Scene():
    shape_list = []
    material_list = []
    light_point_list = []
    MIN_CON = 1.0/256
    background = Color()
    shade_ray = 0
    rec_lvl = 0
    super_sampling_lvl = 0

    def __init__(self, shape_list, material_list, light_point_list):
        self.shape_list = shape_list
        self.material_list = material_list
        self.light_point_list

    def ray_cast(self, r: ray):
        min = float('inf')
        closest_intersection = None
        for i in range(len(self.shape_list)):
            inter = self.shape_list[i].intersect(r, False)
            if inter is not None:
                vec = vector.minus(r.start_point, inter.inter_point)
                distance_sq = vector.dot_product(vec, vec)
                if distance_sq < min:
                    min = distance_sq
                    closest_intersection = inter
        return closest_intersection

    def compute_color(self, intersection: Intersection, rec_count, contribution):
        if (intersection is None ) or (rec_count == self.rec_lvl) or (contribution < self.MIN_CON):
            return self.background
        mat = intersection.material
        color = Color(0,0,0)
        mul_c_bg = self.backGround.mulC(mat.diffuse)
        mul_s_bg = mul_c_bg.mulS(mat.trans)
        color = color.plus(mul_s_bg)
        inter_point = intersection.inter_point
        for light_point in self.light_point_list:
            revLightDir = vector.normalize(vector.minus(self.light.position, inter_point))
            lightRefDir = vector.normalize(vector.reflect(revLightDir, intersection.normal))
            start = vector.plus(inter_point, vector.multiply(revLightDir, 0.001))
            illumination = 1.0;
            invCountOfShadeRays = 1.0 / self.shade_ray
            shadeRayFraction = 1.0 / self.shade_ray / self.shade_ray * self.light.shadow
            lightWidthR = vector.multiply(vector.somePerpendicular(revLightDir), self.light.radius)
            lightWidthD = vector.multiply(vector.crossProduct(lightWidthR, vector.normalize(revLightDir)),
                                          self.light.radius)
            rayLength = None
            for i in range(self.shade_ray):
                for j in range(self.shade_ray):
                    randomUp = random.random()
                    randomRight = random.random()
                    vec = vector.multiply(lightWidthD, ((-self.shadeRays / 2 + j + randomUp - 0.5) * invCountOfShadeRays))
                    vec2 = vector.multiply(lightWidthR, ((-self.shadeRays / 2 + i + randomRight - 0.5) * invCountOfShadeRays))
                    nearestLightPoint = vector.plus(self.light.position, vector.plus(vec, vec2))
                    # Reverse the direction of the shadow
                    revShadeDir = vector.normalize(vector.minus(nearestLightPoint, start))
                    rayLength = vector.length(vector.minus(start, nearestLightPoint))
                    lightLeftInRay = 1.0
                    for s in self.shapeList :
                        ray = ray(vector.plus(start, vector.multiply(revShadeDir, 0.01)), revShadeDir)
                        shadowHit = s.intersect(ray, True)
                        if shadowHit is not None and vector.length(vector.minus(shadowHit.getInterPoint(), start)) < rayLength :
                            lightLeftInRay *= s.material.trans;
                            if lightLeftInRay < 0:
                                lightLeftInRay = 0
                                break
                    illumination -= shadeRayFraction * (1 - lightLeftInRay)

            if illumination > 0 :
                #computation of diffuse light
                diffuseColor = self.light.color.mulC(mat.diffuse.mulS(vector.dotProduct(intersection.getNormal(), revLightDir)))
                # computation of specular light
                specularColor = self.light.color.mulC(mat.specular.mulS(self.light.specular * pow(abs(vector.dotProduct(lightRefDir, intersection.getDirection())), mat.phong)))
                color = color.plus(diffuseColor.plus(specularColor).mulS((1 - mat.trans) * illumination))
        refDirHit = vector.reflect(intersection.direction, (intersection.normal))
        ray2 = ray(vector.plus(intersection.inter_point, (vector.multiply(refDirHit, 0.001))), refDirHit)
        rayReflection = self.ray_cast(ray2);
        reflectionColor = mat.reflection.mulC(self.compute_color(rayReflection, self.recCount + 1, contribution * mat.reflection.grayScale()))
        color = color.plus(reflectionColor);
        if mat.trans > 0:
            rayRec = ray(vector.plus(intersection.inter_point, vector.multiply(intersection.direction, 0.01)), intersection.direction)
            next = self.ray_cast(rayRec);
            color = color.plus(self.compute_color(next, self.recCount + 1, contribution * mat.trans).mulS(mat.trans))
        return color
