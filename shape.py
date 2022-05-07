import material


class Shape:
    # material = material()

    def __init__(self, inputMaterial: material.Material):
        self.material = inputMaterial

    # All of the shapes need to implement intersect
