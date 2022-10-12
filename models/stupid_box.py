from .model import Model
import numpy as np

import trimesh
import trimesh.transformations as transforms

class StupidBox(Model):
    def __init__(self) -> None:
        Model.__init__(self)
        self.scene = None
        self.__build_model()

    def __build_model(self):
        self.scene = trimesh.Scene()
        plane = trimesh.creation.box(extents=[5, 5, 0.01])
        plane.visual.face_colors = [0.5, 0.5, 0.5, 0.5]
        self.scene.add_geometry(plane)
        self.scene.add_geometry(trimesh.creation.axis())

        # object-1 (box)
        box = trimesh.creation.box(extents=[0.3, 0.3, 0.3])
        box.visual.face_colors = [0, 1., 0, 0.5]
        axis = trimesh.creation.axis(origin_color=[1., 0, 0])
        translation = [-0.2, 0, 0.15 + 0.01]  # box offset + plane offset
        box.apply_translation(translation)
        axis.apply_translation(translation)
        rotation = trimesh.transformations.rotation_matrix(
            np.deg2rad(30), [0, 0, 1], point=box.centroid
        )
        box.apply_transform(rotation)
        axis.apply_transform(rotation)
        self.scene.add_geometry(box)
        self.scene.add_geometry(axis)

    def show_box(self):
        self.scene.show()


    def integrate(self) -> None:
        return None

    def show_model(self) -> None:
        pass